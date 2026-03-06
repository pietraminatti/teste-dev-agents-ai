# 🚀 CrewAI - Dois Agentes

Projeto demonstrando dois agentes CrewAI trabalhando em conjunto:

| Agente | Papel | Função |
|--------|-------|--------|
| **Pesquisador** | Pesquisador Sênior de Tecnologia | Pesquisa informações detalhadas sobre o tema |
| **Redator** | Redator Especialista em Conteúdo | Escreve um artigo com base na pesquisa |

## Fluxo

```
Tema → [Pesquisador] → Relatório → [Redator] → Artigo Final
```

## Setup

```bash
# 1. Criar ambiente virtual
python -m venv venv
venv\Scripts\activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar API key
copy .env.example .env
# Edite o .env com sua OPENAI_API_KEY

# 4. Executar
python main.py
```
