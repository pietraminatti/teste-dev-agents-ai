# 🚀 Configuração do GitHub Actions

Este projeto usa **GitHub Actions** para automaticamente analisar o repositório e gerar documentação sempre que há um commit na branch `main`.

## 📋 Como Funciona

1. **Trigger:** Quando você faz push para a branch `main`, o workflow é acionado automaticamente
2. **Análise:** Os agentes CrewAI analisam o repositório
3. **Documentação:** Um README é gerado e commitado automaticamente na branch `feature/documents`
4. **Atualização:** Se a branch já existe, apenas o README é sobrescrito

## 🔑 Configuração de Secrets

Para que o workflow funcione, você precisa adicionar os seguintes secrets no repositório:

### 1. Acesso ao GitHub (Obrigatório)
- **`GITHUB_TOKEN`**: Já é fornecido automaticamente pelo GitHub Actions ✅

### 2. Credenciais do Google Cloud (Para o Vertex AI)
Você precisa converter o arquivo `service_account.json` em variáveis de ambiente:

- **`GOOGLE_TYPE`**: Valor de `"type"` no JSON
- **`GOOGLE_PROJECT_ID`**: Valor de `"project_id"` no JSON
- **`GOOGLE_PRIVATE_KEY_ID`**: Valor de `"private_key_id"` no JSON
- **`GOOGLE_PRIVATE_KEY`**: Valor completo de `"private_key"` (com `\n` preservados)
- **`GOOGLE_CLIENT_EMAIL`**: Valor de `"client_email"` no JSON
- **`GOOGLE_CLIENT_ID`**: Valor de `"client_id"` no JSON
- **`GOOGLE_TOKEN_URI`**: Normalmente `https://oauth2.googleapis.com/token`

### 3. Configuração do Vertex AI (Opcional)
- **`VERTEXAI_LOCATION`**: Região do Vertex AI (padrão: `us-central1`)

## 📝 Passos para Adicionar Secrets

1. Acesse o repositório no GitHub
2. Vá para **Settings** → **Secrets and variables** → **Actions**
3. Clique em **New repository secret**
4. Adicione cada secret com o nome e valor correspondente

### Exemplo de `GOOGLE_PRIVATE_KEY`:
```
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...
...
-----END PRIVATE KEY-----
```

⚠️ **Importante:** Certifique-se de incluir as quebras de linha (`\n`) do arquivo original.

## 🔄 Fluxo de Execução

```
Push em main
    ↓
GitHub Actions dispara
    ↓
Instala dependências
    ↓
Executa run_analysis.py
    ↓
Agentes CrewAI analisam o repositório
    ↓
README gerado
    ↓
Cria/atualiza branch feature/documents
    ↓
README commitado com mensagem "docs: auto-generate README via CrewAI 🤖"
```

## 📊 Status do Workflow

Você pode acompanhar o status do workflow em:
- **Actions** tab do repositório
- Clique no workflow `Analyze Repository and Generate Documentation`

## 🛠️ Troubleshooting

### Erro: "GITHUB_TOKEN não definido"
- O token é fornecido automaticamente, mas pode não ter permissões suficientes
- Verifique **Settings** → **Actions** → **General** → **Workflow permissions**
- Selecione "Read and write permissions"

### Erro: "Credenciais do Google inválidas"
- Verifique se todos os secrets foram adicionados corretamente
- Certifique-se de que a `GOOGLE_PRIVATE_KEY` contém o texto completo com quebras de linha

### Workflow não dispara
- Verifique se você está fazendo push para a branch `main`
- Certifique-se de que o arquivo `.github/workflows/analyze-and-document.yml` existe
- Verifique os logs em **Actions** para mais detalhes

## 📌 Notas Importantes

- O workflow roda em **Ubuntu Latest**
- Python 3.11 é utilizado
- O `GITHUB_TOKEN` é fornecido automaticamente pelo GitHub Actions
- A branch `feature/documents` é criada/resetada automaticamente
- O README é sobrescrito a cada execução (não há histórico de versões)

Para mais informações, consulte a [documentação oficial do GitHub Actions](https://docs.github.com/en/actions).
