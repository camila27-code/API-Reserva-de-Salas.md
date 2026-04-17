from typing import Self
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Reserva:
    def __init__(
        self,
        id: int,
        usuario_id: int,
        sala_id: int,
        data: str,
        hora_inicio: str,
        hora_fim: str,
        status: str = "active"
    ):
        self.id = id
        self.usuario_id = usuario_id
        self.sala_id = sala_id
        self.data = data
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim
        self.status = status

    def cancelar(self) -> bool:
        if self.status == 'canceled':
            return False
        self.status == 'canceled'
        return True
    

    def finalizar(self, hora_fim, hora_atual: str) -> bool:
        formato = '%H:%M'
        hora_fim = datetime.strftime(self.hora_fim, formato)
        hora_atual = datetime.strftime(hora_atual, formato)
        if hora_atual > hora_fim:
            self.status =   'finished'
            return True
        return False
    

    def duracao_em_horas(self, hora_inicio, hora_fim: str) -> float:
        formato = '%H:%M'
        hora_inicio = datetime.strptime(self.hora_inicio, formato)
        hora_fim = datetime.strptime(self.hora_fim, formato)
        return ((hora_fim - hora_inicio).seconds // 3600)


    def conflita_com(self, outra_reserva, sala_id: Self) -> bool:
        formato = '%H:%M'

        if self.sala_id != outra_reserva.sala_id or self.data != outra_reserva.data:
          return False
        

        hora_inicio = datetime.strptime(outra_reserva.hora_inicio, formato).time()
        hora_fim = datetime.strptime(outra_reserva.hora_fim, formato).time()
        hora_inicio = datetime.strptime(self.hora_inicio, formato).time()
        hora_fim = datetime.strptime(self.hora_fim, formato).time()
        return hora_inicio < hora_inicio and hora_inicio < hora_fim
