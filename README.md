# 🍎 Smart Cold Storage Simulator

A hybrid **AI + IoT Simulation** project that detects fruit freshness using Deep Learning and simulates cold storage conditions to provide real-time preservation advice.

## 🚀 Overview
This application solves the problem of food wastage in cold chains. It uses:
1.  **Computer Vision (TensorFlow):** To classify fruits as "Fresh" or "Rotten" from an image.
2.  **IoT Simulation (Streamlit):** To simulate temperature and humidity sensors using interactive sliders.
3.  **Smart Logic:** Combines the visual analysis with storage conditions to generate actionable alerts (e.g., "Fruit is fresh, but temperature is too high!").

## ✨ Features
* **Image Classification:** Upload an image of an apple or banana to detect its quality.
* **Real-time IoT Simulation:** Adjust storage parameters (Temp/Humidity) to test different scenarios.
* **Smart Alerts:**
    * ✅ **Safe:** Fresh fruit + Ideal Temp.
    * ⚠️ **Danger:** Fresh fruit + High Temp (Risk of rotting).
    * ⛔ **Discard:** Rotten fruit detected (Temp control irrelevant).
* **Confidence Score:** Displays the AI model's certainty percentage.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Frontend:** Streamlit
* **AI/ML:** TensorFlow, Keras
* **Image Processing:** Pillow (PIL), NumPy

