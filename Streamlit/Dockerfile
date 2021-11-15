FROM python:3.7-slim

RUN mkdir /app

COPY requirements.txt /app
COPY /src /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "main.py"]
