# CleanSky

**From EarthData to Action — Cleaner, Safer Skies**

CleanSky is an interactive web application that provides real-time air quality and weather information for any location worldwide. Click anywhere on the map to instantly view air quality measurements, weather conditions, and 14-day forecasts.

![CleanSky Interface](https://img.shields.io/badge/Status-Active-success?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.12+-blue?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

## Features

### 🌫️ Real-Time Air Quality Data
- **PM2.5, PM10, NO₂** measurements from global monitoring stations
- **AQI (Air Quality Index)** calculation with color-coded health indicators
- **Health Recommendations** based on current air quality levels
- Location-based data powered by Open-Meteo Air Quality API

### ☀️ Weather & Forecasting
- **Current weather conditions** including temperature and wind speed
- **14-day temperature forecast** with interactive charts
- **Precipitation data** for planning outdoor activities

### 🗺️ Interactive Map Interface
- **Click anywhere** on the map to set your location
- **Color-coded station markers** showing air quality levels
- **Automatic location detection** with geolocation support
- **Reverse geocoding** to display city and country names

## Technologies Used

### Backend
- **FastAPI** - Modern Python web framework for APIs
- **Uvicorn** - ASGI server for production-ready deployment
- **Requests** - HTTP library for external API calls

### Frontend
- **Leaflet.js** - Interactive mapping library
- **Chart.js** - Beautiful data visualization
- **Tailwind CSS** - Utility-first CSS framework
- **Vanilla JavaScript** - No heavy frameworks needed

### External APIs (All Free, No Authentication Required)
- **Open-Meteo Air Quality API** - Real-time air quality data
- **Open-Meteo Weather API** - Weather and forecast data
- **Nominatim/OpenStreetMap** - Reverse geocoding for location names

## Installation & Setup

### Prerequisites
- Python 3.12 or higher
- pip (Python package manager)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd CleanSky
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or using uv (recommended):
   ```bash
   uv sync
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Open your browser**
   ```
   http://localhost:5000
   ```

That's it! No API keys or configuration needed.

## Project Structure

```
cleansky/
├── main.py              # FastAPI backend server
├── static/
│   └── index.html       # Single-page frontend application
├── pyproject.toml       # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Usage

### Basic Usage
1. **View Default Location**: The app loads with Tashkent, Uzbekistan as the default location
2. **Click the Map**: Click anywhere on the map to view air quality for that location
3. **Use Your Location**: Click "Use My Location" to automatically detect your position
4. **Explore Data**: View PM2.5, PM10, NO₂ levels, AQI, and weather forecasts

### Understanding Air Quality Index (AQI)

| AQI Range | Level | Color | Health Recommendation |
|-----------|-------|-------|----------------------|
| 0-60 | Good | 🟢 Green | Air quality is good - enjoy outdoor activities |
| 61-100 | Moderate | 🟡 Yellow | Limit prolonged outdoor exertion |
| 101-150 | Unhealthy | 🟠 Orange | Sensitive groups should limit time outside |
| 151+ | Very Unhealthy | 🔴 Red | Avoid outdoor activity |

## Development

### Running in Development Mode

```bash
python main.py
```

The server will start on `http://0.0.0.0:5000` with auto-reload enabled.

### API Endpoints

- `GET /air-quality?lat={lat}&lon={lon}` - Get air quality data for coordinates
- `GET /weather?lat={lat}&lon={lon}` - Get current weather conditions
- `GET /forecast?lat={lat}&lon={lon}&days={days}` - Get weather forecast

### Example API Response

```json
{
  "aggregated": {
    "pm25": 10.0,
    "pm10": 11.5,
    "no2": 6.0
  },
  "last_updated": "2025-10-05T17:30:00Z",
  "locations": [
    {
      "location": "Air Quality Station (41.31, 69.28)",
      "coordinates": {
        "latitude": 41.3111,
        "longitude": 69.2797
      },
      "measurements": {
        "pm25": 10.0,
        "pm10": 11.5,
        "no2": 6.0
      }
    }
  ]
}
```

## Deployment

### Deploy on Replit
This project is optimized for Replit deployment:
1. Import the repository to Replit
2. Click "Run" - it's already configured!
3. Share your deployment URL with others

### Deploy on Other Platforms

**Using Uvicorn:**
```bash
uvicorn main:app --host 0.0.0.0 --port 5000
```

**Using Docker:**
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

## Configuration

### Environment Variables
No environment variables or API keys are required! All APIs used are completely free and open.

### Customization
- **Default Location**: Edit `DEFAULT` object in `static/index.html` (line 171)
- **Map Tiles**: Change the Leaflet tile provider in `static/index.html` (line 179)
- **AQI Calculation**: Modify the AQI formula in `static/index.html` (line 313)

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Known Limitations

- Air quality data resolution varies by location (11km for Europe, 40km globally)
- Historical air quality data is not available through the current API
- Map requires internet connection for tile loading

## Roadmap

- [ ] Add historical air quality trend graphs
- [ ] Compare multiple locations side-by-side
- [ ] Email/SMS alerts for poor air quality
- [ ] Mobile app version
- [ ] Offline mode with cached data

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **Open-Meteo** for providing free, open-source weather and air quality APIs
- **OpenStreetMap** contributors for mapping data
- **Leaflet.js** for the excellent mapping library
- **Chart.js** for data visualization tools

## Support

If you find this project helpful, please consider:
- Starring the repository ⭐
- Sharing it with others
- Contributing improvements

---

**Made with ❤️ for cleaner air and healthier communities**
