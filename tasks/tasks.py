from crewai import Task
from agents.agents import analista, consultor

# Tarefa 1: Documentação do Código


tarefa_documentacao = Task(
    description=(
        "Analise o repositório GitHub {repo_url} em profundidade. "
        "Mapeie a estrutura do projeto, identifique os módulos principais, "
        "documente as classes e funções mais importantes, "
        "e descreva o fluxo geral da aplicação. "
        "Use a ferramenta de busca no GitHub para navegar pelo código."
    ),
    expected_output=(
        "Um documento técnico estruturado contendo:\n"
        "1) Visão geral do projeto e sua finalidade\n"
        "2) Estrutura de diretórios e arquivos principais\n"
        "3) Descrição dos módulos/componentes e suas responsabilidades\n"
        "4) Classes e funções principais com breve explicação\n"
        "5) Fluxo geral da aplicação\n"
        "6) Tecnologias e dependências utilizadas"
    ),
    agent=analista,
)

# ──────────────────────────────────────────────
# Tarefa 2: Sugestões de Melhorias
# ──────────────────────────────────────────────

tarefa_melhorias = Task(
    description=(
        "Com base na análise do repositório {repo_url}, "
        "identifique pontos de melhoria no código. "
        "Avalie aspectos como: refatoração, boas práticas (SOLID, Clean Code), "
        "performance, segurança, tratamento de erros, testes e manutenibilidade. "
        "Use a ferramenta de busca no GitHub para examinar trechos específicos do código."
    ),
    expected_output=(
        "Um relatório de melhorias contendo:\n"
        "1) Lista de melhorias priorizadas (Alta / Média / Baixa)\n"
        "2) Para cada melhoria:\n"
        "   - Descrição do problema encontrado\n"
        "   - Arquivo e trecho de código afetado\n"
        "   - Sugestão concreta de como melhorar (com exemplo de código quando possível)\n"
        "   - Justificativa e benefício esperado\n"
        "3) Resumo executivo com as 3 melhorias mais impactantes"
    ),
    agent=consultor,
)
