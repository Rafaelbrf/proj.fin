import streamlit as st  # biblioteca para criar a interface web interativa
from novo_usuario import criar_conta  # função que salva novo usuário no arquivo CSV
from login import login_usuario_arquivo  # função que verifica se o login está correto
import os
import main_interface  # módulo que contém a interface principal do sistema financeiro
import re  # biblioteca para validar Gmail

# para iniciar o sistema, digite no terminal do ambiente virtual (.venv):
# streamlit run interface.py

# verifica se o Gmail já está cadastrado no arquivo de usuários
def usuario_existe(nome_arquivo, gmail):
    if not os.path.exists(nome_arquivo):
        return False
    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        for linha in arquivo.readlines()[1:]:  # ignora cabeçalho
            dados = linha.strip().split(",")
            if len(dados) >= 4 and dados[2] == gmail:
                return True
    return False

# busca o nome do usuário com base no Gmail
def obter_nome_por_gmail(nome_arquivo, gmail):
    if not os.path.exists(nome_arquivo):
        return gmail
    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        for linha in arquivo.readlines()[1:]:
            partes = linha.strip().split(',')
            if len(partes) >= 4 and partes[2] == gmail:
                return partes[1]
    return gmail

# define título da aba do navegador
st.set_page_config(page_title="Sistema Financeiro")

# função para forçar recarregamento da página (usada após login)
def _st_rerun():
    try:
        st.rerun()  # versão atual do Streamlit
    except Exception:
        st.info('Por favor, atualize a página (F5) para continuar.')
        st.stop()

# se o usuário já está logado, mostra a interface principal
if 'usuario' in st.session_state and st.session_state['usuario']:
    usuario_logado = st.session_state['usuario']
    nome_usuario = obter_nome_por_gmail("usuarios.csv", usuario_logado)
    st.sidebar.markdown(f"**Logado como:** {nome_usuario}")

    if st.sidebar.button('Sair'):
        st.session_state['usuario'] = None
        _st_rerun()

    main_interface.inicia(usuario_logado)

# se não está logado, mostra tela de login ou criação de conta
else:
    st.title("Bem-vindo ao Sistema Financeiro")

    menu = st.radio("Escolha uma opção:", ["Criar Conta", "Fazer Login"])

    gmail = st.text_input("Gmail")
    senha = st.text_input("Senha", type="password")

    # Validação de email e senha
    def email_valido(gmail):
        return re.match(r"^[\w\.-]+@gmail\.com$", gmail)

    def senha_valida(senha):
        return len(senha) >= 6 and any(c in "#$_-" for c in senha)

    if menu == "Criar Conta":
        nome_conta = st.text_input("Nome de usuário")
        if st.button("Criar"):
            if not email_valido(gmail):
                st.error("Digite um Gmail válido (ex: usuario@gmail.com)")
            elif usuario_existe("usuarios.csv", gmail):
                st.error("Esse Gmail já está cadastrado. Escolha outro.")
            elif not nome_conta.strip():
                st.error("Digite um nome de usuário.")
            elif not senha_valida(senha):
                st.error("A senha deve ter pelo menos 6 caracteres e conter um dos símbolos #, $, _, -.")
            else:
                criar_conta("usuarios.csv", nome_conta=nome_conta, gmail=gmail, senha=senha)
                st.success("Conta criada com sucesso!")

    elif menu == "Fazer Login":
        if st.button("Entrar"):
            autenticado = login_usuario_arquivo("usuarios.csv", gmail, senha)
            if autenticado:
                st.session_state['usuario'] = gmail
                _st_rerun()
            else:
                st.error("Login falhou. Verifique Gmail e senha.")