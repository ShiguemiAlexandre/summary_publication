from requests import Request

class ValidationStatusCode:
    """
    Classe responsável por validar se o status code de uma requisição está entre os permitidos.
    """
    def validate(self, request: Request, permited_status_code: list[int]) -> bool:
        """
        Valida se o status code da requisição está na lista de códigos permitidos.

        Args:
            request (Request): Objeto da requisição a ser validada.
            permited_status_code (list[int]): Lista de status codes aceitos.

        Returns:
            bool: True se o status code for permitido, False caso contrário.
        """
        if request.status_code in permited_status_code:
            return True
        return False
