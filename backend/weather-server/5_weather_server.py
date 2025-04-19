import os
from fastapi import FastAPI, HTTPException, Request
from openweather_api import OpenWeather

app = FastAPI()

# Initialize OpenWeather client
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', '6b0b649e44a49690efe1b52931cd09d6')
weather_client = OpenWeather(api_key=OPENWEATHER_API_KEY)

@app.post("/query-weather")
async def query_weather(request: Request):
    """
    Handle weather queries from the user.
    :return: JSON response with weather information.
    """
    data = await request.json()
    query = data.get("query", "")
    
    # Extract location from query
    location = extract_location_from_query(query)
    if not location:
        raise HTTPException(status_code=400, detail="Please specify a location for the weather query.")
    
    # Fetch and format weather data
    try:
        weather_data = weather_client.get_current_weather(location)
        response = format_weather_response(weather_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching weather data: {str(e)}")
    
    return {"response": response}

def format_weather_response(weather_data):
    """
    Format the weather data into a user-friendly response.
    :param weather_data: The weather data from OpenWeather API.
    :return: Formatted weather response as a string.
    """
    if not weather_data:
        return "Sorry, I could not retrieve the weather information."
    
    name = weather_data.get("name")
    description = weather_data.get("weather", [{}])[0].get("description", "unknown")
    temp = weather_data.get("main", {}).get("temp", "unknown")
    
    return f"The weather in {name} is currently {description} with a temperature of {temp}°C."

def extract_location_from_query(query):
    """
    Extract location from the user query.
    :param query: The user query string.
    :return: Extracted location or None if not found.
    """
    if "weather in" in query.lower():
        return query.lower().split("weather in")[-1].strip()
    return None
