"""
run_analysis.py — script headless para rodar os agentes CrewAI via GitHub Actions.
Recebe GITHUB_REPO_URL por variável de ambiente, gera documentação via CrewAI
e publica o README.md na branch 'feature-documents' (criada a partir da main)
usando a GitHub REST API.
"""

import os
import json
import base64
import tempfile
import requests
from dotenv import load_dotenv
from crewai import Crew, Process

load_dotenv()

# ── Reconstrói a service account do Google a partir dos secrets ──────────────
required_secrets = [
    "GOOGLE_TYPE",
    "GOOGLE_PROJECT_ID", 
    "GOOGLE_PRIVATE_KEY_ID",
    "GOOGLE_PRIVATE_KEY",
    "GOOGLE_CLIENT_EMAIL",
    "GOOGLE_CLIENT_ID",
]

missing_secrets = [s for s in required_secrets if not os.environ.get(s)]
if missing_secrets:
    raise ValueError(
        f"❌ Secrets não configurados no GitHub Actions: {', '.join(missing_secrets)}\n"
        f"Configure em: Settings → Secrets and variables → Actions\n"
        f"Veja GITHUB_ACTIONS_SETUP.md para instruções."
    )

_sa_info = {
    "type": os.environ["GOOGLE_TYPE"],
    "project_id": os.environ["GOOGLE_PROJECT_ID"],
    "private_key_id": os.environ["GOOGLE_PRIVATE_KEY_ID"],
    "private_key": os.environ["GOOGLE_PRIVATE_KEY"].replace("\\n", "\n"),
    "client_email": os.environ["GOOGLE_CLIENT_EMAIL"],
    "client_id": os.environ["GOOGLE_CLIENT_ID"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": os.environ.get("GOOGLE_TOKEN_URI", "https://oauth2.googleapis.com/token"),
}

_sa_tmp = tempfile.NamedTemporaryFile(
    mode="w", suffix=".json", delete=False, encoding="utf-8"
)
json.dump(_sa_info, _sa_tmp)
_sa_tmp.flush()
_sa_tmp.close()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = _sa_tmp.name
os.environ["VERTEXAI_PROJECT"] = os.environ["GOOGLE_PROJECT_ID"]
os.environ["VERTEXAI_LOCATION"] = os.getenv("VERTEXAI_LOCATION", "us-central1")

# ── Importa agentes e tarefas DEPOIS de configurar as credenciais ─────────────
from agents.agents import analista, consultor       # noqa: E402
from tasks.tasks import tarefa_documentacao, tarefa_melhorias  # noqa: E402


# ── Helpers da GitHub REST API ────────────────────────────────────────────────

def _gh_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def _parse_repo(repo_url: str) -> tuple[str, str]:
    """Extrai owner e repo_name de uma URL GitHub."""
    clean = repo_url.rstrip("/").replace("https://github.com/", "").removesuffix(".git")
    parts = clean.split("/")
    if len(parts) < 2:
        raise ValueError(f"URL do repositório inválida: {repo_url}")
    return parts[0], parts[1]


def _get_branch_sha(owner: str, repo: str, branch: str, token: str) -> str:
    """Retorna o SHA do topo de uma branch."""
    url = f"https://api.github.com/repos/{owner}/{repo}/git/refs/heads/{branch}"
    resp = requests.get(url, headers=_gh_headers(token), timeout=15)
    if resp.status_code == 404:
        raise ValueError(f"Branch '{branch}' não encontrada no repositório {owner}/{repo}.")
    resp.raise_for_status()
    return resp.json()["object"]["sha"]


def _create_or_reset_branch(owner: str, repo: str, new_branch: str, base_sha: str, token: str) -> None:
    """Cria a branch 'new_branch' a partir de base_sha. Se já existir, reseta para base_sha."""
    ref = f"refs/heads/{new_branch}"
    headers = _gh_headers(token)

    # Tenta criar
    create_resp = requests.post(
        f"https://api.github.com/repos/{owner}/{repo}/git/refs",
        headers=headers,
        json={"ref": ref, "sha": base_sha},
        timeout=15,
    )

    if create_resp.status_code == 422:
        # Branch já existe → reseta (force update) para o SHA da main
        patch_resp = requests.patch(
            f"https://api.github.com/repos/{owner}/{repo}/git/refs/heads/{new_branch}",
            headers=headers,
            json={"sha": base_sha, "force": True},
            timeout=15,
        )
        patch_resp.raise_for_status()
        print(f"🔄 Branch '{new_branch}' resetada para o topo da main.")
    else:
        create_resp.raise_for_status()
        print(f"✅ Branch '{new_branch}' criada a partir da main.")


def _get_file_sha(owner: str, repo: str, path: str, branch: str, token: str) -> str | None:
    """Retorna o SHA do arquivo no repositório, ou None se não existir."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    resp = requests.get(url, headers=_gh_headers(token), params={"ref": branch}, timeout=15)
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json().get("sha")


def _commit_file(
    owner: str,
    repo: str,
    path: str,
    content: str,
    branch: str,
    commit_message: str,
    token: str,
) -> None:
    """Cria ou sobrescreve um arquivo em uma branch via GitHub API."""
    file_sha = _get_file_sha(owner, repo, path, branch, token)
    encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")

    payload: dict = {
        "message": commit_message,
        "content": encoded,
        "branch": branch,
    }
    if file_sha:
        payload["sha"] = file_sha  # necessário para atualizar um arquivo existente

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    resp = requests.put(url, headers=_gh_headers(token), json=payload, timeout=30)
    resp.raise_for_status()
    print(f"📄 Arquivo '{path}' commitado na branch '{branch}'.")


# ── Fluxo principal ───────────────────────────────────────────────────────────

def main():
    repo_url = os.environ.get("GITHUB_REPO_URL", "").strip()
    if not repo_url:
        raise ValueError("GITHUB_REPO_URL não definida.")

    gh_token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not gh_token:
        raise ValueError("GITHUB_TOKEN não definido.")

    doc_branch = os.environ.get("DOC_BRANCH", "feature-documents")
    base_branch = os.environ.get("BASE_BRANCH", "main")

    print(f"🔍 Analisando repositório: {repo_url}")
    os.environ["GITHUB_REPO_URL"] = repo_url

    # ── 1. Roda os agentes CrewAI ─────────────────────────────────────────────
    crew = Crew(
        agents=[analista, consultor],
        tasks=[tarefa_documentacao, tarefa_melhorias],
        process=Process.sequential,
        verbose=True,
    )
    resultado = crew.kickoff(inputs={"repo_url": repo_url})

    # ── 2. Monta o conteúdo do README.md ──────────────────────────────────────
    readme_content = f"""# 📖 Documentação Automática — Gerada por CrewAI

> Este arquivo foi gerado automaticamente pelos agentes CrewAI em resposta ao último commit.
> **Repositório analisado:** {repo_url}

---

{resultado}
"""

    # ── 3. Publica no GitHub ───────────────────────────────────────────────────
    owner, repo_name = _parse_repo(repo_url)

    print(f"\n📡 Publicando documentação no repositório {owner}/{repo_name}...")

    # Obtém o SHA do topo da main
    base_sha = _get_branch_sha(owner, repo_name, base_branch, gh_token)

    # Cria ou reseta a branch feature-documents
    _create_or_reset_branch(owner, repo_name, doc_branch, base_sha, gh_token)

    # Commita o README.md na branch de documentação
    _commit_file(
        owner=owner,
        repo=repo_name,
        path="README.md",
        content=readme_content,
        branch=doc_branch,
        commit_message="docs: auto-generate README via CrewAI 🤖",
        token=gh_token,
    )

    print(f"\n🎉 Documentação publicada com sucesso na branch '{doc_branch}'!")
    print(f"   → https://github.com/{owner}/{repo_name}/tree/{doc_branch}")


if __name__ == "__main__":
    main()
