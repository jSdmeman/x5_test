from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import shortuuid

from database.database import sync_engine, SessionLocal
from database import models, crud, schemas
from database.models import integrations
from integrator import etherscan_integration, selectel_integration


models.Base.metadata.create_all(bind=sync_engine)

app = FastAPI()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        await db.close()


@app.post("/create_integration", response_model=schemas.IntegrationTaskCreated)
async def create_integration(name: str | None = None, db: AsyncSession = Depends(get_db)):
    # создаем имя если его нет
    if not name:
        name = f"user_{shortuuid.uuid()}"

    # создаем таск
    task = schemas.IntegrationTaskCreate(name=name)
    db_task = await crud.create_integration_task(db=db, task=task)

    for name in integrations:
        # сохраняем интеграции в бд
        integration = schemas.IntegrationCreate(name=name)
        integration = await crud.create_integration(db=db, task_id=db_task.id, integration=integration)
        # добавляем интеграции в очередь
        if name == 'etherscan':
            etherscan_integration.delay(db_task.id, integration.retry_counter)
        elif name == 'selectel':
            selectel_integration.delay(db_task.id, integration.retry_counter)

    # отдаем id статуса
    await db.close()
    return schemas.IntegrationTaskCreated(task_id=db_task.id)


@app.get("/task_status/{task_id}", response_model=schemas.IntegrationTask)
async def task_status(task_id: int, db: AsyncSession = Depends(get_db)):
    # получаем таск
    db_task = await crud.get_integration_task(db, task_id)

    # ошибка id таска
    if not db_task:
        raise HTTPException(status_code=404, detail='Task not found')

    # статусы интеграций
    db_statuses = await crud.get_integration(db, task_id)
    statuses = list(map(lambda x: schemas.Integration(name=x.name, status=x.status, retry_counter=x.retry_counter), db_statuses))

    # формируем ответ
    task = schemas.IntegrationTask(
        id = db_task.id,
        name = db_task.name,
        status = db_task.status,
        integration_statuses = statuses
    )
    return task
