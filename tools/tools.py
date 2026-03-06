import os
import requests
from crewai.tools import BaseTool
from pydantic import Field


class GithubRepoTool(BaseTool):
    name: str = "GitHub Repository Search"
    description: str = (
        "Busca arquivos e código dentro de um repositório GitHub. "
        "Use para encontrar implementações, funções ou arquivos "
        "relacionados a um termo específico."
    )

    gh_token: str = Field(default="")
    repo_url: str = Field(default="")

    def _run(self, query: str) -> str:

        if not self.repo_url:
            return "repo_url não configurado."

        repo = self.repo_url.rstrip("/").replace(".git", "")
        parts = repo.replace("https://github.com/", "").split("/")

        if len(parts) < 2:
            return "URL do repositório inválida."

        owner, repo_name = parts[0], parts[1]

        headers = {"Accept": "application/vnd.github+json"}

        if self.gh_token:
            headers["Authorization"] = f"Bearer {self.gh_token}"

        params = {"q": f"{query} repo:{owner}/{repo_name}", "per_page": 5}

        resp = requests.get(
            "https://api.github.com/search/code",
            headers=headers,
            params=params,
            timeout=15,
        )

        if resp.status_code == 403:
            return "Rate limit da API do GitHub atingido."

        if resp.status_code != 200:
            return f"Erro na API do GitHub: {resp.status_code}"

        items = resp.json().get("items", [])

        if not items:
            return "Nenhum resultado encontrado."

        results = []

        for item in items:
            results.append(
                f"📄 {item['path']}\n"
                f"🔗 {item['html_url']}"
            )

        return "\n\n".join(results)


github_tool = GithubRepoTool(
    gh_token=os.getenv("GITHUB_TOKEN", ""),
    repo_url=os.getenv("GITHUB_REPO_URL", ""),
)