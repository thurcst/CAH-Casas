from sanic import Sanic
from objects.jogador import Jogador
from objects.partida import Partida

import logging

LOG_FORMAT = "%(asctime)s [%(levelname)s]: %(threadName)s - %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


def main():
    dummy = Jogador("isaac")
    dummy_2 = Jogador("vitu")

    game = Partida(dummy, 10, 30, 15)
    game.entrar_na_sala(dummy_2)

    game.iniciar_jogo(str(dummy.id))

    game.debug_jogadores()

    for jogador in game.jogadores:
        print("Jogador: {}\nID: {}".format(jogador.nome.capitalize(), jogador.id))

        for carta in jogador.cartas:
            print(carta.id)

    # Simulação de carta jogada

    payload = {"jogador": str(dummy.id), "resposta": [str(dummy.cartas[0].id)]}

    game.selecionar_pergunta(payload=payload)

    print(game.mesa.debug())


if __name__ == "__main__":
    main()
