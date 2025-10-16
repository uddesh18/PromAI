from agent.core_agent import MonitoringAgent

if __name__ == "__main__":
    agent = MonitoringAgent()
    print("🔍 Running AI Monitoring Agent...")
    output = agent.monitor()
    print(output)