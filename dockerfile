FROM python:3.10-slim

COPY req.txt req.txt
RUN pip install --no-cache-dir -r req.txt

RUN pip install --no-cache-dir streamlit

WORKDIR /app

COPY . /app

# Указываем команду для запуска приложения Streamlit
CMD ["streamlit", "run", "ai.py"]
