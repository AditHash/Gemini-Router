import os
import requests
from fastapi import FastAPI, HTTPException, Request
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load OpenWeather API key
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', '6b0b649e44a49690efe1b52931cd09d6')
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.post("/query-weather")
async def query_weather(request: Request):
    """
    Handle weather queries from the user.
    :return: JSON response with weather information.
    """
    try:
        data = await request.json()
        logger.info(f"Received request payload: {data}")
    except Exception as e:
        logger.error(f"Failed to parse request payload: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON payload.")
    
    query = data.get("query", "").strip()
    if not query:
        logger.warning("Missing 'query' field in the request payload.")
        raise HTTPException(status_code=400, detail="Please specify a location for the weather query.")
    
    # Extract location from query
    location = extract_location_from_query(query)
    if not location:
        logger.warning(f"Could not extract location from query: {query}")
        raise HTTPException(status_code=400, detail="Could not extract location from the query.")
    
    logger.info(f"Extracted location: {location}")
    
    # Fetch and format weather data
    try:
        response = requests.get(OPENWEATHER_BASE_URL, params={
            "q": location,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        })
        response.raise_for_status()
        weather_data = response.json()
        formatted_response = format_weather_response(weather_data)
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        raise HTTPException(status_code=500, detail="Failed to fetch weather data from OpenWeather API.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing the request.")
    
    return {"response": formatted_response}

def format_weather_response(weather_data):
    """
    Format the weather data into a user-friendly response.
    """
    name = weather_data.get("name", "unknown location")
    description = weather_data.get("weather", [{}])[0].get("description", "unknown").capitalize()
    temp = weather_data.get("main", {}).get("temp", "unknown")
    feels_like = weather_data.get("main", {}).get("feels_like", "unknown")
    humidity = weather_data.get("main", {}).get("humidity", "unknown")
    return (
        f"The weather in {name} is currently {description} with a temperature of {temp}°C. "
        f"It feels like {feels_like}°C with a humidity level of {humidity}%."
    )

def extract_location_from_query(query):
    """
    Extract location from the user query.
    """
    query = query.lower().strip()
    # Handle queries like "What is the weather in Kolkata?"
    if "weather in" in query:
        return query.split("weather in")[-1].strip()
    # Handle queries like "Kolkata weather" or "Kolkata"
    if "weather" in query:
        return query.replace("weather", "").strip()
    # If the query is a single word or direct location name
    return query if query else None
