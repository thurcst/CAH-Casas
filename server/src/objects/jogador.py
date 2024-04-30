from objects.resposta import Resposta
from sanic.log import logger

from sanic import Websocket

import uuid


class Jogador:
    def __init__(self, websocket: Websocket, nome: str = None) -> None:
        self.nome = nome
        self.cartas = []
        self.pontuacao = 0
        self.status = "aguardando"  # possíveis status = aguardando, escolhendo, votando
        self.id = websocket.__hash__()
        self.websocket = websocket
        self.id_partida = None

        logger.info("Jogador %s foi criado com o id %s.", self.nome, self.id)

    def descartar_resposta(self, resposta: Resposta):

        logger.info(
            "Carta recebida foi de texto %s e ID %s", resposta.texto, str(resposta.id)
        )

        self.cartas = [
            carta for carta in self.cartas if str(str(carta.id)) != str(resposta.id)
        ]

        logger.info(
            "A carta de ID %s foi descartada do deck do jogador %s",
            str(resposta.id),
            self.id,
        )
        logger.info("Agora o jogador %s possui %s cartas.", self.nome, len(self.cartas))

    def to_json(self) -> str:
        response = {
            "contexto": "informacoes_do_usuario",
            "jogador": self.nome,
            "payload": {
                "id": self.id,
            },
        }

        return response

    def debug(self) -> None:
        print(str(self))

    def __str__(self) -> str:
        txt = f"""\n\tNome: {self.nome}\n\tCartas: {','.join([carta.texto for carta in self.cartas])}\n\tPontuação: {self.pontuacao}\n\tStatus: {self.status}\n\tID: {self.id}"""

        return txt
