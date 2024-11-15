import streamlit as st
from DatabaseManager import DatabaseManager
from Auth import Auth
from DietGenerator import DietGenerator
from TrainingPlanGenerator import TrainingPlanGenerator
from ChatBot import ChatBot
from UI import UI

class NutriProApp:
    def __init__(self):
        self.db = DatabaseManager()
        self.auth = Auth(self.db)
        self.diet_gen = DietGenerator()
        self.training_gen = TrainingPlanGenerator()
        self.chatbot = ChatBot()
        self.ui = UI(
            self.db, 
            self.auth, 
            self.diet_gen, 
            self.training_gen, 
            self.chatbot
        )

    def run(self):
        # Configuração inicial do Streamlit
        st.set_page_config(
            page_title="NutriPro: Saúde e Bem-Estar Integrados",
            page_icon="🍎",
            layout="wide"
        )
        self.ui.style_css()
        self.ui.main_interface()