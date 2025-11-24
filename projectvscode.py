import streamlit as st
import pandas as pd
import duckdb
import os
from langchain.tools import tool

# Import Gemini client from LangChain Google GenAI integration
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_classic.agents import AgentExecutor, create_react_agent #classic langchain for agents with python 3.12.10 to fix compatibility
from langchain_classic import hub

from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
import os
print("Current working directory:", os.getcwd())
# --- Configuration ---
# Set your Gemini API key in environment variable GOOGLE_API_KEY
os.environ["GOOGLE_API_KEY"] = ""  # Replace with your Gemini API key

@st.cache_resource
def initialize_agent():
    def safe_load_csv(filename, encoding=None):
        try:
            return pd.read_csv(filename, on_bad_lines='skip', encoding=encoding)
        except FileNotFoundError:
            st.error(f"File not found: {filename}. Please verify the dataset is available.")
            return pd.DataFrame()
        except Exception as e:
            st.warning(f"Warning loading {filename}: {e}")
            return pd.DataFrame()

    # Load CSV files
    amazon_sale_df = safe_load_csv('Amazon Sale Report.csv', encoding='latin-1')
    cloud_wh_df = safe_load_csv('Cloud Warehouse Compersion Chart.csv')
    expense_df = safe_load_csv('Expense IIGF.csv')
    international_sale_df = safe_load_csv('International sale Report.csv')
    may_2022_df = safe_load_csv('May-2022.csv')
    pl_march_2021_df = safe_load_csv('PL March 2021.csv')
    sale_report_df = safe_load_csv('Sale Report.csv')

    # Setup DuckDB in memory
    con = duckdb.connect(database=':memory:')
    if not amazon_sale_df.empty and len(amazon_sale_df.columns) > 0:
        con.register('amazon_sales', amazon_sale_df)
    if not cloud_wh_df.empty and len(cloud_wh_df.columns) > 0:
        con.register('cloud_warehouse', cloud_wh_df)
    if not expense_df.empty and len(expense_df.columns) > 0:
        con.register('expenses', expense_df)
    if not international_sale_df.empty and len(international_sale_df.columns) > 0:
        con.register('international_sales', international_sale_df)
    if not may_2022_df.empty and len(may_2022_df.columns) > 0:
        con.register('may_2022', may_2022_df)
    if not pl_march_2021_df.empty and len(pl_march_2021_df.columns) > 0:
        con.register('pl_march_2021', pl_march_2021_df)
    if not sale_report_df.empty and len(sale_report_df.columns) > 0:
        con.register('sales_report', sale_report_df)

    @tool
    def run_duckdb_query(query: str) -> str:
        """
        Executes SQL queries on the retail sales data.
        Input: Syntactically correct SQL query string.
        Returns: Top 50 rows of the query result as a string, or an error message.
        Available tables: amazon_sales, cloud_warehouse, expenses, international_sales,
                          may_2022, pl_march_2021, sales_report.
        """
        try:
            result = con.execute(query).fetchdf()
            return result.head(50).to_string()
        except Exception as e:
            return f"Error executing query: {str(e)}"

    tools = [run_duckdb_query]

    # Initialize the Gemini LLM client
    chat_llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.0,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm=chat_llm, tools=tools, prompt=prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=15,
        max_execution_time=120
    )

    store = {}

    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        if session_id not in store:
            store[session_id] = ChatMessageHistory()
        return store[session_id]

    conversational_agent = RunnableWithMessageHistory(
        agent_executor,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    return conversational_agent


# --- Streamlit UI ---
st.set_page_config(page_title="Retail Insights Assistant", page_icon="📊")
st.title("📊 Retail Insights Assistant")
st.markdown("Ask questions about your retail data and get AI-powered insights!")

agent = initialize_agent()

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_query := st.chat_input("Ask your retail data question:"):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            response = agent.invoke(
                {"input": user_query},
                config={"configurable": {"session_id": "streamlit_session"}}
            )
            answer = response['output']
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
