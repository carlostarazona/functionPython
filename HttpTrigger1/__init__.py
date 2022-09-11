
import azure.functions as func
from ..webscraping import scrape_site

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    req_body = req.get_json()

    dni = req_body.get('dni')
    dia_emisión = req_body.get('dia_emisión')
    mes_emisión = req_body.get('mes_emisión')
    año_emisión = req_body.get('año_emisión')
    dia_nacimiento = req_body.get('dia_nacimiento')
    mes_nacimiento = req_body.get('mes_nacimiento')
    año_nacimiento = req_body.get('año_nacimiento')
    respuestascraping = scrape_site(dni,dia_emisión,mes_emisión,año_emisión,dia_nacimiento,mes_nacimiento,año_nacimiento)
    if respuestascraping == 500:
        return func.HttpResponse(
            body ="Credenciales incorrectas",
            status_code= 400
            )
    else:
        return func.HttpResponse(
            body = respuestascraping,
            mimetype="application/json",
            status_code = 200
        )
    
