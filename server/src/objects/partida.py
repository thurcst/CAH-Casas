from objects.jogador import Jogador
from objects.deck import Deck
from objects.mesa import Mesa

import logging
import uuid

LOG_FORMAT = "%(asctime)s [%(levelname)s]: %(threadName)s - %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


class Partida:
    """
    Entidade da partida
    """

    def __init__(
        self,
        jogador: Jogador,
        max_pontuacao: int = 10,
        temporizador_votacao: int = 30,
        temporizador_selecao: int = 30,
        max_rodadas: int = 15,
    ) -> None:

        # Valores devault
        self.temporizador_votacao = temporizador_votacao
        self.temporizador_selecao = temporizador_selecao
        self.max_pontuacao = max_pontuacao
        self.max_rodadas = max_rodadas
        self.dono = jogador

        self.jogadores = [self.dono]
        self.rodada_atual = 0
        self.deck = Deck()
        self.mesa = Mesa(deck=self.deck)
        self.id = uuid.uuid4()
        self.started = False

        logger.info("A entidade da Partida foi criada com o ID %s", self.id)

    def __str__(self) -> str:
        debug_text = f"""ID: {self.id}\nStarted: {self.started}\nTemporizador de seleção: {self.temporizador_selecao}\nTemporizador de votação: {self.temporizador_votacao}\nPontuação máxima: {self.max_pontuacao}\nMáximo de rodadas: {self.max_rodadas}\nJogadores: {len(self.jogadores)}\nDono da sala: {str(self.dono)}\n"""
        return debug_text

    def iniciar_jogo(self, id: str) -> str:
        try:
            if id == str(self.dono.id):
                self.started = True
                self.gerar_primeira_pergunta()

                for jogador in self.jogadores:
                    jogador.cartas.extend(self.deck.pick_respostas())

                    for carta in jogador.cartas:
                        carta.jogador = jogador.nome

                return "OK"
            else:
                return "NOT STARTED"

        except Exception as e:
            logger.exception(e)

    def gerar_primeira_pergunta(self) -> None:
        pergunta_inicial = self.deck.pick_perguntas(1)
        self.mesa.pergunta_da_rodada = pergunta_inicial[0]

    def gerar_perguntas(self):
        perguntas = self.deck.pick_perguntas()
        return perguntas

    def selecionar_pergunta(self, payload: dict):

        jogador = self.get_jogador(payload["jogador"])

        if len(payload["resposta"]) > int(self.mesa.pergunta_da_rodada.picks):
            logger.info(
                "O jogador %s enviou mais respostas do que o necessário.", jogador.nome
            )
            raise Exception("Mais respostas do que deveria.")

        respostas_da_rodada = [
            str(resposta.jogador) for resposta in self.mesa.respostas_da_rodada
        ]

        if jogador.nome in respostas_da_rodada:
            raise Exception("Jogador já fez sua seleção.")

        logger.info("Jogadores que já responderam a rodada: %s", respostas_da_rodada)

        for resposta in payload["resposta"]:
            resposta = self.get_resposta(resposta)

            try:
                self.mesa.adicionar_resposta(resposta)
                jogador.descartar_resposta(resposta)
            except Exception as e:
                logger.exception(e)
                raise Exception(e)

    def entrar_na_sala(self, novo_jogador: Jogador) -> uuid.UUID:
        try:
            if novo_jogador.id not in [jogador.id for jogador in self.jogadores]:
                self.jogadores.append(novo_jogador)
            else:
                raise Exception("Jogador de mesmo ID já está no lobby")

            logger.info(
                "O jogador %s entrou na sala com o ID %s",
                novo_jogador.nome,
                novo_jogador.id,
            )
            return self.id
        except Exception as e:
            logger.exception(e)

    def get_resposta(self, id_resposta: str):
        resposta = [
            resposta
            for resposta in self.deck.respostas
            if str(resposta.id) == id_resposta
        ]
        if len(resposta) > 0:
            return resposta[0]

    def get_jogador(self, id_jogador: str):
        jogador = [
            jogador for jogador in self.jogadores if str(jogador.id) == id_jogador
        ]

        if len(jogador) > 0:
            return jogador[0]

    def debug_jogadores(self) -> None:
        for jogador in self.jogadores:
            print(str(jogador))

    def debug(self) -> None:
        print(str(self))