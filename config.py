from dotenv import dotenv_values


config = dotenv_values('app.env')
PG_USER = config['PG_USER']
PG_PASS = config['PG_PASS']
PG_HOST = config['PG_HOST']
PG_NAME = config['PG_NAME']
RETRY_LIMIT_ETHERSCAN = int(config['RETRY_LIMIT_ETHERSCAN'])
RETRY_LIMIT_SELECTEL = int(config['RETRY_LIMIT_SELECTEL'])
ETHERSCAN_TOKEN = config['ETHERSCAN_TOKEN']
