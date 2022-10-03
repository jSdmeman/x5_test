import asyncio
import threading
from celery import Celery

from database.database import SessionLocal
from database import crud
from integrations.etherscan import etherscan_status
from integrations.selectel import selectel_status
from config import RETRY_LIMIT_ETHERSCAN, RETRY_LIMIT_SELECTEL


app = Celery(
    'integration_tasks',
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)
app.loop = asyncio.get_event_loop()
app.loop_runner = threading.Thread(
    target = app.loop.run_forever,
    daemon = True
)
app.loop_runner.start()


async def async_etherscan(task_id: int, retry_counter: int):
    integration_name = 'etherscan'
    db = SessionLocal()

    # проверяем лимиты на ретраи
    if retry_counter == RETRY_LIMIT_ETHERSCAN:
        status = 'failed'
        await crud.update_integration_status(db, integration_name, task_id, status)
        await crud.update_integration_task_status(db, task_id, status)
        await db.close()
        return

    retry_counter += 1
    await crud.update_integration_retry_counter(db, integration_name, task_id, retry_counter)

    # делаем запрос и выставляем нужный статус если запрос не прошел
    if not await etherscan_status():
        etherscan_integration.delay(task_id, retry_counter)
        await db.close()
        return

    # обновляем статус интеграции
    status = 'success'
    await crud.update_integration_status(db, integration_name, task_id, status)

    # обновляем статус интеграционной задачи
    all_integrations = await crud.get_integration(db, task_id)
    await db.close()
    for item in all_integrations:
        if item.status != 'success':
            return
    await crud.update_integration_task_status(db, task_id, status)
    return


async def async_selectel(task_id: int, retry_counter: int):
    integration_name = 'selectel'
    db = SessionLocal()

    # проверяем лимиты на ретраи
    if retry_counter == RETRY_LIMIT_SELECTEL:
        status = 'failed'
        await crud.update_integration_status(db, integration_name, task_id, status)
        await crud.update_integration_task_status(db, task_id, status)
        await db.close()
        return

    retry_counter += 1
    await crud.update_integration_retry_counter(db, integration_name, task_id, retry_counter)

    # делаем запрос и выставвляем нужный статус если запрос не проше
    if not await selectel_status():
        selectel_integration.delay(task_id, retry_counter)
        await db.close()
        return

    # обновляем статус интеграции
    status = 'success'
    await crud.update_integration_status(db, integration_name, task_id, status)

    # обновляем статус интеграционной задачи
    all_integrations = await crud.get_integration(db, task_id)
    await db.close()
    for item in all_integrations:
        if item.status != 'success':
            return
    await crud.update_integration_task_status(db, task_id, status)
    return


@app.task
def etherscan_integration(task_id: int, retry_counter:int):
    coro = async_etherscan(task_id, retry_counter)
    asyncio.run_coroutine_threadsafe(
        coro = coro,
        loop = app.loop
    )


@app.task
def selectel_integration(task_id: int, retry_counter:int):
    coro = async_selectel(task_id, retry_counter)
    asyncio.run_coroutine_threadsafe(
        coro = coro,
        loop = app.loop
    )
