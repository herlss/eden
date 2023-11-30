from app.scraping.aws import AwsDashboardData
import requests as req
import json as js

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

    # Gráfico do dash abaixo será apenas 1(ou 2) big numbers. Colocar na descrição do(s) big number(s): "Services in Normal 
    # Performance status" e "Services in not Normal Performance status :/"
    @classmethod
    def getOciDashboard(cls):
        url = "https://ocistatus.oraclecloud.com/api/v2/components_v2.json"

        r = req.get(url)

        data = r.json()
        json = []

        for region in data["regionHealthReports"]:
            if "Sao Paulo" in region["regionName"]:
                json.append(region)
            elif "Vinhedo" in region["regionName"]:
                json.append(region)

        vinhedoOn = 0
        saoPauloOn = 0
        totalOn = 0
        vinhedoOff = 0
        saoPauloOff = 0
        totalOff = 0

        for region in json:
            if "Vinhedo" in region["regionName"]:
                for service in region["serviceHealthReports"]:
                    if service["serviceStatus"] == "NormalPerformance":
                        vinhedoOn += 1
                    else:
                        vinhedoOff += 1
            elif "Sao Paulo" in region["regionName"]:
                for service in region["serviceHealthReports"]:
                    if service["serviceStatus"] == "NormalPerformance":
                        saoPauloOn += 1     
                    else:
                        saoPauloOff += 1   
            totalOn = vinhedoOn + saoPauloOn
            totalOff = vinhedoOff + saoPauloOff

        print(saoPauloOn, vinhedoOn, totalOn, saoPauloOff, vinhedoOff, totalOff)
        return {"Normal Performance services": totalOn, "Not Normal Performance services": totalOff}
