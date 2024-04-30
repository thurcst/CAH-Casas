import asyncio
from websockets import client
import json

from pprint import pprint


def request_user_input():
    entrada = input("Escolha uma operação para ser feita: ")
    if entrada == "1":
        metadata = {"contexto": "iniciar_conexao"}
    elif entrada == "2":
        nome = input("Digita teu nome: ")
        metadata = {"contexto": "criar_jogador", "payload": {"nome": nome}}
    elif entrada == "3":
        metadata = {"contexto": "criar_partida"}
    elif entrada == "4":
        id_sala = input("Digite o ID da sala: ")
        metadata = {"contexto": "entrar_na_sala", "payload": {"id_sala": id_sala}}

    return metadata


async def conn():
    async with client.connect("ws://127.0.0.1:3000/game") as ws:
        try:
            while True:
                entrada = request_user_input()

                await ws.send(json.dumps(entrada))

                data = await ws.recv()
                pprint(data)
        except KeyboardInterrupt:
            await ws.close()


asyncio.get_event_loop().run_until_complete(conn())
