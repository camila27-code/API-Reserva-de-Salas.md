from fastapi import APIRouter, HTTPException, status

from schemas.usuario import UsuarioCreate, UsuarioOut
from services.reserva_services import (
    ErrosValidacoes,
    criar_usuario,
    listar_usuarios,
)


router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.post("", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def criar_usuario_route(data: UsuarioCreate):
    try:
        return criar_usuario(**data.model_dump())
    except ErrosValidacoes as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, e.mensagens)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.get("", response_model=list[UsuarioOut])
def listar_usuarios_route():
    return listar_usuarios()
