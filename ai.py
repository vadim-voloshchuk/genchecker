import streamlit as st
import textwrap
import os
import docx
import google.generativeai as genai
from google.generativeai import GenerativeModel
import cohere

class TextGenerator:
    def __init__(self, google_api_key, cohere_api_key):
        genai.configure(api_key=google_api_key)
        self.google_api_key = google_api_key
        self.cohere_client = cohere.Client(api_key=cohere_api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')

    def generate_text(self, main_text, readme_text, source_text):
        context = f"{readme_text}\n#Target:\n{source_text}"
        messages = [{'role': 'user', 'parts': context}]
        response = self.model.generate_content(messages)
        response_cohere = self.cohere_client.chat(message=context)
        return response.text, response_cohere.text

    @staticmethod
    def get_text_from_docx(filename):
        try:
            doc = docx.Document(filename)
            return '\n'.join([para.text for para in doc.paragraphs])
        except FileNotFoundError:
            return "Файл не найден."

def main():
    st.title("Генератор текста")

    page = st.sidebar.selectbox("Выберите страницу", ["Главная", "Загрузка изображений"])

    if page == "Главная":
        data = open("data/инструкция.txt", 'r', encoding="utf-8").read()

        st.subheader("Текст, который надо переписать:")
        source_text = st.text_area("Сгенерированный вариант:", height=200)

        if st.button("Сгенерировать"):
            with st.spinner("Обработка текста..."):            
                generator = TextGenerator(
                    "AIzaSyA-ndk8GaYzCbYk1KnZkjrFpQOoMPes2gk",
                    "xa88h1He5s7PhBTMcnyCsaOiL6uIsB0rtMQjqW3k"
                )
                generated_text, coheregenerated_text = generator.generate_text("NONE", data, source_text)
                col1,col2 = st.columns(2)

                with col1:
                    st.write(generated_text)
                
                with col2:
                    st.write(coheregenerated_text)
                st.success("Готово!!!")

    elif page == "Загрузка изображений":
        st.subheader("Загрузите изображение:")
        uploaded_file = st.file_uploader("Выберите файл", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image.")

if __name__ == "__main__":
    main()
