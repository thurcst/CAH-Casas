import uuid
import json


class Pergunta:
    def __init__(self, texto: str, autor: str = "default") -> None:
        self.texto = texto
        self.ingame = False
        self.picks = max(texto.count("_"), 1)
        self.autor = autor
        self.id = uuid.uuid4()

    def to_json(self) -> str:
        obj = {
            "texto": self.texto,
            "picks": self.picks,
            "autor": self.autor,
            "id": str(self.id),
        }

        return json.dumps(obj)

    def debug(self):
        return f"""Texto: {self.texto}\nIngame: {self.ingame}\nPicks: {self.picks}\nID: {self.id}\nAutor: {self.autor}"""
