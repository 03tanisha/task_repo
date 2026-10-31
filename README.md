# PDF RAG Chatbot

**Live Demo:** [Try the PDF RAG Chatbot](https://tanisha-ragchatbot.streamlit.app/)





# AI Agent with Tools

## Features

### 1. Weather Information
Retrieves sample weather information for Delhi, Jaipur, and Mumbai.

### 2. Stock Price
Retrieves a sample stock price for a given stock symbol.

### 3. Tool Calling
Routes user requests to the appropriate Python function based on the user's query.

### 4. Chat
Allows users to ask multiple questions in a single session.

### 5. Exit
Type `quit`, `exit`, or `bye` to exit the chat.

## Setup Instructions

### 1. Install Python
Install Python if it is not already installed on your system.

### 2. Install Ollama
Download and install Ollama from the official website:

https://ollama.com/

### 3. Download the Model
Open the terminal and run the following command:

```bash
ollama pull qwen2.5:0.5b
```

### 4. Install Dependencies
Activate your virtual environment and install the required dependency:

```bash
pip install ollama
```

### 5. Run the Project
Open the terminal in your project folder and run:

```bash
python main.py
```

## Example Usage

### Example 1: Weather Information

**Input:**
```text
What is the weather in Jaipur?
```

**Output:**
```text
Tool selected: get_weather
Tool input: {'city': 'Jaipur'}
Tool result: {'city': 'Jaipur', 'temperature': 32, 'condition': 'sunny'}

Agent: The weather in Jaipur is sunny with a temperature of 32 degrees Celsius.
```

### Example 2: Stock Price

**Input:**
```text
What is the stock price of TSLA?
```

**Expected tool input:**
```text
{'symbol': 'TSLA'}
```

**Note:** Stock prices are currently sample values and do not represent real-time market prices. Weather information is also based on predefined sample data.

### Example 3: Exit the Chat

**Input:**
```text
quit
```

**Output:**
```text
Agent stopped. Goodbye!
```

## How It Works

1. **User Input:** The user enters a question in natural language.
2. **Intent Recognition:** The Qwen2.5 model identifies which tool is appropriate for the request.
3. **Tool Selection:** The model selects the corresponding Python function, such as `get_weather` or `get_stock_price`.
4. **Function Execution:** The Python program calls the selected function with the required arguments.
5. **Result Generation:** The function returns its result, and the model converts it into a natural-language response.
6. **Continuous Chat:** The user can ask more questions until they type `quit`, `exit`, or `bye`.

## Technologies Used

- Python
- Ollama
- Qwen2.5 (0.5B)
- JSON
- Python Functions

