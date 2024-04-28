from objects.resposta import Resposta
from objects.deck import Deck

import logging

LOG_FORMAT = "%(asctime)s [%(levelname)s]: %(threadName)s - %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


class Mesa:

    def __init__(self, deck: Deck) -> None:
        self.deck = deck

        self.pergunta_da_rodada = None
        self.respostas_da_rodada = []
        logger.info("Mesa foi iniciada.")

    def reiniciar(self):
        self.pergunta_da_rodada = []
        self.respostas_da_rodada = []

    def adicionar_resposta(self, resposta: Resposta):
        logger.info(
            "A resposta '%s' foi adicionada à mesa e marcada como usada ingame",
            resposta.texto,
        )
        self.respostas_da_rodada.append(resposta)

    def debug(self):
        return f"Pergunta da rodada: \n\tTexto: {self.pergunta_da_rodada.texto}\n\tPicks: {self.pergunta_da_rodada.picks}\nRespostas em jogo: {[resposta.texto for resposta in self.respostas_da_rodada]}"
