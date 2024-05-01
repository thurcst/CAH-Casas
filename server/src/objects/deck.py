from objects.pergunta import Pergunta
from objects.resposta import Resposta

from sanic.log import logger
from random import choice


class Deck:
    """
    ### Responsabilidades do Deck

    Ler as cartas da memória

    Selecionar as cartas para serem escolhidas como pergunta

    Distribuir as cartas para os jogadores

    Marcar cartas como ingame (Perguntas e Respostas)
    """

    def __init__(self) -> None:
        self.perguntas = []
        self.respostas = []

        logger.info("Deck foi iniciado.")
        self.carregar_cartas()

    def carregar_cartas(self):
        """Faz a leitura das cartas no banco de dados"""
        with open(
            "/home/costa/Projetos/cards_against_the_humanity/server/src/objects/perguntas.txt"
        ) as f:
            for pergunta in f.readlines():
                self.perguntas.append(Pergunta(pergunta[:-2]))

            logger.info("Foram carregadas %s perguntas", len(self.perguntas))

        with open(
            "/home/costa/Projetos/cards_against_the_humanity/server/src/objects/respostas.txt"
        ) as f:
            for resposta in f.readlines():
                self.respostas.append(Resposta(resposta[:-2]))
            logger.info("Foram carregadas %s respostas", len(self.respostas))

    def pick_respostas(self, k: int = 10):
        """Seleciona 10 cartas arbitrárias entre as cartas que ainda não estão em jogo.
        Automaticamente as marca como ingame.

        Args:
            k (int, optional): Quantidade de cartas a serem puxadas. Defaults to 10.

        Raises:
            Exception: Caso acabem as cartas disponíveis, levanta um erro

        Returns:
            list(Resposta): Lista com as 10 respostas já marcadas como ingame
        """

        respostas_nao_usadas = [
            resposta for resposta in self.respostas if resposta.ingame == False
        ]
        logger.info(f"respostas restantes: {len(respostas_nao_usadas) - 10}")

        if len(respostas_nao_usadas) == 0:
            raise Exception("Acabaram as cartas, porra")

        respostas = [choice(respostas_nao_usadas) for _ in range(k)]

        for resposta in respostas:
            resposta.marcar_ingame()

        if k == 1:
            # Caso onde é a primeira carta a ser jogada
            # não passa pelo processo de seleção dos jogadores
            self.marcar_pergunta_ingame(respostas[0].id)

        return respostas

    def pick_perguntas(self, k: int = 3) -> list[Pergunta]:
        """
        Escolhe aleatoriamente 3 perguntas da lista de perguntas ainda não escolhidas

        Params:
            k (int): Quantidade de perguntas a serem retornadas

        Raises:
            Exception: Erro caso não hajam mais cartas para serem escolhidas

        Returns:
            list[Pergunta]: Lista com as 3 perguntas para o jogador escolher.
        """

        perguntas_nao_usadas = [
            pergunta for pergunta in self.perguntas if pergunta.ingame == False
        ]

        logger.info(f"Perguntas restantes: {len(perguntas_nao_usadas)}")

        if len(perguntas_nao_usadas) == 0:
            raise Exception("Acabaram as cartas, porra")

        perguntas = [choice(perguntas_nao_usadas) for _ in range(k)]

        if k == 1:
            # Caso onde é a primeira carta a ser jogada
            # não passa pelo processo de seleção dos jogadores
            self.marcar_pergunta_ingame(perguntas[0].id)

        return perguntas

    def marcar_pergunta_ingame(self, id):
        """Recebe um ID de pergunta e marca ela como já utilizada em jogo

        Args:
            id (str): identificador da carta a ser marcada

        Raises:
            Exception: Exception de not found
        """
        pergunta = [pergunta for pergunta in self.perguntas if pergunta.id == id].pop()

        if not pergunta:
            raise Exception("Pergunta não existe na lista de perguntas")
        pergunta.ingame = True

        logger.info("%s", pergunta.debug())
