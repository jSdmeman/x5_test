### для запуска
```console
python -m celery -A integrator worker -P gevent
uvicorn main:app --reload
```

### app.env
Так же для запуска должен быть файл app.env в который подставить нужные значения
```code
PG_USER=''
PG_PASS=''
PG_HOST=''
PG_NAME=''
RETRY_LIMIT_ETHERSCAN=5
RETRY_LIMIT_SELECTEL=5
ETHERSCAN_TOKEN=''
```
