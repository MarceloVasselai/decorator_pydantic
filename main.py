import requests
from pydantic import BaseModel, ValidationError

# Criando o decorator
def calcular_tempo(funcao):
    def wrapper():
        import time
        inicio = time.time()
        print("Acessando a API....")
        funcao()  # Chama a função original
        print("Retorno da API....")
        fim = time.time()
        tempo_execucao = fim - inicio
        print(f"Tempo de execução: {tempo_execucao:.2f} segundos")
    return wrapper

# Definindo um modelo Pydantic para validar a resposta da API
class CotacaoDolar(BaseModel):
    bid: float
    ask: float
    high: float
    low: float
    varBid: float
    pctChange: float
    timestamp: str
    create_date: str

class RespostaAPI(BaseModel):
    USDBRL: CotacaoDolar

@calcular_tempo
def pegar_cotacao_dolar():
    link = "https://economia.awesomeapi.com.br/last/USD-BRL"
    requisicao = requests.get(link)

    if requisicao.status_code == 200:
        try:
            resposta = RespostaAPI(**requisicao.json())  # Valida a resposta usando Pydantic
            print(f"Cotação do Dólar: {resposta.USDBRL.bid}")
            print(f"Código de Retorno da Requisição: {requisicao.status_code}")
            return resposta.USDBRL.bid
        except ValidationError as e:
            print("Erro de validação da resposta:", e.json())
    else:
        raise Exception("Erro ao acessar a API de cotação do dólar.")

# Chama a função para pegar a cotação do dólar
pegar_cotacao_dolar()