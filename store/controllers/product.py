from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status
from pydantic import UUID4
from store.core.exceptions import InsertionError, NotFoundException

from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.usecases.product import ProductUsecase

router = APIRouter(tags=["products"])


@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def post(
    body: ProductIn = Body(...), usecase: ProductUsecase = Depends()
) -> ProductOut:
    try:
        return await usecase.create(body=body)
    except InsertionError as e:  
        raise HTTPException(status_code=400, detail="Erro ao inserir o produto: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor: " + str(e))



@router.get(path="/{id}", status_code=status.HTTP_200_OK)
async def get(
    id: UUID4 = Path(alias="id"), usecase: ProductUsecase = Depends()
) -> ProductOut:
    try:
        return await usecase.get(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)

@router.get(path="/", status_code=status.HTTP_200_OK)
async def query(
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    usecase: ProductUsecase = Depends()
) -> List[ProductOut]:
    return await usecase.query(min_price=min_price, max_price=max_price)

@router.patch(path="/{id}", status_code=status.HTTP_200_OK)
async def patch(
    id: UUID4 = Path(alias="id"),
    body: ProductUpdate = Body(...),
    usecase: ProductUsecase = Depends(),
) -> ProductUpdateOut:
    try:
        updated_at = datetime.now()
        return await usecase.update(id=id, body=body, updated_at=updated_at)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"O produto com o ID {id} não foi encontrado. Por favor, verifique o ID e tente novamente. {exc}")


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: UUID4 = Path(alias="id"), usecase: ProductUsecase = Depends()
) -> None:
    try:
        await usecase.delete(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)