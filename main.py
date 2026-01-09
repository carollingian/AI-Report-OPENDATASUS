from src.agent.orchestrator import build_agent

agent = build_agent()

response = agent.invoke({
    "input": "Gere um relatório epidemiológico sobre o cenário atual da SRAG no Brasil"
})

print(response["output"])