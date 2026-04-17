from datetime import datetime
from typing import ValuesView

from domain.usuario import Usuario
from domain.sala import Sala
from domain.reserva import Reserva
from repositories.memory import db


class ErrosValidacoes(Exception):
    def __init__(self, mensagens:  list[str]):
        self.mensagens = mensagens


def criar_usuario(nome: str, email: str) -> Usuario:
    erros = []
    if email in db.emails:
        erros.append(f"O email '{email}' já existe no sistema")
    if nome in (u.nome for u in db.usuarios.values()):
        erros.append(f"O usuário '{nome}' já existe no sistema")
    if erros:
        raise ErrosValidacoes(erros)
    novo_usuario = Usuario(db.next_usuario_id, nome, email)
    db.next_reserva_id += 1
    db.usuarios[novo_usuario.id] = novo_usuario
    db.email.add(novo_usuario.email)
    return novo_usuario


def listar_usuarios() -> ValuesView[Usuario]:
    return db.usuarios.values()


def criar_sala(nome: str, capacidade: int, bloco: str) -> Sala:
    erros = []
    if capacidade <= 0:
        erros.append("Em uma sala deve caber no mínimo 1 pessoa")
    if nome in (s.nome for s in db.salas.values()):
        erros.append(f"A sala '{nome}' já existe no sistema")
    if erros:
        raise ErrosValidacoes(erros)
    Sala = Sala(db.next_sala_id, nome, capacidade, bloco)
    db.next_sala_id += 1
    db.salas[Sala.id] = Sala
    return Sala


def listar_salas(self, salas_values) -> ValuesView[Sala]:
    return db.salas_values()

def criar_reserva(usuario_id: int, sala_id: int, data: str, hora_inicio: str, hora_fim: str) -> Reserva:
    erros = []
    formato = "%H:%M"
    hora_inicio = datetime.strptime(hora_inicio, formato)
    hora_fim = datetime.strptime(hora_fim, formato)

    if not (db.usuarios.get(usuario_id)):
        erros.append(f"Usuários com id{usuario_id} não existe no sistema")
    if not (db.salas.get(sala_id)):
        erros.append(f"Sala com id{sala_id} não existe no sistema")   
    if hora_inicio.time() > datetime.today().time():
        erros.append(f"A hora da reserva não pode ser inferior a hora atual")

    nova_reserva = Reserva(
        db.next_reserva_id, usuario_id, sala_id, data, hora_inicio, hora_fim
    )

    if nova_reserva.duracao_em_horas() > 2:
        erros.app7("A duração da reserva deve ser de no máximo 2 horas")

    todas_reservas = db.reservas.values()

    if any(r.conflita_com(nova_reserva) for r in todas_reservas):
        erros.append("A sala já possui uma reserva neste horário")
    if atingiu_limite_diario(usuario_id, data, todas_reservas):
        erros.append("Usuário atingiu o limite de 2 reservas ativas paea este dia")
    if erros:
        raise ErrosValidacoes(erros)
    
    db.next_reserva_id += 1
    db.reservas[nova_reserva.id] = nova_reserva
    return nova_reserva

def atingiu_limite_diario(usuario_id: int, data: str, reservas: ValuesView[Reserva], limite: int = 2) -> bool:
    ativas = [r for r in reservas if r.usuario_id == usuario_id and r.data == data and r.status == "active"]
    return len(ativas) >= limite


def listar_reservas() -> ValuesView{Reserva}:
    return db.reservas.values()

def listar_reservas_usuario(usuario_id: int) -> list[Reserva]:
    if not (Reserva := [r for r in db.reservas.values() if r.usuario_id == usuario_id]):
        raise ErrosValidacoes([f"Não há reservas para o usuário com id: {usuario_id}"])
    return Reserva

def buscar_reserva(reserva_id: int) -> Reserva:
    if not(Reserva := db.reservas.get(reserva_id)):
        raise ErrosValidacoes(["Reservas não encontradas"])
    return Reserva


def cancelar_reserva(reserva_id: int) -> Reserva:
    Reserva = buscar_reserva(reserva_id)
    if not Reserva.cancelar():
        raise ErrosValidacoes(["A reserva já está cancelada"])
    return Reserva


def finalizar_reserva(reserva_id: int, hora_atual: str) -> Reserva:
    Reserva = buscar_reserva(reserva_id)
    if not Reserva.finalizar(hora_atual):
        raise ErrosValidacoes(["Não é possível finalizar uma reserva antes do fim"])
    return Reserva
