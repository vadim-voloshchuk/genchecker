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

    def get_gemini_model(self):
        for m in GenerativeModel.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return GenerativeModel(m.name, api_key=self.google_api_key)
        return None

    def get_text_from_docx(self, filename):
        doc = docx.Document(filename)
        return '\n'.join([para.text for para in doc.paragraphs])

    def process_files(self, source_dir, output_dir):
        readme_text = textwrap.dedent(open('инструкция.txt', 'r', encoding="utf-8").read())
        main_text = self.get_text_from_docx("Гибкие методологии Управление IT-проектами 29 апреля 1.docx")

        warning_pieces = os.listdir(source_dir)
        for raw_log in warning_pieces:
            piece_problem = open(f"{source_dir}/{raw_log}", 'r', encoding="utf-8").read()
            messages = [
                {
                    'role': 'user',
                    'parts': f"""
                    {readme_text}

                    Общий контекст:
                    {main_text}

                    Сгенерированный фрагмент:
                    {piece_problem}
                    """
                }
            ]

            response = self.model.generate_content(messages)
            output_file = open(f"{output_dir}/{raw_log}", 'w', encoding="utf-8")
            output_file.write(response.text)
            output_file.close()

    def generate_text(self, main_text, readme_text, source_text):
        context = f"{readme_text}\n#Target:\n{source_text}"
        messages = [
            {
                'role': 'user',
                'parts': context
            }
        ]
        response = self.model.generate_content(messages)
        responsecohere = "NONE"
        return response.text, responsecohere

def get_text_from_docx(filename):
    try:
        doc = docx.Document(filename)
        return '\n'.join([para.text for para in doc.paragraphs])
    except FileNotFoundError:
        return "Файл не найден."
    
def get_readme_text(filename_or_content):
    try:
        if isinstance(filename_or_content, str):
            with open(filename_or_content, 'r', encoding="utf-8") as file:
                return file.read()
        else:
            return filename_or_content.getvalue().decode("utf-8")
    except FileNotFoundError:
        return "Файл не найден."

def main():
    st.title("Генератор текста")

    data =  open("data/инструкция.txt", 'r', encoding="utf-8").read()
    st.write(data)

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

if __name__ == "__main__":
    main()
