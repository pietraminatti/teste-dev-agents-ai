from crewai import Task
from agents.agents import analista, consultor

# Tarefa 1: Documentação do Código


tarefa_documentacao = Task(
    description=(
        "Analise o repositório GitHub {repo_url} em profundidade e gere um README em Markdown. "
        "Mapeie a estrutura do projeto, identifique os módulos principais, "
        "documente as classes e funções mais importantes, "
        "e descreva o fluxo geral da aplicação. "
        "Use a ferramenta de busca no GitHub para navegar pelo código.\n\n"
        "FORMATO OBRIGATÓRIO: Markdown puro (não JSON, não XML, não código, apenas Markdown)\n"
        "ESTRUTURA: Siga este padrão:\n"
        "# Nome do Repositório\nDescrição curta\n\n"
        "## 📋 Sumário\n- [Visão Geral](#visão-geral)\n...\n\n"
        "## 👀 Visão Geral\n[Descrição detalhada]\n\n"
        "## ✨ Características\n- ✅ Característica 1\n...\n\n"
        "## 📦 Pré-requisitos\n- Python 3.10+\n...\n\n"
        "## 🚀 Instalação\n[Passos claros]\n\n"
        "## 💻 Uso\n[Exemplos com código]\n\n"
        "## 📁 Estrutura do Projeto\n[Árvore de diretórios]\n\n"
        "## 🏗️ Arquitetura\n[Diagrama e explicação]\n\n"
        "## 🛠️ Tecnologias\n[Tabela]\n\n"
        "## 🤝 Contribuindo\n[Como contribuir]\n\n"
        "## 📝 Licença\n[Informações de licença]\n\n"
        "IMPORTANTE:\n"
        "- RESPONDA APENAS COM MARKDOWN (começando com #)\n"
        "- NÃO inclua nenhum texto antes ou depois\n"
        "- NÃO use JSON, XML, ou qualquer outro formato\n"
        "- NÃO inclua explicações ou pensamentos\n"
        "- Comece diretamente com '# Nome do Projeto'"
    ),
    expected_output=(
        "Um arquivo README em Markdown puro (APENAS Markdown, nada mais):\n\n"
        "# Nome do Projeto\n\n"
        "[Conteúdo estruturado apenas em Markdown]\n\n"
        "REGRAS CRÍTICAS:\n"
        "1. APENAS Markdown (começar com #)\n"
        "2. NÃO JSON\n"
        "3. NÃO XML\n"
        "4. NÃO código de programação como resposta\n"
        "5. NÃO explicações preliminares\n"
        "6. NÃO preâmbulos\n"
        "A resposta inteira deve ser o conteúdo do README em Markdown."
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
