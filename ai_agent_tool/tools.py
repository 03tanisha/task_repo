
# functions for weather of delhi

def get_weather(city: str):
    weather_data = {
        "delhi": {
            "temperature": 26,
            "condition": "sunny"
        },
        "mumbai": {
            "temperature": 30,
            "condition": "cloudy"
        },
        "jaipur": {
            "temperature": 32,
            "condition": "sunny"
        }
    }

    city = city.strip().lower()

    if city in weather_data:
        return {
            "city": city.title(),
            **weather_data[city]
        }

    return {
        "city": city.title(),
        "message": "Weather data is not available for this city."
    }



# function for stock price 
def get_stock_price(symbol: str):
    return {
        "symbol" : symbol,
        "price":234.54,
        "currency" : "USD"
    }