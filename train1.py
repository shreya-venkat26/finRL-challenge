from openai import OpenAI
from langgraph.graph import StateGraph
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    # HAS A LIMIT FOR NOW (?)
    api_key = "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"
)

def deepseek_agent(prompt_text: str) -> str:
    response = client.chat.completions.create(
        model="deepseek/deepseek-r1",
        messages=[{"role": "user", "content": prompt_text}]
    )
    return response.choices[0].message.content.strip()


def sentiment_agent(state):
    prompt = f"""You are a sentiment analyzer.
    Estimate a sentiment score from 0 to 1 for this news:

    {state['input']}

    Respond with just the number."""
    try:
        score = float(deepseek_agent(prompt))
    except:
        score = 0.5
    state["sentiment_score"] = score
    return state

def risk_agent(state):
    prompt = f"""You are a financial risk analyst.
    Based on this market news:

    {state['input']}

    What is the risk score from 0 (very low) to 1 (very high)? Respond with just the number."""
    try:
        score = float(deepseek_agent(prompt))
    except:
        score = 0.5
    state["risk_score"] = score
    return state

def macro_agent(state):
    prompt = f"""You are a macroeconomic analyst.
    Given this news:

    {state['input']}

    How relevant is this to macroeconomic trends? Give a score 0 (not relevant) to 1 (highly relevant)."""
    try:
        score = float(deepseek_agent(prompt))
    except:
        score = 0.5
    state["macro_score"] = score
    return state

def tech_agent(state):
    prompt = f"""You are a technical signal predictor.
    Based on this news and implied sentiment:

    {state['input']}

    What is the technical confidence score from 0 to 1?"""
    try:
        score = float(deepseek_agent(prompt))
    except:
        score = 0.5
    state["tech_score"] = score
    return state

# langraph agent chain
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

# test1
example_input = {
    "input": "Tesla shares surged after the company reported record deliveries, surpassing analyst expectations."
}

result = graph.invoke(example_input)

print("\nFinal Output:")
for k, v in result.items():
    print(f"{k}: {v}")
