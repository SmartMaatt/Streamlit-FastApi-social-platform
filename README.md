<h1 align="center">Streamlit FastAPI Social Platform</h1>

<p align="center">
  <a href="#overview">Overview</a> •
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#license">License</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  <img src="https://img.shields.io/badge/Author-SmartMatt-blue" />
</p>

## Overview
This repository contains a social platform application with a frontend built using Streamlit and a backend using FastAPI, integrated with a Firebase database. The platform is designed to facilitate simple communication between the Streamlit system and the database through an API and to test the capabilities of Streamlit, which is known for its somewhat limited features.

## Features
- **Streamlit Frontend**: A user-friendly interface for interacting with the platform.
- **FastAPI Backend**: Robust API for efficient server-side processing.
- **Firebase Database Integration**: Cloud-based database for secure and scalable data storage.

## Installation
The entire setup is containerized using Docker Compose, ensuring easy and consistent deployment.

### Prerequisites
- Docker
- Docker Compose

### Setup Instructions
1. **FastAPI Container Setup**:
   ```bash
   cd Fastapi
   docker build -t fastapi .
   docker run -d --name fastapi -p 8000:8000 fastapi
   ```

2. **Streamlit Container Setup**:
   ```bash
   cd Streamlit
   docker build -t streamlit .
   docker run -d --name streamlit -p 8501:8501 streamlit
   ```

3. **Docker Compose**:
   ```bash
   docker-compose build
   docker-compose up
   ```

### Firebase Connection
To connect to Firebase:
1. Create a config.py file in the main directory of the Streamlit app.
2. Insert the firebaseConfig dictionary into config.py to establish a connection with the Firebase database.

## Usage
The main frontend file (main.py in the Streamlit app directory) demonstrates the usage of various components such as authentication, database interactions, and UI elements.

### Key Components:
* Firebase Authentication: User authentication via Firebase.
* Database Operations: CRUD operations with Firebase Realtime Database.
* Custom Component Builder: A utility for incorporating custom styles and scripts.\

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
&copy; 2023 Mateusz Płonka (SmartMatt). All rights reserved.
<a href="https://smartmatt.pl/">
    <img src="https://smartmatt.pl/github/smartmatt-logo.png" title="SmartMatt Logo" align="right" width="60" />
</a>

<p align="left">
  <a href="https://smartmatt.pl/">Portfolio</a> •
  <a href="https://github.com/SmartMaatt">GitHub</a> •
  <a href="https://www.linkedin.com/in/mateusz-p%C5%82onka-328a48214/">LinkedIn</a> •
  <a href="https://www.youtube.com/user/SmartHDesigner">YouTube</a> •
  <a href="https://www.tiktok.com/@smartmaatt">TikTok</a>
</p>
