from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update

from database import models, schemas


async def get_integration_task(db: AsyncSession, task_id: int):
    result = await db.execute(
        select(models.IntegrationTask).where(models.IntegrationTask.id==task_id)
    )
    return result.scalars().first()


async def update_integration_task_status(db: AsyncSession, task_id: int, status: str):
    await db.execute(
        update(models.IntegrationTask).where(models.IntegrationTask.id==task_id).values(status=status)
    )
    await db.commit()


async def create_integration_task(db: AsyncSession, task: schemas.IntegrationTaskCreate):
    db_task = models.IntegrationTask(name=task.name)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def get_integration(db: AsyncSession, task_id: int):
    result = await db.execute(
        select(models.Integration).where(models.Integration.task_id==task_id)
    )
    return result.scalars().all()


async def update_integration_status(db: AsyncSession, name: str, task_id: int, status: str):
    await db.execute(
        update(models.Integration).where(
            (models.Integration.task_id==task_id) &
            (models.Integration.name==name)
        ).values(status=status)
    )
    await db.commit()


async def update_integration_retry_counter(db: AsyncSession, name: str, task_id: int, retry_counter: int):
    await db.execute(
        update(models.Integration).where(
            (models.Integration.task_id==task_id) &
            (models.Integration.name==name)
        ).values(retry_counter=retry_counter)
    )
    await db.commit()


async def create_integration(db: AsyncSession, task_id: int, integration: schemas.IntegrationCreate):
    db_integration = models.Integration(**integration.dict(), task_id=task_id)
    db.add(db_integration)
    await db.commit()
    await db.refresh(db_integration)
    return db_integration