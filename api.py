import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from dotenv import load_dotenv
from crewai import Crew, Process

from agents.agents import analista, consultor
from tasks.tasks import tarefa_documentacao, tarefa_melhorias

load_dotenv()

app = FastAPI(
    title="CrewAI - Análise de Código GitHub",
    description="API que recebe um link de repositório GitHub e retorna documentação e sugestões de melhorias.",
    version="1.0.0",
)


class RepoRequest(BaseModel):
    repo_url: str

    class Config:
        json_schema_extra = {
            "example": {
                "repo_url": "https://github.com/crewAIInc/crewAI"
            }
        }


class AnalysisResponse(BaseModel):
    repo_url: str
    resultado: str


@app.post("/analisar", response_model=AnalysisResponse)
async def analisar_repositorio(request: RepoRequest):
    """
    Recebe a URL de um repositório GitHub e executa os agentes
    de análise de código e sugestão de melhorias.
    """
    if not request.repo_url.startswith("https://github.com/"):
        raise HTTPException(
            status_code=400,
            detail="URL inválida. Informe uma URL válida do GitHub (https://github.com/...)"
        )

    os.environ["GITHUB_REPO_URL"] = request.repo_url

    crew = Crew(
        agents=[analista, consultor],
        tasks=[tarefa_documentacao, tarefa_melhorias],
        process=Process.sequential,
        verbose=True,
    )

    resultado = crew.kickoff(inputs={"repo_url": request.repo_url})

    return AnalysisResponse(
        repo_url=request.repo_url,
        resultado=str(resultado),
    )


@app.get("/")
async def root():
    return {
        "message": "CrewAI - Análise de Código GitHub",
        "docs": "/docs",
        "uso": "POST /analisar com { \"repo_url\": \"https://github.com/usuario/repo\" }",
    }


if __name__ == "__main__":
    import uvicorn
    # Rodar com: C:\cv\Scripts\python api.py
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
