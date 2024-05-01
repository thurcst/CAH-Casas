from websockets.exceptions import ConnectionClosed
from sanic import Sanic, Websocket, Request
from sanic.signals import Event
from sanic.log import logger

from objects.jogador import Jogador
from objects.partida import Partida

import json

app = Sanic(__name__)

ONLINE_PLAYERS = {}
PARTIDAS = {}

"""
Formato das requisições

{
    contexto: 'entrou_na_sala',
    jogador: 'nome do usuario',
    payload: any
}
"""


async def check_state(ws: Websocket):
    return ws.ws_proto.state


async def error(error_msg: str, ws: Websocket):
    metadata = {"contexto": "erro", "payload": {"error_msg": error_msg}}
    await ws.send(json.dumps(metadata))


def get_jogador(id_jogador):
    try:
        jogador = ONLINE_PLAYERS[id_jogador]
        return jogador
    except KeyError as e:
        logger.info("O jogador procurado não existe: %s", e)


def get_partida(id_sala):
    try:
        partida = PARTIDAS[id_sala]
        return partida
    except KeyError as e:
        logger.error("Partida não existe. %s", e)


@app.signal("jogador.conexao.iniciar")
async def iniciar_conexao(**context):

    ws = context["websocket"]
    identifier = ws.__hash__()

    if ONLINE_PLAYERS.get(identifier) != None:
        await error("usuario ja cadastrado", ws)
        return

    jogador = Jogador(websocket=ws)

    ONLINE_PLAYERS[identifier] = jogador

    metadata = jogador.to_json()
    response = json.dumps(metadata)
    await ws.send(response)


@app.signal("jogador.conexao.entrar_na_sala")
async def entrar_na_sala(**context):

    ws = context["websocket"]
    identifier = ws.__hash__()

    id_sala = context.get("payload").get("id_sala")

    jogador = get_jogador(identifier)
    partida = get_partida(id_sala)

    try:
        metadata_partida = partida.entrar_na_sala(jogador)
        metadata_partida = json.loads(metadata_partida)

        for jogador in partida.jogadores:
            metadata = {"contexto": "entrou_na_partida", "payload": metadata_partida}
            metadata = json.dumps(metadata)
            await jogador.websocket.send(metadata)
    except Exception as e:
        logger.info("Aconteceu um erro ao entrar na sala: %s", e)


@app.signal("jogador.registro.definir_nome")
async def criar_jogador(**context):
    ws = context.get("websocket")
    identifier = ws.__hash__()
    nome = context.get("payload").get("nome")

    jogador = ONLINE_PLAYERS.get(identifier)
    jogador.nome = nome

    response = {"contexto": "nome_atualizado"}

    await ws.send(json.dumps(response))


@app.signal("sala.registro.criar")
async def criar_sala(**context):
    ws = context.get("websocket")
    identifier = ws.__hash__()

    jogador = ONLINE_PLAYERS[identifier]
    partida = Partida(jogador=jogador)
    jogador.id_partida = partida.id

    PARTIDAS[str(partida.id)] = partida

    await ws.send(partida.to_json())


@app.signal("sala.status.iniciar")
async def iniciar_sala(**context):
    ws = context.get("websocket")
    identifier = ws.__hash__()

    jogador = ONLINE_PLAYERS[identifier]
    partida = PARTIDAS[jogador.id_partida]

    if partida.dono.id == jogador.id:
        pergunta = partida.iniciar_jogo()
        metadata = {"contexto": "partida_iniciada", "payload": {"pergunta": pergunta}}
        metadata = json.dumps(metadata)

    for jogador in partida.jogadores:
        await jogador.websocket.send(metadata)


@app.signal("sala.status.iniciar")
async def distribuir_cartas(**context):
    ws = context.get("websocket")
    identifier = ws.__hash__()

    jogador = ONLINE_PLAYERS[identifier]
    partida = PARTIDAS[jogador.id_partida]

    partida.distribuir_cartas()

    for jogador in partida.jogadores:
        metadata = {
            "contexto": "cartas_distribuidas",
            "payload": {"cartas": [resposta.to_json() for resposta in jogador.cartas]},
        }
        await jogador.websocket.send(metadata)


@app.signal("sala.votacao.iniciar")
async def iniciar_votacao(**context):
    ws = context.get("websocket")
    identifier = ws.__hash__()

    jogador = ONLINE_PLAYERS.get(identifier)
    partida = PARTIDAS.get(jogador.id_partida)

    metadata = {"contexto": "iniciar_votacao"}

    await partida.broadcast(metadata)


async def handler(msg: dict, ws: Websocket):

    ctx = msg.get("contexto")

    assert ctx != None

    try:
        if ctx == "iniciar_conexao":
            await app.dispatch("jogador.conexao.iniciar", context={"websocket": ws})

        elif ctx == "entrar_na_sala":
            await app.dispatch(
                "jogador.conexao.entrar_na_sala",
                context={"websocket": ws, "payload": msg["payload"]},
            )

        elif ctx == "reconetar":
            raise NotImplementedError

        elif ctx == "criar_jogador":
            await app.dispatch(
                "jogador.registro.definir_nome",
                context={"websocket": ws, "payload": msg["payload"]},
            )

        elif ctx == "criar_partida":
            await app.dispatch(
                "sala.registro.criar",
                context={"websocket": ws},
            )

        elif ctx == "iniciar_partida":
            await app.dispatch("sala.status.iniciar", context={"websocket": ws})

        elif ctx == "iniciar_votacao":
            await app.dispatch("sala.votacao.iniciar", context={"websocket": ws})

        elif ctx == "contabilizar_voto":
            raise NotImplementedError

        elif ctx == "finalizar_votacao":
            raise NotImplementedError

        elif ctx == "finalizar_partida":
            raise NotImplementedError

    except Exception as e:
        logger.error("Ocorreu um erro que gerou a exeption %s", e)


@app.signal(Event.WEBSOCKET_HANDLER_BEFORE)
async def websocket_after(**context):
    for user in ONLINE_PLAYERS:
        state = await check_state(ONLINE_PLAYERS[user].websocket)

        logger.info(
            "State atual do jogador %s (%s) é %s",
            ONLINE_PLAYERS[user].nome,
            ONLINE_PLAYERS[user].websocket.__hash__(),
            state,
        )

        if state != 1:
            del ONLINE_PLAYERS[user]


@app.websocket("/game")
async def game(request: Request, websocket: Websocket):

    while True:
        try:
            data = await websocket.recv()
            data = json.loads(data)

            await handler(data, websocket)
        except Exception as e:
            logger.error("a conexão foi fechada. Exception: %s", e)
            break


if __name__ == "__main__":
    app.run("127.0.0.1", 3000, dev=True, auto_reload=True)
