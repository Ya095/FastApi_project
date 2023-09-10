from datetime import datetime
import time
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.operations.models import operation
from src.operations.schemas import OperationCreate


router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)


# пример кэширования (30 сек)
@router.get("/long_operation")
@cache(expire=30)
def get_long_op():
    time.sleep(2)
    return 'Очень долгие вычисления'


@router.get("")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.all(),
            "details": None
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.post("")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(operation).values(**new_operation.dict())
        await session.execute(stmt)
        await session.commit()
        return {"status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail={
            "status": "error: wrong data",
            "date": f"{datetime.today().replace(microsecond=0)}",
            "detail": str(e)
        })

