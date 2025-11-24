📊 Retail Insights Assistant Chatbot

Author: Ashwin H
Date: 22-11-2025

Overview

This is a multi-agent conversational chatbot application designed to provide natural language querying and summarization of complex sales data. It leverages a modern data stack combining LangChain, the Google Gemini API, and DuckDB for efficient data analysis directly from local CSV reports.

The application allows users to ask questions about retail performance, sales figures, and other metrics, which the system converts into DuckDB queries and provides human-readable responses via the Gemini generative model.

✨ Key Features

Multi-Agent Architecture: Utilizes LangChain's AgentExecutor and create_react_agent for robust and conversational AI flow.

LLM Integration: Integrated with the Google Gemini generative model via the ChatGoogleGenerativeAI interface for natural language understanding and generation.

Data Query Engine: Executes high-speed SQL queries on local CSV sales data loaded into DuckDB.

User Interface: Built with Streamlit for an interactive, web-based chat interface complete with session management.

Data Handling: Handles multiple CSV datasets and includes error handling for missing files, ensuring stability.

⚙️ Setup Instructions

Follow these steps to get the project running locally.

1. Prerequisites

You must have Python 3.8+ installed on your system.

2. Create and Activate a Python Virtual Environment

It is recommended to use a virtual environment to manage dependencies.
 

python -m venv .venv
# On Windows
.venv\Scripts\activate.bat
# On macOS/Linux
source .venv/bin/activate


3. Install Dependencies

Install all necessary libraries using the provided requirements.txt.

pip install -r requirements.txt


4. Set Gemini API Key

You need a Google Gemini API key to interact with the model.

Obtain your key from the Google AI Studio: https://aistudio.google.com/api-keys

Set the API key as an environment variable. The Streamlit application will automatically use this.

On macOS/Linux:

export GEMINI_API_KEY="YOUR_API_KEY_HERE"


On Windows (Command Prompt):

set GEMINI_API_KEY="YOUR_API_KEY_HERE"


On Windows (PowerShell):

$env:GEMINI_API_KEY="YOUR_API_KEY_HERE"


5. Prepare Data Files

Place your CSV data files in the project's root directory.

Required Data: Ensure files such as Amazon Sale Report.csv and PL March 2021.csv are present, or update the file paths within your Python code (projectvscode.py) to match your actual data locations.

6. Run the Streamlit Application

Start the chatbot interface from your command line:

streamlit run projectvscode.py


The application will open in your default web browser, typically at http://localhost:8501.

6. Usage
Enter natural language queries or commands related to sales data

The AI agent processes inputs via multi-agent collaboration querying DuckDB and generating summarized responses

Chat interface maintains conversation sessions

7. Assumptions & Limitations
Requires access to Gemini API and sales CSV data

Handles up to 15 agent iterations and 2 minutes of processing time

CSV files must be in correct locations or paths updated accordingly

No persistent storage or external database indexing currently

8.Possible Improvements
Add persistent conversational memory across sessions

Extend data scale beyond in-memory DuckDB to distributed databases

Improve toolset with additional analytics and data visualization modules

Optimize query latency and agent response times