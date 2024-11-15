import streamlit as st
import ollama

class DietGenerator:
    def __init__(self):
        pass

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

    def calcular_imc(self, peso, altura):
        try:
            imc = peso / (altura ** 2)
        except ZeroDivisionError:
            imc = None

        if imc is not None:
            if imc < 18.5:
                categoria = "Abaixo do peso"
            elif 18.5 <= imc < 25:
                categoria = "Peso normal"
            elif 25 <= imc < 30:
                categoria = "Sobrepeso"
            else:
                categoria = "Obesidade"
        else:
            categoria = "IMC Indefinido"
        return imc, categoria

    def gerar_dieta_traduzida(self, imc_atual, objetivo, sexo, idade):
        desiredModel = 'llama3.2:3b'  # Certifique-se de que este modelo está disponível

        # Mapear o objetivo para inglês
        objetivos_map = {
            "Perder peso": "lose weight",
            "Ganhar massa muscular": "gain muscle mass",
            "Manter peso": "maintain current weight"
        }
        objetivo_ingles = objetivos_map.get(objetivo, "maintain current weight")

        # Mapear o sexo para inglês
        sexo_map = {
            "Masculino": "male",
            "Feminino": "female",
            "Outro": "other"
        }
        sexo_ingles = sexo_map.get(sexo, "other")

        # Prompt para gerar a dieta em inglês
        prompt_dieta = f"""
        You are a professional nutritionist with expertise in creating personalized diet plans. Based on
        the following information, generate a comprehensive and detailed diet plan tailored to the user's needs:
        
        **User Details:**
        - **Age:** {idade} years
        - **Sex:** {sexo_ingles}
        - **Current BMI:** {imc_atual:.2f} if imc_atual else "N/A"
        - **Goal:** {objetivo_ingles}

        **Requirements:**
        1. **Meal Plan:** Provide specific food items and their quantities for each meal of the day,
        including breakfast, morning snack, lunch, afternoon snack, and dinner.
        2. **Nutritional Justification:** Explain why each food item is suitable for achieving the user's
        goal, considering their BMI and other relevant factors.
        3. **Meal Schedule:** Suggest optimal times for each meal to maximize metabolic efficiency
        and adherence to the diet.
        4. **Complementary Exercises:** Recommend exercises that complement the diet plan, taking
        into account the user's goal, physical condition, age, and sex.

        **Presentation:**
        - Organize the diet plan in a clear and professional format.
        - Use bullet points or tables where appropriate for better readability.
        Ensure the diet plan is balanced, sustainable, and tailored specifically to help the user achieve
        their health and fitness goals.
        """

        # Enviando o prompt para o modelo
        try:
            response = ollama.generate(model=desiredModel, prompt=prompt_dieta)
            dieta_em_ingles = self.extract_response_text(response)
        except Exception as e:
            st.error(f"Erro ao gerar a dieta em inglês: {e}")
            return None

        # Prompt para traduzir a dieta para o português
        prompt_traducao = f"""
        Traduza o seguinte plano de dieta para o português do Brasil de forma precisa e mantendo o
        formato profissional:
        {dieta_em_ingles}
        """

        try:
            response_traducao = ollama.generate(model=desiredModel, prompt=prompt_traducao)
            dieta_traduzida = self.extract_response_text(response_traducao)
        except Exception as e:
            st.error(f"Erro ao traduzir a dieta: {e}")
            return None

        return dieta_traduzida
