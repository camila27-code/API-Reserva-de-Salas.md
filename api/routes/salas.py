from fastapi import APIRouter, HTTPException, status

from schemas.sala import SalaCreate, SalaOut
from services.reserva_services import (
    ErrosValidacoes,
    criar_sala,
    listar_salas
)

router = APIRouter(prefix="/salas", tags=["Salas"])


@router.post("", response_model=SalaOut, status_code=status.HTTP_201_CREATED)
def criar_sala_route(data: SalaCreate):
    try:
        return criar_sala(**data.model_dump())
    except ErrosValidacoes as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, e.mensagens)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.get("", response_model=list[SalaOut])
def listar_salas_route():
     return listar_salas()
