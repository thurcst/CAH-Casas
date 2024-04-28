import uuid
import json


class Resposta:
    def __init__(self, texto: str, autor: str = "Cartas contra a humanidade") -> None:
        self.texto = texto
        self.ingame = False
        self.autor = autor
        self.jogador = None
        self.votos = 0
        self.id = uuid.uuid4()

    def marcar_ingame(self):
        self.ingame = True

    def to_json(self) -> str:
        obj = {"texto": self.texto, "autor": self.autor, "id": self.id}

        return json.dumps(obj)

    def debug(self):
        return f"""Texto: {self.texto}\nIngame: {self.ingame}\nVotos: {self.votos}\nID: {self.id}\nAutor: {self.autor}\nJogador: {self.jogador}"""
