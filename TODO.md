# TODO: Melhorias do Projeto Streamlit

Este documento descreve melhorias potenciais para a Aplicação de Criação de Prompts baseada em Streamlit, focando em segurança e boas práticas de Python.

## Alta Prioridade

### Melhorias de Segurança

- [ ] **Gestão Segura de Chaves API**: Melhorar o sistema atual de gestão da chave API Groq usando variáveis de ambiente e .env.
  - Adicionar validação da chave API no arranque da aplicação
  - Implementar mensagens de erro amigáveis quando a chave API não estiver disponível
- [ ] **Validação de Input**: Adicionar validação abrangente para todos os inputs do utilizador nos campos de texto.
  - Verificar comprimentos máximos
  - Validar conteúdo antes de enviar para a API Groq
- [ ] **Gestão de Erros da API**: Melhorar o tratamento de erros nas chamadas à API Groq para fornecer feedback útil ao utilizador.

### Boas Práticas de Python

- [ ] **Type Hints**: Adicionar type hints em todo o código (já iniciado em `groq_ai.py`).
- [ ] **Tratamento de Erros**: Implementar tratamento adequado de exceções para chamadas à API e operações de ficheiros.
- [ ] **Logging**: Adicionar logging estruturado em vez de print statements para melhor debugging e monitorização.
- [ ] **Gestão de Configuração**: Mover configurações de valores hardcoded para um módulo de configuração dedicado.

## Prioridade Média

### Qualidade de Código

- [ ] **Documentação de Código**: Adicionar docstrings a todas as funções e classes seguindo PEP 257.
- [ ] **Linting de Código**: Configurar linting com ferramentas como flake8, pylint, ou ruff.
- [ ] **Formatação de Código**: Implementar formatação automática de código com black ou yapf.

### Gestão de Dependências

- [ ] **Fixação de Versões**: Garantir que todas as dependências têm versões fixas (já feito em requirements.txt).
- [ ] **Verificação de Dependências**: Implementar verificação regular de dependências vulneráveis.

## Baixa Prioridade

### Melhorias da Aplicação Streamlit

- [ ] **Cache de Streamlit**: Utilizar st.cache para melhorar o desempenho em operações repetitivas.
- [ ] **Temas Personalizados**: Implementar temas personalizados para melhorar a aparência da aplicação.
- [ ] **Componentes Reutilizáveis**: Criar componentes Streamlit reutilizáveis para partes comuns da UI.
- [ ] **Sessão de Estado**: Utilizar st.session_state para uma melhor gestão de estado da aplicação.
- [ ] **Internacionalização**: Melhorar o suporte para múltiplos idiomas (atualmente misturando Português e Inglês).
- [ ] **Acessibilidade**: Garantir que a aplicação é acessível a utilizadores com deficiências.

### Documentação

- [ ] **Guia do Utilizador**: Criar um guia de utilizador abrangente para a aplicação.
- [ ] **Documentação para Desenvolvedores**: Adicionar documentação para desenvolvedores que queiram contribuir para o projeto.

## Notas de Implementação

### Para Melhorias de Segurança

```python
# Exemplo de gestão melhorada de chave API
import os
import streamlit as st
from dotenv import load_dotenv

# Carregar variáveis de ambiente do ficheiro .env
load_dotenv()

# Obter chave API com tratamento de erros
def get_api_key():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        st.error("Chave API GROQ não configurada. Por favor configure a variável de ambiente GROQ_API_KEY.")
        st.stop()
    return api_key
```

### Para Tratamento de Erros

```python
# Exemplo de tratamento de erros melhorado para chamadas à API
import logging
import streamlit as st
from groq.error import GroqError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_api_call(func):
    try:
        return func()
    except GroqError as e:
        logger.error(f"Erro ao chamar API Groq: {e}")
        st.error("Desculpe, ocorreu um erro ao processar o seu pedido. Por favor tente novamente mais tarde.")
        return None
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        st.error("Ocorreu um erro inesperado. Por favor contacte o suporte.")
        return None
```

### Para Validação de Input

```python
# Exemplo de validação de input
def validate_prompt_input(text):
    if not text or not text.strip():
        return False, "Por favor forneça um texto válido."
    if len(text) > 5000:  # Definir um limite razoável
        return False, "O texto é demasiado longo. Por favor limite a 5000 caracteres."
    return True, ""

# Em app.py
if generate_button:
    is_valid, error_msg = validate_prompt_input(goal)
    if not is_valid:
        st.error(error_msg)
    else:
        # Continuar com o processamento...
```