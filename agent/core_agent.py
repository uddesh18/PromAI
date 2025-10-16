from openai import OpenAI
from agent.prometheus_client import PrometheusClient

class MonitoringAgent:
    def __init__(self):
        self.prom_client = PrometheusClient()
        self.client = OpenAI()

    def monitor(self):
        metrics = self.prom_client.fetch_metrics()
        findings = []

        for metric_name, data in metrics.items():
            for target, value in data["values"].items():
                if value > data["threshold"]:
                    findings.append(
                        f"⚠️ {metric_name} high on {target} ({value:.2f} > {data['threshold']})"
                    )

        if not findings:
            return "✅ All metrics within normal range."

        summary = "\n".join(findings)
        prompt = (
            f"These system metrics exceeded thresholds:\n{summary}\n\n"
            "Suggest likely causes and remediation actions."
        )

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a DevOps AI monitoring assistant."},
                {"role": "user", "content": prompt}
            ],
        )

        suggestion = response.choices[0].message.content
        return f"{summary}\n\n🤖 Agent Suggestion:\n{suggestion}"
