import streamlit as st
from groq_ai import re_prompt
from sanitize import sanitize_prompt

# Set page configuration with Portuguese title
st.set_page_config(
    page_title="Aplicação de Criação de Prompts",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Hide the Settings button with CSS
hide_settings_button = """
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
"""

st.markdown(hide_settings_button, unsafe_allow_html=True)


# Main page header (keeping Portuguese for UI elements)
st.title("Aplicação de Criação de Prompts")
st.subheader("Crie prompts bem estruturados para modelos de IA")

# Add a sidebar with information (Portuguese UI text)
with st.sidebar:
    st.header("Sobre")
    st.write(
        "Esta aplicação ajuda-o a criar prompts estruturados para modelos de IA, definindo "
        "componentes-chave como objetivos, requisitos de formato, avisos e contexto."
    )
    st.write("---")
    st.write("### Como utilizar")
    st.write(
        "1. Preencha as quatro secções no painel principal\n"
        "2. Reveja o seu prompt gerado\n"
        "3. Copie e utilize com o seu modelo de IA favorito"
    )

# Main content area - Prompt components section
st.write("## Componentes do Prompt")

# Create two columns for the form layout
col1, col2 = st.columns(2)

# First column with Goal and Return Format fields
with col1:
    goal = st.text_area(
        "Objetivo", 
        placeholder="Defina o objetivo do agente de IA\nExemplo: Gera um resumo de 100 palavras sobre blockchain.",
        height=150
    )
    
    return_format = st.text_area(
        "Formato de Retorno", 
        placeholder="Defina o formato para os dados retornados\nExemplo: Cria uma lista com os 5 principais desafios do blockchain.",
        height=150
    )

# Second column with Warnings and Context fields
with col2:
    warnings = st.text_area(
        "Avisos", 
        placeholder="Defina quaisquer avisos ou restrições\nExemplo: O texto não pode ter mais de 200 palavras.",
        height=150
    )
    
    context_dump = st.text_area(
        "Contexto", 
        placeholder="Defina contexto adicional ou exemplos\nExemplo: Explica blockchain para um iniciante sem termos técnicos complicados.",
        height=150
    )

# Button to generate the prompt
generate_button = st.button("Gerar Prompt", type="primary")

# Display section for the generated prompt
st.write("---")
st.write("## Prompt Gerado")

# Generate and display the prompt if button is clicked or any field has content
if generate_button or (goal or return_format or warnings or context_dump):
    # Create the formatted prompt by combining all sections
    prompt_parts = []
    
    if goal:
        prompt_parts.append(f"**Objetivo:**\n{goal}\n")
    
    if return_format:
        prompt_parts.append(f"**Formato de Retorno:**\n{return_format}\n")
    
    if warnings:
        prompt_parts.append(f"**Avisos:**\n{warnings}\n")
    
    if context_dump:
        prompt_parts.append(f"**Contexto:**\n{context_dump}")
    
    # Join all parts with line breaks
    final_prompt_1 = "\n".join(prompt_parts)
    
    # Sanitize the prompt before sending to Groq AI
    sanitized_prompt, issues = sanitize_prompt(final_prompt_1)
    
    # Display warning messages if any issues were found during sanitization
    if issues:
        for issue_type, message in issues.items():
            st.warning(f"⚠️ {message}")
    
    # Get enhanced prompt from Groq AI using the sanitized prompt
    final_prompt_2 = re_prompt(sanitized_prompt)
    
    # Display both original and enhanced prompts
    if sanitized_prompt:
        st.text_area("O seu Prompt:", final_prompt_1, height=300)
        st.text_area("O seu Prompt melhorado:", final_prompt_2, height=300)
        st.success("O seu prompt está pronto! Copie-o e utilize com o seu modelo de IA favorito.")
    else:
        st.info("Preencha pelo menos um campo para gerar um prompt.")
else:
    st.info("Preencha os campos acima e clique em 'Gerar Prompt' para criar o seu prompt.")

# Add a footer with logo and link
st.markdown("---")

# Pure markdown footer with HTML img tag for size control
col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
with col3:
    st.markdown("<a href='https://www.mariocodelabs.com/'><img src='https://i.imgur.com/Ebf0JAJ.png' width='300'></a>", unsafe_allow_html=True)