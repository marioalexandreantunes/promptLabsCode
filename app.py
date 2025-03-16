import streamlit as st
import os
import uuid

from dotenv import load_dotenv
from groq_ai import re_prompt
from sanitize import sanitize_prompt
from streamlit_cookies_controller import CookieController
from datetime import datetime, timedelta

load_dotenv() 

DEBUG = os.getenv("DEBUG") == "True"


# Set page configuration with Portuguese title
st.set_page_config(
    page_title="Aplicação de Criação de Prompts",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
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

# Initialize session variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# Get all cookies first
#st.session_state.cookie_manager = stx.CookieManager()

st.session_state.cookie_manager = CookieController()
cookie_manager = st.session_state.cookie_manager
all_cookies = cookie_manager.getAll()


# Check for session in cookies using the all_cookies dictionary
session_token = all_cookies.get("session_token")
session_expiry = all_cookies.get("session_expiry")

if DEBUG:
    print("======================= root ============================")
    print(f"Debug - Token: {session_token}")
    print(f"Debug - Expiry: {session_expiry}")

if session_token and session_expiry:
    try:
        expiry = datetime.fromisoformat(session_expiry)
        if DEBUG:
            print(f"Debug - Current time: {datetime.now()}")
            print(f"Debug - Expiry time: {expiry}")
            print(f"Debug - Is valid: {expiry > datetime.now()}")
        
        if expiry > datetime.now():
            st.session_state.logged_in = True
            st.sidebar.success("Session loaded from cookie")
        else:
            st.sidebar.warning("Session expired")
    except Exception as e:
        # Invalid or expired token
        print(f"Error: {e}")
        pass

# Função para verificar login
def check_login(username, password):
    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")
    if DEBUG:
        print("======================= login ============================")
    if username == admin_username and password == admin_password:
        # Generate a session token and set expiry (1 day for better testing)
        session_id = str(uuid.uuid4())
        expiry_time = datetime.now() + timedelta(days=1)
        expiry_str = expiry_time.isoformat()
        
        # Set cookies with unique keys and longer max_age
        '''
        cookie_manager.set(
            cookie="session_token", 
            val=session_id,
            expires_at=expiry_time,
            key="set_token",
            path="/"  # Add path parameter
        )
        cookie_manager.set(
            cookie="session_expiry", 
            val=expiry_str,
            expires_at=expiry_time,
            key="set_expiry",
            path="/"  # Add path parameter
        )
        '''
        cookie_manager.set(
            "session_token", 
            session_id,
        )
        cookie_manager.set(
            "session_expiry", 
            expiry_str
        )
        
        # Make sure to set the session state before rerunning
        st.session_state.logged_in = True
        if DEBUG:
            print("Login successful, cookie set")
            print(f"Debug - Token: {cookie_manager.get('session_token')}")
            print(f"Debug - Expiry: {cookie_manager.get('session_expiry')}")
        
        # Add a small delay before rerunning to ensure cookies are set
        st.rerun()
    else:
        st.error("Usuário ou senha incorretos!")

# Se o usuário ainda não está logado, mostra a tela de login
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns(3)
    with col2:
        st.title("🔑 Login")
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            check_login(username, password)
else:
    # Main page header (keeping Portuguese for UI elements)
    st.title("Aplicação de Criação de Prompts")
    st.subheader("Crie prompts bem estruturados para modelos de IA")

    # Add logout button
    if st.sidebar.button("Logout"):
        # Get all cookies to check existence

        session_token = all_cookies.get("session_token")
        session_expiry = all_cookies.get("session_expiry")

        if DEBUG:
            print("======================= logout ============================")
            print(f"Debug - All Cookies before deletion: {all_cookies}")
            print(f"Debug - Token before deletion: {session_token}")
            print(f"Debug - Expiry before deletion: {session_expiry}")
        # Delete cookies if they exist
        #cookie_manager.delete("session_token", key="delete_token")
        #cookie_manager.delete("session_expiry", key="delete_expiry")
        cookie_manager.remove('session_token')
        cookie_manager.remove('session_expiry')
        #cookie_manager.delete("session_expiry")
            
        # Clear session state and set logged_in to False
        # st.session_state.clear()
        st.session_state.logged_in = False

        if DEBUG:
            print(f"Debug - All Cookies after deletion: {cookie_manager.get('session_token')}")
            print(f"Debug - All Cookies after deletion: {cookie_manager.get('session_expiry')}")

        st.session_state.clear()
        
        # Force a rerun to show login page
        st.rerun()

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
            "3. Verifique o prompt melhorado\n"
            "4. Copie e utilize com o seu modelo de IA favorito"
        )
        st.write("---")
        st.markdown(
            "<a href='https://www.mariocodelabs.com/'><img src='https://i.imgur.com/Ebf0JAJ.png' width='250'></a>",
            unsafe_allow_html=True,
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
            height=150,
        )

        context_dump = st.text_area(
            "Contexto",
            placeholder="Defina contexto adicional ou exemplos\nExemplo: Explica blockchain para um iniciante sem termos técnicos complicados.",
            height=150,
        )

    # Second column with Warnings and Context fields
    with col2:
        warnings = st.text_area(
            "Avisos",
            placeholder="Defina quaisquer avisos ou restrições\nExemplo: O texto não pode ter mais de 200 palavras.",
            height=150,
        )

        return_format = st.text_area(
            "Formato de Retorno",
            placeholder="Defina o formato para os dados retornados\nExemplo: Cria uma lista com os 5 principais desafios do blockchain.",
            height=150,
        )

    # Button to generate the prompt
    generate_button = st.button("Gerar Prompt", type="primary", icon="👽")

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
            st.success(
                "O seu prompt está pronto! Copie-o e utilize com o seu modelo de IA favorito."
            )
        else:
            st.info("Preencha pelo menos um campo para gerar um prompt.")
    else:
        st.info(
            "Preencha os campos acima e clique em 'Gerar Prompt' para criar o seu prompt."
        )

    # Add a footer with logo and link
    st.markdown("---")
    year = datetime.now().year
    st.markdown(f"marioCodeLabs.com © {year}")
