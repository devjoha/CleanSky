# CleanSky

**From EarthData to Action — Cleaner, Safer Skies**

CleanSky is an interactive web application that provides real-time air quality and weather information for any location worldwide. Click anywhere on the map to instantly view air quality measurements, weather conditions, and 14-day forecasts.

![CleanSky Interface](https://img.shields.io/badge/Status-Active-success?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.12+-blue?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## Features

### 🌫️ Real-Time Air Quality Data

* **PM2.5, PM10, NO₂** measurements from global monitoring stations
* **AQI (Air Quality Index)** calculation with color-coded health indicators
* **Health Recommendations** based on current air quality levels
* Location-based data powered by Open-Meteo Air Quality API

### ☀️ Weather & Forecasting

* **Current weather conditions** including temperature and wind speed
* **14-day temperature forecast** with interactive charts
* **Precipitation data** for planning outdoor activities

### 🗺️ Interactive Map Interface

* **Click anywhere** on the map to set your location
* **Automatic location detection** with geolocation support
* **Reverse geocoding** to display city and country names
* **Marker on click** so you can see exactly where you selected

---

## Technologies Used

### Backend

* **FastAPI** - Modern Python web framework for APIs
* **Uvicorn** - ASGI server for production-ready deployment
* **Requests** - HTTP library for external API calls

### Frontend

* **Leaflet.js** - Interactive mapping library
* **Chart.js** - Beautiful data visualization
* **Tailwind CSS** - Utility-first CSS framework
* **Vanilla JavaScript** - Lightweight, no heavy frameworks

### External APIs (All Free, No Authentication Required)

* **Open-Meteo Air Quality API** - Real-time air quality data
* **Open-Meteo Weather API** - Weather and forecast data
* **Nominatim/OpenStreetMap** - Reverse geocoding for location names

---

## Installation & Setup

### Prerequisites

* Python 3.12 or higher
* [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Quick Start

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd CleanSky
   ```

2. **Install dependencies**

   #### Option 1 — Using uv (recommended)

   ```bash
   uv sync
   ```

   #### Option 2 — Using pip

   ```bash
   pip install -r requirements.txt
   ```

3. **Activate virtual environment** (important!)

   ```bash
   source .venv/bin/activate   # Linux / macOS
   .venv\Scripts\activate      # Windows PowerShell
   ```

4. **Run the application with Uvicorn**

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   > ⚠️ Do not run `python main.py` directly — FastAPI apps need to be served with **uvicorn**.

5. **Open your browser**

   ```
   http://localhost:8000
   ```

---

## Project Structure

```
CleanSky/
├── main.py              # FastAPI backend server
├── static/
│   └── index.html       # Single-page frontend application
├── pyproject.toml       # Python dependencies (for uv)
├── requirements.txt     # Fallback dependencies (for pip)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

---

## Usage

* Default location: **Tashkent, Uzbekistan**
* Click anywhere on the map to fetch air quality & weather for that point
* Use "📍 Use My Location" to detect your position
* AQI widget updates with color-coded status and health recommendations

---
---

## Troubleshooting

* **`ModuleNotFoundError: No module named 'fastapi'`**
  → You forgot to activate the virtual environment. Run:

  ```bash
  source .venv/bin/activate   # Linux / macOS
  .venv\Scripts\activate      # Windows
  ```

* **`pip` or `uv` not recognized**

  * Make sure Python is installed and added to your PATH.
  * On Linux/macOS you can try:

    ```bash
    python3 -m pip install -r requirements.txt
    ```
  * On Windows you can try:

    ```powershell
    py -m pip install -r requirements.txt
    ```
  * For uv installation, follow: [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)

* **Blank page**
  → Make sure you’re visiting `http://localhost:8000` (not `5000`).

* **Still doesn’t work?**
  Try reinstalling dependencies:

  ```bash
  rm -rf .venv
  uv sync
  ```

  or

  ```bash
  pip install --upgrade pip setuptools wheel
  pip install -r requirements.txt
  ```

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Made with ❤️ for cleaner air and healthier communities**
