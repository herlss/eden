from app.scraping.aws import AwsDashboardData
from collections import Counter

class DashboardService:
    @classmethod
    def getAwsDashboard(self):
        dashboard = {}

        data = AwsDashboardData()

        filter = [incident for incident in data if incident["region_name"] in ["N. Virginia", "Sao Paulo"]]

        service_name_counts = Counter(incident["service_name"] for incident in filter)

        regions = [
            ["Sao Paulo", sum(1 for incident in filter if incident["region_name"] == "Sao Paulo")],
            ["N. Virginia", sum(1 for incident in filter if incident["region_name"] == "N. Virginia")]
        ]

        dashboard["Incidents by Service"] = [[service_name, count] for service_name, count in service_name_counts.items()]
        dashboard["Incidents by Region"] = regions
        dashboard["Total Incidents"] = len(filter)

        return dashboard