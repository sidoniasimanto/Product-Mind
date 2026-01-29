from backend.agents.product_agent import ProductDecisionAgent

agent = ProductDecisionAgent()
decisions = agent.run()

for d in decisions[:5]:
    print(agent.explain(d))
