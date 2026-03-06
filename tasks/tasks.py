from crewai import Task
from agents.agents import analista, consultor

# Tarefa 1: Documentação do Código


tarefa_documentacao = Task(
    description=(
        "Analise o repositório GitHub {repo_url} em profundidade. "
        "Mapeie a estrutura do projeto, identifique os módulos principais, "
        "documente as classes e funções mais importantes, "
        "e descreva o fluxo geral da aplicação. "
        "Use a ferramenta de busca no GitHub para navegar pelo código. "
        "Estruture o resultado seguindo o template em README_TEMPLATE.md:\n"
        "- Visão geral clara e concisa\n"
        "- Características principais\n"
        "- Pré-requisitos e instalação\n"
        "- Estrutura do projeto com diagrama\n"
        "- Arquitetura com fluxo visual\n"
        "- Tecnologias e versões utilizadas\n"
        "- Exemplos práticos de uso\n\n"
        "IMPORTANTE: Sua resposta deve conter APENAS o README em Markdown. "
        "Não inclua explicações, pensamentos ou preâmbulos. "
        "Comece diretamente com o título do projeto (# Nome do Projeto)."
    ),
    expected_output=(
        "Um README.md bem estruturado contendo:\n"
        "1) Cabeçalho com nome do projeto e descrição\n"
        "2) Sumário com links internos\n"
        "3) Visão geral e problemas que resolve\n"
        "4) Características principais (lista com ✅)\n"
        "5) Pré-requisitos claros\n"
        "6) Instruções de instalação passo a passo\n"
        "7) Exemplos de uso com código\n"
        "8) Estrutura de diretórios com explicação\n"
        "9) Diagrama de arquitetura em ASCII\n"
        "10) Tabela de tecnologias com versões\n"
        "11) Exemplos e resultados esperados\n"
        "12) Seção de troubleshooting\n"
        "13) Licença, autor e contato\n\n"
        "ATENÇÃO: A resposta deve ser APENAS o markdown do README. "
        "Sem explicações, comentários ou pensamentos adicionais."
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
        "Use a ferramenta de busca no GitHub para examinar trechos específicos do código.\n\n"
        "IMPORTANTE: Sua resposta deve conter APENAS um relatório estruturado. "
        "Não inclua pensamentos preliminares, explicações ou preâmbulos. "
        "Comece diretamente com o título ou seção do relatório."
    ),
    expected_output=(
        "Um relatório de melhorias contendo:\n"
        "1) Lista de melhorias priorizadas (Alta / Média / Baixa)\n"
        "2) Para cada melhoria:\n"
        "   - Descrição do problema encontrado\n"
        "   - Arquivo e trecho de código afetado\n"
        "   - Sugestão concreta de como melhorar (com exemplo de código quando possível)\n"
        "   - Justificativa e benefício esperado\n"
        "3) Resumo executivo com as 3 melhorias mais impactantes\n\n"
        "ATENÇÃO: Responda APENAS com o relatório estruturado. "
        "Sem explicações prévias ou comentários adicionais."
    ),
    agent=consultor,
)
