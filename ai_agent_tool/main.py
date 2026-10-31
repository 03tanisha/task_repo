
import json
import ollama
from tools import get_weather, get_stock_price

# Available tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather information for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Name of the city"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Get stock price of a company",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock ticker, e.g. AAPL"
                    }
                },
                "required": ["symbol"]
            }
        }
    }
]

# Python functions mapping
available_functions = {
    "get_weather": get_weather,
    "get_stock_price": get_stock_price
}

# Keep asking questions
while True:
    user_message = input("\nAsk your question (or type 'quit' to exit): ")

    if user_message.strip().lower() in ["quit", "exit", "bye"]:
        print("Agent stopped. Goodbye!")
        break

    if not user_message.strip():
        continue

    # Send question to model
    response = ollama.chat(
        model="qwen2.5:0.5b",
        messages=[
            {
                "role": "user",
                "content": user_message
            }
        ],
        tools=tools
    )

    message = response.message

    if message.tool_calls:
        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            arguments = tool_call.function.arguments
            if function_name == "get_stock_price":
                user_words = user_message.upper().replace("?", "").split()

                for word in user_words:
                    if word in ["TSLA", "AAPL", "GOOGL", "MSFT", "NVDA"]:
                        arguments["symbol"] = word
                        break

            print("Tool selected:", function_name)
            print("Tool input:", arguments)

            function_to_call = available_functions.get(function_name)

            if function_to_call:
                result = function_to_call(**arguments)
                print("Tool result:", result)

                final_response = ollama.chat(
                    model="qwen2.5:0.5b",
                    messages=[
                        {"role": "user", "content": user_message},
                        message,
                        {
                            "role": "tool",
                            "name": function_name,
                            "content": json.dumps(result)
                        }
                    ],
                    tools=tools
                )

                print("Agent:", final_response.message.content)

            else:
                print("Unknown tool:", function_name)

    else:
        print("Agent:", message.content)
