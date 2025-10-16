import requests
import yaml

class PrometheusClient:
    def __init__(self, config_path="config/settings.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
        self.base_url = self.config["prometheus"]["base_url"]

    def query_metric(self, query):
        url = f"{self.base_url}/api/v1/query"
        response = requests.get(url, params={"query": query})
        if response.status_code != 200:
            print(f"⚠️ Failed query: {response.status_code}")
            return {}

        data = response.json()["data"]["result"]
        results = {}

        # Store all instances and their metric values
        for item in data:
            labels = item.get("metric", {})
            instance = labels.get("instance", "unknown")
            job = labels.get("job", "")
            value = float(item["value"][1])
            results[f"{job}@{instance}"] = value

        return results

    def fetch_metrics(self):
        results = {}
        for metric in self.config["prometheus"]["metrics"]:
            values = self.query_metric(metric["query"])
            results[metric["name"]] = {
                "values": values,
                "threshold": metric["threshold"]
            }
        return results