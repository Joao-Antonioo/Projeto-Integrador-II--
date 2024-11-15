import streamlit as st
import ollama

class ChatBot:
    def __init__(self):
        self.desiredModel = 'llama3.2:3b'  # Certifique-se de que este modelo está disponível

    @staticmethod
    def extract_response_text(response):
        if isinstance(response, dict):
            return response.get('response', '')
        elif hasattr(response, '__iter__'):
            text = ''
            for item in response:
                if isinstance(item, dict) and 'response' in item:
                    text += item['response']
                else:
                    text += str(item)
            return text
        else:
            return str(response)

    def handle_chat(self):
        st.title("Fale com nossa IA 🤖")
        st.markdown("Converse com nossa inteligência artificial para tirar suas dúvidas ou obter conselhos!")

        # Inicializar o histórico de conversas
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []

        # Exibir o histórico de mensagens
        for message in st.session_state['chat_history']:
            if message['role'] == 'user':
                with st.chat_message("user"):
                    st.write(message['content'])
            else:
                with st.chat_message("assistant"):
                    st.write(message['content'])

        # Entrada de mensagem usando st.chat_input
        user_input = st.chat_input("Digite sua mensagem:")
        if user_input:
            # Adicionar a mensagem do usuário ao histórico
            st.session_state['chat_history'].append({'role': 'user', 'content': user_input})
            with st.chat_message("user"):
                st.write(user_input)

            # Construir o prompt a partir do histórico de forma estruturada
            prompt = "Você é um assistente de inteligência artificial amigável e prestativo. Responda às perguntas do usuário de forma clara e concisa.\n\n"
            for message in st.session_state['chat_history']:
                if message['role'] == 'user':
                    prompt += f"Usuário: {message['content']}\n"
                else:
                    prompt += f"Assistente: {message['content']}\n"
            prompt += "Assistente:"

            # Enviar o prompt ao modelo
            with st.chat_message("assistant"):
                with st.spinner("Pensando..."):
                    try:
                        response_generator = ollama.generate(model=self.desiredModel, prompt=prompt)
                        resposta_ia = self.extract_response_text(response_generator)
                        if resposta_ia:
                            # Adicionar a resposta da IA ao histórico
                            st.session_state['chat_history'].append({'role': 'assistant', 'content': resposta_ia})
                            st.write(resposta_ia)
                        else:
                            st.error("Não foi possível obter a resposta da IA.")
                    except Exception as e:
                        st.error(f"Erro ao obter a resposta da IA: {e}")

            # Limitar o histórico para evitar excesso de tokens
            if len(st.session_state['chat_history']) > 10:
                st.session_state['chat_history'] = st.session_state['chat_history'][-10:]

        # Botão para limpar a conversa
        if st.button("Limpar Conversa"):
            st.session_state['chat_history'] = []
            st.success("Conversa limpa.")
