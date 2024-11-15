import streamlit as st
import hashlib
from DatabaseManager import DatabaseManager


class Auth:
    def __init__(self, db: DatabaseManager):
        self.db = db

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def signup(self):
        st.title("Criar Nova Conta")
        
        # Campos para o cadastro do usuário
        name = st.text_input("Nome", key='signup_name')
        email = st.text_input("Email", key='signup_email')
        username = st.text_input("Nome de Usuário", key='signup_username')
        password = st.text_input("Senha", type="password", key='signup_password')
        confirm_password = st.text_input("Confirme a Senha", type="password", key='signup_confirm_password')
        
        # Botão para confirmar o cadastro
        if st.button("Cadastrar"):
            if password != confirm_password:
                st.error("As senhas não coincidem.")
            else:
                # Verificar se o username ou email já existe no banco de dados
                user = self.db.fetch_one("SELECT * FROM users WHERE username=? OR email=?", (username, email))
                if user:
                    st.error("Nome de usuário ou email já estão em uso.")
                else:
                    # Criptografar a senha e cadastrar o usuário
                    hashed_password = self.hash_password(password)
                    self.db.execute_query(
                        "INSERT INTO users (name, email, username, password) VALUES (?, ?, ?, ?)",
                        (name, email, username, hashed_password)
                    )
                    st.success("Conta criada com sucesso! Agora você pode fazer login.")

    def login(self):
        st.title("Login")
        
        # Campos de entrada para o login
        username = st.text_input("Nome de Usuário", key='login_username')
        password = st.text_input("Senha", type="password", key='login_password')
        
        # Botão para realizar o login
        if st.button("Entrar"):
            # Buscar o usuário no banco de dados
            user = self.db.fetch_one("SELECT * FROM users WHERE username=?", (username,))
            if user:
                # Verificar se a senha corresponde à armazenada
                hashed_password = user[4]
                if self.hash_password(password) == hashed_password:
                    st.success(f"Bem-vindo, {user[1]}!")
                    # Guardar informações do usuário na sessão
                    st.session_state['logged_in'] = True
                    st.session_state['user_id'] = user[0]
                    st.session_state['username'] = user[3]
                    st.session_state['name'] = user[1]
                else:
                    st.error("Senha incorreta.")
            else:
                st.error("Usuário não encontrado.")
