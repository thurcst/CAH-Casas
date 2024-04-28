import uuid

import logging

from objects.resposta import Resposta

LOG_FORMAT = "%(asctime)s [%(levelname)s]: %(threadName)s - %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


class Jogador:
    def __init__(self, nome: str) -> None:
        self.nome = nome
        self.cartas = []
        self.pontuacao = 0
        self.status = "aguardando"  # possíveis status = aguardando, escolhendo, votando
        self.id = uuid.uuid4()

        logger.info("Jogador %s foi criado com o id %s.", self.nome, self.id)

    def descartar_resposta(self, resposta: Resposta):
        self.cartas = [
            carta for carta in self.cartas if str(carta.id) != str(resposta.id)
        ]
        logger.info(
            "A carta de ID %s foi descartada do deck do jogador %s",
            str(resposta.id),
            self.id,
        )

    def to_json(self) -> str:
        response = {
            "nome": self.nome,
            "id": self.id,
        }

        return response

    def debug(self) -> None:
        print(str(self))

    def __str__(self) -> str:
        txt = f"""\n\tNome: {self.nome}\n\tCartas: {','.join([carta.texto for carta in self.cartas])}\n\tPontuação: {self.pontuacao}\n\tStatus: {self.status}\n\tID: {self.id}"""

        return txt
