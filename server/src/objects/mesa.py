from objects.resposta import Resposta
from objects.deck import Deck
from sanic.log import logger


class Mesa:

    def __init__(self, deck: Deck) -> None:
        self.votos = 0
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

    def computar_voto(self, id_resposta):
        obj = [
            resposta
            for resposta in self.respostas_da_rodada
            if str(resposta.id) == id_resposta
        ]

        if len(obj) > 0:
            obj[0].votos += 1
            self.votos += 1
        else:
            raise Exception("Carta não encontrada")

        logger.info("A respost '%s' agora possui %s votos.", obj[0].texto, obj[0].votos)

    def finalizar_rodada(self) -> list[Resposta]:
        def __return_votos(resposta: Resposta):
            return resposta.votos

        votados = sorted(self.respostas_da_rodada, key=__return_votos)
        return votados

    def debug(self):
        return f"Pergunta da rodada: \n\tTexto: {self.pergunta_da_rodada.texto}\n\tPicks: {self.pergunta_da_rodada.picks}\nRespostas em jogo: {[resposta.texto for resposta in self.respostas_da_rodada]}"
