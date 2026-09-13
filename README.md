# 🌦️ SkyGuard AI – Real-Time Weather Anomaly Detection Platform

SkyGuard AI is an end-to-end AI-powered weather anomaly detection platform that monitors Automatic Weather Stations (AWS) in real time. The system analyzes live weather data using a Machine Learning model trained on historical NOAA weather records and detects abnormal weather conditions before they become critical.

Built using **React, FastAPI, PostgreSQL, Docker, and Scikit-learn**, SkyGuard AI demonstrates the complete lifecycle of an AI application—from data ingestion and model training to deployment, live prediction, visualization, and alerting.

---

# 🚀 Features

* 🌍 Real-time weather monitoring using OpenWeather API
* 🤖 AI-powered anomaly detection with Isolation Forest
* 📊 Interactive dashboard with weather trends and analytics
* 🛰️ Support for multiple weather stations
* ⏰ Automated background scheduler for periodic weather updates
* 🚨 Real-time anomaly alerts
* 📈 Prediction history with confidence scores
* 🐳 Dockerized backend with PostgreSQL
* 🔗 RESTful APIs built using FastAPI

---

# 🏗️ System Architecture

```text
                NOAA Historical Dataset
                        │
                        ▼
              Data Cleaning & Preprocessing
                        │
                        ▼
                 Isolation Forest Training
                        │
                        ▼
              Saved Model (.pkl + Scaler)
                        │
────────────────────────────────────────────────────

               OpenWeather Current API
                        │
                        ▼
               FastAPI Weather Service
                        │
                        ▼
             PostgreSQL Weather Database
                        │
                        ▼
             Machine Learning Prediction
                        │
                        ▼
            Prediction + Confidence Score
                        │
                        ▼
         React Dashboard + Alert Notifications
```

---

# 🧠 Machine Learning Pipeline

Historical weather data from the NOAA Integrated Surface Database (2023–2025) is used to train an Isolation Forest model.

### Features Used

* Temperature
* Humidity
* Pressure
* Wind Speed
* Wind Direction
* Visibility
* Month
* Hour

The trained model identifies weather readings that significantly deviate from historical patterns.

---

# ⚙️ Tech Stack

### Frontend

* React.js
* Tailwind CSS
* Axios
* Recharts

### Backend

* FastAPI
* SQLAlchemy
* APScheduler

### Machine Learning

* Python
* Scikit-learn
* Isolation Forest
* Pandas
* NumPy

### Database

* PostgreSQL

### External API

* OpenWeather API

### DevOps

* Docker
* Docker Compose
* Git
* GitHub

---

# 📂 Project Structure

```text
SkyGuard-AI/

├── backend/
│   ├── app/
│   ├── models/
│   ├── services/
│   ├── api/
│   ├── schemas/
│   └── main.py
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   └── layouts/
│

│
├── docker-compose.yml
├── README.md
└── requirements.txt
```

---

# 🔄 Workflow

1. Historical NOAA weather data is used to train the anomaly detection model.
2. The scheduler periodically fetches live weather from OpenWeather.
3. Weather readings are stored in PostgreSQL.
4. The trained Isolation Forest predicts whether the reading is **Normal** or **Anomalous**.
5. Predictions and confidence scores are saved.
6. The dashboard updates automatically with weather trends, prediction history, and alerts.

---

# 📸 Screenshots

Add screenshots here after uploading them.

* Dashboard
* Weather Page
* Prediction Page
* Station Management
* Alert Notifications

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/your-username/SkyGuard-AI.git
cd SkyGuard-AI
```

## Backend

```bash
cd backend

pip install -r requirements.txt

uvicorn app.main:app --reload
```

## Frontend

```bash
cd frontend

npm install

npm run dev
```

## Docker

```bash
docker compose up --build
```

---

# 📌 Future Enhancements

* Deploy to AWS/Azure
* Kubernetes deployment
* Email/SMS notifications
* Role-based authentication
* Advanced anomaly explanation using Explainable AI (XAI)
* Time-series forecasting integration (LSTM/Transformers)

---

# 📚 Dataset

* NOAA Integrated Surface Database (ISD)
* OpenWeather API (Live Weather)

---

# 👩‍💻 Author

**Akhila Uggina**

* LinkedIn: https://www.linkedin.com/in/akhila-uggina-499321312/
* GitHub: https://github.com/Akhilauggina

---

## ⭐ If you found this project interesting, consider giving it a star!
