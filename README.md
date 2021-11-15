# Docker Fastapi
cd Fastapi
docker build -t fastapi .
docker run -d --name fastapi -p 8000:8000 fastapi

# Docker Streamlit
cd Streamlit
docker build -t streamlit .
docker run -d --name streamlit -p 8501:8501 streamlit

# Docker compose
docker-compose build
docker-compose up

# Firebase connection
Create config.py file in main directory of Streamlit app then insert "firebaseConfig" dict into it to make connection with database work properly.
