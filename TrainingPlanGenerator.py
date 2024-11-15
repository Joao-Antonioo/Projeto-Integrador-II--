import streamlit as st
import ollama

class TrainingPlanGenerator:
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

    def gerar_treino_traduzido(self, objetivo, foco, tempo, idade, sexo, nivel_experiencia, equipamentos, limitacoes, altura, peso):
        desiredModel = 'llama3.2:3b'  # Certifique-se de que este modelo está disponível

        # Calcular IMC
        imc, _ = self.calcular_imc(peso, altura)

        # Mapear o objetivo para inglês
        objetivos_map = {
            "Perder peso": "lose weight",
            "Ganhar massa muscular": "gain muscle mass",
            "Melhorar condicionamento": "improve conditioning",
            "Aumentar flexibilidade": "increase flexibility",
            "Melhorar resistência": "improve endurance"
        }
        objetivo_ingles = objetivos_map.get(objetivo, "improve conditioning")

        # Mapear o foco para inglês
        foco_map = {
            "Braços": "arms",
            "Pernas": "legs",
            "Glúteos": "glutes",
            "Abdômen": "abdomen",
            "Peito": "chest",
            "Costas": "back",
            "Corpo inteiro": "full body"
        }
        foco_ingles = [foco_map.get(f, f) for f in foco]
        foco_ingles_str = ', '.join(foco_ingles) if foco_ingles else "full body"

        # Mapear sexo para inglês
        sexo_map = {
            "Masculino": "male",
            "Feminino": "female",
            "Outro": "other"
        }
        sexo_ingles = sexo_map.get(sexo, "other")

        # Mapear nível de experiência para inglês
        nivel_map = {
            "Iniciante": "beginner",
            "Intermediário": "intermediate",
            "Avançado": "advanced"
        }
        nivel_ingles = nivel_map.get(nivel_experiencia, "beginner")

        # Mapear equipamentos para inglês
        equipamentos_map = {
            "Nenhum": "none",
            "Pesos livres": "free weights",
            "Máquinas de musculação": "weight machines",
            "Elásticos": "resistance bands",
            "Bola de exercício": "exercise ball",
            "Esteira": "treadmill",
            "Bicicleta ergométrica": "stationary bike"
        }
        equipamentos_ingles = [equipamentos_map.get(e, e) for e in equipamentos]
        equipamentos_ingles_str = ', '.join(equipamentos_ingles) if equipamentos_ingles else "none"

        # Limitações
        limitacoes_str = limitacoes if limitacoes else "None"

        # Prompt para gerar o treino em inglês
        prompt_treino = f"""
        You are a professional fitness trainer with expertise in creating personalized workout plans. Based on the following user information, generate a comprehensive and detailed training plan tailored
        to the user's needs:

        **User Details:**
        - **Age:** {idade} years
        - **Sex:** {sexo_ingles}
        - **Height:** {altura} meters
        - **Weight:** {peso} kg
        - **BMI:** {imc:.2f} if imc else "N/A"
        - **Fitness Level:** {nivel_ingles}
        - **Goal:** {objetivo_ingles}
        - **Focus Areas:** {foco_ingles_str}
        - **Available Time Per Day:** {tempo} minutes
        - **Available Equipment:** {equipamentos_ingles_str}
        - **Injuries or Physical Limitations:** {limitacoes_str}

        **Requirements:**
        1. **Exercise Plan:** List specific exercises with the number of sets and repetitions suitable for
        the user's goal, focus areas, and fitness level.
        2. **Weekly Schedule:** Provide a weekly workout schedule distributing exercises appropriately across the 7 days.
        3. **Effectiveness Justification:** Explain why each exercise is effective in achieving the user's
        goal, considering their BMI and other relevant factors.
        4. **Safety and Form Tips:** Offer guidelines on proper form and safety precautions, especially
        considering any injuries or limitations.
        5. **Warm-Up and Cool-Down:** Include recommended warm-up and cool-down routines to
        prevent injuries and enhance performance.

        **Presentation:**
        - Organize the workout plan in a clear and professional format.
        - Use bullet points, numbered lists, or tables where appropriate for better readability.
        Ensure the training plan is balanced, achievable, and specifically tailored to help the user reach
        their health and fitness objectives.
        """

        # Enviando o prompt para o modelo
        try:
            response = ollama.generate(model=desiredModel, prompt=prompt_treino)
            treino_em_ingles = self.extract_response_text(response)
        except Exception as e:
            st.error(f"Erro ao gerar o treino em inglês: {e}")
            return None

        # Prompt para traduzir o treino para o português
        prompt_traducao = f"""
        Traduza o seguinte plano de treino para o português de forma precisa e mantendo o formato
        profissional:
        {treino_em_ingles}
        """

        try:
            response_traducao = ollama.generate(model=desiredModel, prompt=prompt_traducao)
            treino_traduzido = self.extract_response_text(response_traducao)
        except Exception as e:
            st.error(f"Erro ao traduzir o treino: {e}")
            return None

        return treino_traduzido
