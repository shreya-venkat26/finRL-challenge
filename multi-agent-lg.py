from datasets import load_dataset
import pandas as pd
from newspaper import Article
from langgraph.graph import StateGraph

url = "https://www.benzinga.com/analyst-ratings/price-target/20/05/16093262/10-biggest-price-target-changes-for-friday"
article = Article(url)
article.download()
article.parse()

print(article.text)

input_data = {
    "symbol": "A", 
    "summary": article.text,
    "volume": 1500000,  
    "open": 75.0,
    "close": 78.0
}

def sentiment_agent(state):
    summary = state['summary']
    score = 0.8 if "positive" in summary.lower() else 0.2
    state["sentiment_score"] = score
    return state

def risk_agent(state):
    volume = state.get("volume", 0)
    score = 1.0 if volume > 1_000_000 else 0.3
    state["risk_score"] = score
    return state

def macro_agent(state):
    state["macro_score"] = 0.5
    return state

def tech_agent(state):
    open_price, close_price = state.get("open", 0), state.get("close", 0)
    momentum = (close_price - open_price) / open_price if open_price else 0
    score = max(0, min(1, 0.5 + momentum))
    state["tech_score"] = score
    return state

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

result = graph.invoke(input_data)


print(result)
