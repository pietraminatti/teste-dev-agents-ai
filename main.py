import os
from dotenv import load_dotenv
from crewai import Crew, Process

from agents.agents import analista, consultor
from tasks.tasks import tarefa_documentacao, tarefa_melhorias

load_dotenv()

crew = Crew(
    agents=[analista, consultor],
    tasks=[tarefa_documentacao, tarefa_melhorias],
    process=Process.sequential,
    verbose=True,
)


def main():
    print("  CrewAI - Análise de Código GitHub")
    print("=" * 60)

    repo_url = input("\n Cole a URL do repositório GitHub: ").strip()

    if not repo_url:
        repo_url = "https://github.com/crewAIInc/crewAI"
        print(f"   Usando repo padrão: {repo_url}")

    # Atualiza a variável de ambiente para o GithubSearchTool
    os.environ["GITHUB_REPO_URL"] = repo_url

    print("\n Iniciando análise do repositório...\n")

    resultado = crew.kickoff(inputs={"repo_url": repo_url})

    print("\n" + "=" * 60)
    print(" Análise Completa")
    print("=" * 60)
    print(resultado)


if __name__ == "__main__":
    main()
