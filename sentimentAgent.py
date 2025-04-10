from langchain_openai import ChatOpenAI

from langchain.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph

# Initialize the LLM
llm = ChatOpenAI(model="gpt-3.5-turbo")

# --------------------- Agent Prompts ---------------------

sentiment_prompt = ChatPromptTemplate.from_template("""
You are a financial sentiment analyzer.
Analyze the following news or sentence and give a sentiment score between 0 (very negative) and 1 (very positive).

News: {text}

Respond with a number between 0 and 1.
""")

risk_prompt = ChatPromptTemplate.from_template("""
You are a financial risk analyzer.
Based on the news or sentence below, estimate a risk score between 0 (very low risk) and 1 (very high risk).

News: {text}

Respond with a number between 0 and 1.
""")

macro_prompt = ChatPromptTemplate.from_template("""
You are a macroeconomic analyst.
Estimate a macroeconomic relevance score for the following news or sentence between 0 (irrelevant) and 1 (very relevant).

News: {text}

Respond with a number between 0 and 1.
""")

tech_prompt = ChatPromptTemplate.from_template("""
You are a technical analyst.
Estimate a technical signal confidence score between 0 (low confidence) and 1 (high confidence) for the following news or sentence.

News: {text}

Respond with a number between 0 and 1.
""")

# --------------------- Agent Functions ---------------------

def call_llm_score(prompt_template, text):
    prompt = prompt_template.format_messages(text=text)
    response = llm(prompt)
    try:
        return float(response.content.strip())
    except ValueError:
        return 0.5  # fallback default

def sentiment_agent(state):
    score = call_llm_score(sentiment_prompt, state["input"])
    state["sentiment_score"] = score
    return state

def risk_agent(state):
    score = call_llm_score(risk_prompt, state["input"])
    state["risk_score"] = score
    return state

def macro_agent(state):
    score = call_llm_score(macro_prompt, state["input"])
    state["macro_score"] = score
    return state

def tech_agent(state):
    score = call_llm_score(tech_prompt, state["input"])
    state["tech_score"] = score
    return state

# --------------------- LangGraph Build ---------------------

builder = StateGraph(dict)

builder.add_node("SentimentAgent", sentiment_agent)
builder.add_node("RiskAgent", risk_agent)
builder.add_node("MacroAgent", macro_agent)
builder.add_node("TechnicalAgent", tech_agent)

builder.set_entry_point("SentimentAgent")
builder.add_edge("SentimentAgent", "RiskAgent")
builder.add_edge("RiskAgent", "MacroAgent")
builder.add_edge("MacroAgent", "TechnicalAgent")
builder.set_finish_point("TechnicalAgent")

graph = builder.compile()

# --------------------- Example Run ---------------------

example_input = {
    "input": "Tesla stock surged after the company reported record-breaking quarterly deliveries, beating Wall Street estimates."
}

result = graph.invoke(example_input)
print(result)
