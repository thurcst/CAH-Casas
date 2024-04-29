from sanic import Sanic, Websocket, Request, HTTPResponse
from sanic.log import logger

import json

from objects.jogador import Jogador
from objects.partida import Partida

app = Sanic(
    __name__,
)

JOIN_LIST = {}

"""
Formato das requisições

{
    contexto: 'entrou_na_sala',
    jogador: 'nome do usuario',
    payload: any
}
"""


async def handler(msg: dict, ws: Websocket):
    logger.debug(msg)
    identifier = ws.__hash__()

    if msg["contexto"] == "iniciar_conexao":
        jogador = Jogador()

        JOIN_LIST[identifier] = jogador, ws
        response = json.dumps(jogador.to_json())
        await ws.send(response)

    if msg["contexto"] == "reconetar":
        raise NotImplementedError

    elif msg["contexto"] == "criar_jogador":
        jogador, _ = JOIN_LIST[identifier]
        jogador.nome = msg["payload"]["nome"]

        response = {"contexto": "nome_atualizado"}

        await ws.send(json.dumps(response))


@app.websocket("/game")
async def game(request: Request, ws: Websocket):

    logger.debug(request.__str__())

    async for msg in ws:

        data = json.loads(msg)

        logger.debug(data)
        logger.debug(ws.__hash__())

        await handler(data, ws)


@app.get("/ping")
async def ping(request: Request):
    return HTTPResponse("pong", 200)


if __name__ == "__main__":
    app.run("127.0.0.1", 3000, auto_reload=True, verbosity=0, access_log=False)
    # app.run()
