from dotenv import load_dotenv
from requests import Session
import logging
from validation.requests import ValidationStatusCode
from datetime import datetime, timedelta

class ClippingsQuery:
    def __init__(self, token: str):
        load_dotenv()

        self.API_TOKEN_ASTREA = token

        self.session = Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.API_TOKEN_ASTREA}"
            }
        )

        self.validation_status_code = ValidationStatusCode()

        self.logger = logging.getLogger(__name__)

    def query_post(self, fromDate: datetime = None, toDate: datetime = None):
        self.logger.info("Capturando dados de publicações")

        fromDate = fromDate if fromDate else datetime.now() - timedelta(days=1)
        toDate = toDate if toDate else datetime.now()

        self.logger.info(f"Iniciando busca no dia {toDate.strftime('%d/%m/%Y')} - {fromDate.strftime('%d/%m/%Y')}")

        payload = {
            "order": "",
            "cursor": "",
            "page": 0,
            "limit": 10000,
            "caseId": None,
            "caseTitle": None,
            "fromDate": fromDate.strftime("%Y-%m-%d"),
            "toDate": toDate.strftime("%Y-%m-%d"),
            "endCreateDate": None,
            "customerId": None,
            "dateFilter": "RELEASE_DATE",
            "clippingTypeFilter": "ALL",
            "subpoenaStatusFilter": "ALL",
            "caseStatusFilter": "ALL",
            "status": "RECEIVED",
            "clippingSearchName": None,
            "state": None,
            "userId": "5665827422863360",
            "caseResponsibleId": None,
            "dateToShow": "CLIPPING_DATE"
        }

        response = self.session.post(
            "https://app.astrea.net.br/api/v2/clippings/query",
            json=payload
        )

        if not self.validation_status_code.validate(
            request=response,
            permited_status_code=[200]
        ):
            raise response.raise_for_status()

        self.logger.info("Dados de publicações capturado com sucesso")

        return response.json()