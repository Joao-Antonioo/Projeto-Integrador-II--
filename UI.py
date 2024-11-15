import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from streamlit_option_menu import option_menu
from DatabaseManager import DatabaseManager
from Auth import Auth
from DietGenerator import DietGenerator
from TrainingPlanGenerator import TrainingPlanGenerator
from ChatBot import ChatBot


class UI:
    def __init__(self, db: DatabaseManager, auth: Auth, diet_gen: DietGenerator, training_gen: TrainingPlanGenerator, chatbot: ChatBot):
        self.db = db
        self.auth = auth
        self.diet_gen = diet_gen
        self.training_gen = training_gen
        self.chatbot = chatbot

    def style_css(self):
        st.markdown("""
            <style>
            .big-font {font-size:30px !important; font-weight: bold;}
            .medium-font {font-size:20px !important;}
            .small-font {font-size:14px !important;}
            .highlight {background-color: #f9f9f9; padding: 20px; border-radius: 10px;}
            .stButton>button {width: 100%;}
            .stChatMessage {padding: 10px; border-radius: 10px; margin-bottom: 10px;}
            .stChatMessageUser {background-color: #DCF8C6;}
            .stChatMessageAssistant {background-color: #E5E5EA;}
            </style>
        """, unsafe_allow_html=True)

    def show_main_menu(self):
        with st.sidebar:
            st.image("https://via.placeholder.com/150x150.png?text=NutriPro", width=150)
            if 'name' in st.session_state:
                st.markdown(f"**Bem-vindo, {st.session_state['name']}!**")
            escolha = option_menu(
                "Menu Principal", 
                ["Início", "IMC & Dieta", "Treino com IA", "Histórico", "Fale com nossa IA", "Sobre", "Sair"],
                icons=['house', 'calculator', 'dumbbell', 'clock-history', 'chat-dots', 'info-circle', 'box-arrow-right'],
                menu_icon="cast", 
                default_index=0
            )

            if escolha == "Início":
                self.pagina_inicial()
            elif escolha == "IMC & Dieta":
                self.imc_e_dieta()
            elif escolha == "Treino com IA":
                self.treino_com_ia()
            elif escolha == "Histórico":
                self.historico()
            elif escolha == "Fale com nossa IA":
                self.chatbot.handle_chat()
            elif escolha == "Sobre":
                self.sobre()
            elif escolha == "Sair":
                # Logout
                st.session_state['logged_in'] = False
                st.session_state.pop('user_id', None)
                st.session_state.pop('username', None)
                st.session_state.pop('name', None)
                st.success("Você saiu da sua conta.")

    def main_interface(self):
        if 'logged_in' not in st.session_state:
            st.session_state['logged_in'] = False

        if st.session_state['logged_in']:
            self.show_main_menu()
        else:
            menu = ["Login", "Cadastrar"]
            choice = st.sidebar.selectbox("Menu", menu)
            if choice == "Login":
                self.auth.login()
            elif choice == "Cadastrar":
                self.auth.signup()

    def pagina_inicial(self):
        st.title(f"Bem-vindo ao NutriPro, {st.session_state['name']} 👋")
        st.markdown("<p class='big-font'>Seu assistente integrado de saúde e bem-estar</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='highlight'>", unsafe_allow_html=True)
            st.markdown("<p class='medium-font'>O que oferecemos:</p>", unsafe_allow_html=True)
            st.markdown("""
                - 📊 Cálculo preciso de IMC
                - 📋 Análise detalhada do seu estado de saúde
                - 🥗 Planos de dieta personalizados instantâneos
                - 💪 Planos de treino personalizados
                - 📈 Acompanhamento do seu progresso
                - 🤖 Chatbot inteligente para tirar suas dúvidas
            """)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.image("https://via.placeholder.com/400x300.png?text=Healthy+Lifestyle", width=400)

        st.markdown("---")
        st.markdown(f"<p class='medium-font'>Comece sua jornada para uma vida mais saudável hoje mesmo!</p>", unsafe_allow_html=True)

    def imc_e_dieta(self):
        st.title("Calculadora de IMC e Plano de Dieta Integrados")
        col1, col2 = st.columns([2,1])
        
        with col1:
            st.markdown("<div class='highlight'>", unsafe_allow_html=True)
            st.markdown("<p class='medium-font'>Insira seus dados:</p>", unsafe_allow_html=True)
            
            peso = st.number_input("Peso (kg)", min_value=30.0, max_value=300.0, value=70.0, step=0.1)
            altura = st.number_input("Altura (m)", min_value=1.0, max_value=2.5, value=1.70, step=0.01)
            sexo = st.selectbox("Sexo", ["Masculino", "Feminino", "Outro"])
            idade = st.number_input("Idade", min_value=1, max_value=120, value=30, step=1)
            objetivo = st.selectbox("Seu objetivo", ["Perder peso", "Ganhar massa muscular", "Manter peso"])

            if st.button("Calcular IMC e Gerar Dieta"):
                with st.spinner("Calculando IMC e gerando seu plano personalizado..."):
                    imc, categoria = self.diet_gen.calcular_imc(peso, altura)
                    dieta = self.diet_gen.gerar_dieta_traduzida(imc, objetivo, sexo, idade)
                    st.success("IMC calculado e plano de dieta gerado com sucesso!")

                    # Exibir IMC
                    if imc is not None:
                        st.markdown(f"<p class='big-font'>Seu IMC é: {imc:.2f}</p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p class='big-font'>Seu IMC é: N/A</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='medium-font'>Categoria: {categoria}</p>", unsafe_allow_html=True)

                    # Gráfico do IMC
                    if imc is not None:
                        fig = go.Figure(go.Indicator(
                            mode = "gauge+number",
                            value = imc,
                            domain = {'x': [0, 1], 'y': [0, 1]},
                            title = {'text': "IMC", 'font': {'size': 24}},
                            gauge = {
                                'axis': {'range': [None, 40], 'tickwidth': 1, 'tickcolor': "darkblue"},
                                'bar': {'color': "darkblue"},
                                'bgcolor': "white",
                                'borderwidth': 2,
                                'bordercolor': "gray",
                                'steps': [
                                    {'range': [0, 18.5], 'color': 'cyan'},
                                    {'range': [18.5, 25], 'color': 'royalblue'},
                                    {'range': [25, 30], 'color': 'orange'},
                                    {'range': [30, 40], 'color': 'red'}
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': imc
                                }
                            }
                        ))
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.write("Gráfico do IMC não disponível.")

                    # Exibir Dieta
                    st.markdown("<p class='medium-font'>Seu Plano de Dieta Personalizado:</p>", unsafe_allow_html=True)
                    if dieta:
                        st.markdown(dieta, unsafe_allow_html=True)
                    else:
                        st.error("Não foi possível gerar a dieta.")

                    # Salvar no banco de dados
                    self.db.execute_query(
                        "INSERT INTO historico (user_id, data, peso, altura, imc, categoria, objetivo, sexo, idade, dieta) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (st.session_state['user_id'], datetime.now().strftime("%Y-%m-%d %H:%M:%S"), peso, altura, imc, categoria, objetivo, sexo, idade, dieta)
                    )

            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='highlight'>", unsafe_allow_html=True)
            st.markdown("<p class='medium-font'>Interpretação do IMC:</p>", unsafe_allow_html=True)
            st.markdown("""
                - **Abaixo de 18.5**: Abaixo do peso
                - **18.5 - 24.9**: Peso normal
                - **25.0 - 29.9**: Sobrepeso
                - **30.0 ou mais**: Obesidade
            """)
            st.image("https://via.placeholder.com/300x200.png?text=IMC+Chart", width=300)

            st.markdown("<p class='medium-font'>Dicas para uma dieta equilibrada:</p>", unsafe_allow_html=True)
            st.markdown("""
                1. Priorize alimentos integrais
                2. Inclua proteínas magras em todas as refeições
                3. Consuma frutas e vegetais variados
                4. Beba água regularmente
                5. Evite alimentos processados e açúcares refinados
            """)
            st.markdown("</div>", unsafe_allow_html=True)

    # Rest of the methods follow the same indentation pattern...