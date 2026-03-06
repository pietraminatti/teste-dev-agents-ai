import os
import json
import tempfile
from dotenv import load_dotenv
from crewai import Agent, LLM
from tools.tools import github_tool

load_dotenv()

# Reconstrói o JSON da service account a partir das variáveis de ambiente
_sa_info = {
    "type": os.environ["GOOGLE_TYPE"],
    "project_id": os.environ["GOOGLE_PROJECT_ID"],
    "private_key_id": os.environ["GOOGLE_PRIVATE_KEY_ID"],
    "private_key": os.environ["GOOGLE_PRIVATE_KEY"].replace("\\n", "\n"),
    "client_email": os.environ["GOOGLE_CLIENT_EMAIL"],
    "client_id": os.environ["GOOGLE_CLIENT_ID"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": os.environ["GOOGLE_TOKEN_URI"],
}

# Escreve em um arquivo temporário para que o litellm encontre via ADC
_sa_tmp = tempfile.NamedTemporaryFile(
    mode="w", suffix=".json", delete=False, encoding="utf-8"
)
json.dump(_sa_info, _sa_tmp)
_sa_tmp.flush()

# Define GOOGLE_APPLICATION_CREDENTIALS antes do LiteLLM ser inicializado
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = _sa_tmp.name
os.environ["VERTEXAI_PROJECT"] = os.environ["GOOGLE_PROJECT_ID"]
os.environ["VERTEXAI_LOCATION"] = os.getenv("VERTEXAI_LOCATION", "us-central1")

# Tenta usar gemini-2.0-flash primeiro, fallback para gemini-1.5-flash
try:
    gemini_llm = LLM(model="vertex_ai/gemini-2.0-flash")
except Exception:
    gemini_llm = LLM(model="vertex_ai/gemini-1.5-flash")


# ──────────────────────────────────────────────
# Agente 1: Analista de Código
# ──────────────────────────────────────────────

analista = Agent(
    role="Analista Sênior de Código",
    goal=(
        "Analisar o repositório GitHub {repo_url}, "
        "mapeando sua estrutura, módulos, classes e funções principais, "
        "e produzir uma documentação técnica completa."
    ),
    backstory=(
        "Você é um engenheiro de software sênior com mais de 15 anos de experiência "
        "em revisão e análise de código. Você domina múltiplas linguagens e frameworks, "
        "e é reconhecido pela sua capacidade de entender rapidamente bases de código "
        "complexas e produzir documentação clara e precisa. Você sempre analisa "
        "a arquitetura geral antes de mergulhar nos detalhes."
    ),
    tools=[github_tool],
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False,
)

# ──────────────────────────────────────────────
# Agente 2: Consultor de Melhorias
# ──────────────────────────────────────────────

consultor = Agent(
    role="Consultor de Qualidade de Software",
    goal=(
        "Analisar o código do repositório {repo_url} e sugerir melhorias concretas "
        "em refatoração, boas práticas, performance, segurança e manutenibilidade."
    ),
    backstory=(
        "Você é um consultor especialista em qualidade de software com vasta experiência "
        "em code review e melhoria contínua. Você conhece profundamente os princípios "
        "SOLID, Design Patterns, Clean Code e práticas de segurança. "
        "Suas recomendações são sempre práticas, priorizadas por impacto "
        "e acompanhadas de justificativas claras e exemplos de código."
    ),
    tools=[github_tool],
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False,
)
