import time
import logging
from fastapi import FastAPI, status, Response
from logging import StreamHandler, FileHandler, Formatter
from random import randint
from time import sleep

# CONFIGURAÇÃO DE LOGGING 
logger = logging.getLogger("API_Monitoramento")
logger.setLevel(logging.DEBUG)

# Formatação: asctime, levelname e message
formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Handler para arquivo e para o console
file_handler = FileHandler("api_telemetria.log")
file_handler.setFormatter(formatter)
stream_handler = StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

API = FastAPI()

def simula_latencia(tempo_min: int, tempo_max: int) -> float:
    t = randint(tempo_min, tempo_max) / 10
    sleep(t)
    return t

@API.get("/produtos")
def produtos():
    inicio = time.time() # Início da medição de latência 
    t_latencia = simula_latencia(0, 20)
    
    total_time = (time.time() - inicio) * 1000 # Tempo em ms
    
    # Golden Signal: Tráfego e Latência 
    logger.info(f"Endpoint /produtos acessado. Latência: {total_time:.2f}ms")
    
    return PRODUTOS

@API.post("/produtos", status_code=status.HTTP_201_CREATED)
def pedido(nome_produto: str, response: Response):
    inicio = time.time()
    t_latencia = simula_latencia(0, 15)
    
    # Golden Signal: Erros 
    if nome_produto not in PRODUTOS.keys():
        response.status_code = status.HTTP_400_BAD_REQUEST
        logger.error(f"Erro no pedido: Produto '{nome_produto}' inexistente.")
        return {"status": "Produto não existe"}

    total_time = (time.time() - inicio) * 1000

    # Nível WARN: Se latência > 1000ms (exemplo de X milissegundos)
    if total_time > 1000:
        logger.warning(f"Latência alta no pedido: {nome_produto} demorou {total_time:.2f}ms")
    else:
        logger.info(f"Pedido realizado: {nome_produto} em {total_time:.2f}ms") [cite: 19]

    PEDIDOS.append(PRODUTOS[nome_produto])
    return {"status": "Pedido realizado com sucesso"}

@API.get("/pedidos")
def listar_pedidos():
    # Exemplo simples de Saturação: monitorar tamanho da fila 
    logger.info(f"Listagem de pedidos solicitada. Volume atual: {len(PEDIDOS)} itens.")
    return PEDIDOS
