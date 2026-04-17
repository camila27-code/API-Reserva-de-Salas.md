from fastapi import APIRouter, HTTPException, status

from schemas.reserva import ReservaCreate, ReservaOut
from services.reserva_services import(
    ErrosValidacoes,
    buscar_reserva,
    cancelar_reserva,
    criar_reserva,
    finalizar_reserva,
    listar_reservas,
    listar_reservas_usuario,
)

router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.post("", response_model=ReservaOut, status_code=status.HTTP_201_CREATED)
def criar_reserva_route(data: ReservaCreate):
    try:
        return criar_reserva(**data.model_dump())
    except ErrosValidacoes as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, e.mensagens)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e)) 


@router.get("", response_model=list[ReservaOut])
def listar_reservas_routs():
    return listar_reservas()


@router.get("/usuario/{usuario_id}", response_model=list[ReservaOut])
def listar_reservas_usuario_route(usuario_id: int):
    try:
        return listar_reservas_usuario(usuario_id)
    except ErrosValidacoes as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, e.mensagens)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.get("/{reserva_id}", response_model=ReservaOut)
def buscar_reserva_route(reserva_id: int):
    try:
        return buscar_reserva(reserva_id)
    except ErrosValidacoes as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, e.mensagens)


@router.put("/{reserva_id}/cancelar")
def cancelar_reserva_route(reserva_id: int):
    try:
        return cancelar_reserva(reserva_id)
    except ErrosValidacoes as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, e.mensagens)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))



@router.put("/{reserva_id}/finalizar")
def finalizar_reserva_route(reserva_id: int, hora_atual: str):
    try:
        return finalizar_reserva(reserva_id, hora_atual)
    except ErrosValidacoes as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, e.mensagens)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))
    
