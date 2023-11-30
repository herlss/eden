from app.scraping.aws import AwsDashboardData

class DashboardService:
    @classmethod
    def getAwsDashboard(cls):
        dashboard = {}

        data = AwsDashboardData()

        filter = [incident for incident in data if incident["region_name"] in ["N. Virginia", "Sao Paulo"]]

        service_count = {}
        for incident in filter:
            service_name = incident["service_name"]
            service_count[service_name] = service_count.get(service_name, 0) + 1

        sao_paulo_count = sum(1 for incident in filter if incident["region_name"] == "Sao Paulo")
        virginia_count = sum(1 for incident in filter if incident["region_name"] == "N. Virginia")

        regions = [
            ["Sao Paulo", sao_paulo_count],
            ["N. Virginia", virginia_count]
        ]

        dashboard["Incidents by Service"] = [[service_name, count] for service_name, count in service_count.items()]
        dashboard["Incidents by Region"] = regions
        dashboard["Total Incidents"] = len(filter)

        return dashboard
