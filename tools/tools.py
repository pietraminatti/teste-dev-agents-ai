import os
import requests
from crewai.tools import BaseTool
from pydantic import Field


class GithubRepoTool(BaseTool):
    name: str = "GitHub Repository Search"
    description: str = (
        "Busca código e arquivos em um repositório GitHub. "
        "Recebe uma query de busca e retorna trechos relevantes do repositório."
    )
    gh_token: str = Field(default="")
    repo_url: str = Field(default="")

    def _run(self, query: str) -> str:
        repo = self.repo_url.rstrip("/")
        # Extrai owner/repo da URL
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

        if resp.status_code != 200:
            return f"Erro na API do GitHub: {resp.status_code} - {resp.text}"

        items = resp.json().get("items", [])
        if not items:
            return "Nenhum resultado encontrado."

        results = []
        for item in items:
            results.append(f"📄 {item['path']}\n   {item['html_url']}")
        return "\n\n".join(results)


github_tool = GithubRepoTool(
    gh_token=os.getenv("GITHUB_TOKEN", ""),
    repo_url=os.getenv("GITHUB_REPO_URL", ""),
)
