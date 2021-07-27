## Russian Federation IP Address Ranges Parser

Parser IP ranges from page: https://lite.ip2location.com/russian-federation-ip-address-ranges

### Requirements
* Python 3.7.5+
* Tornado 6.1.4+
* SQLAlchemy 1.3.20+
* PostgreSQL 11+

### Installation
* Copy `config.example.yaml` to `config.yaml` and modify it. You must change DB_HOST, DB_USER, DB_PASS, DB_NAME and JWT_SECRET.
* install python dependencies: `pip install -r requirements.txt`
* install `pip install psycopg2-binary` db driver
* deploy database : `python db_init.py`

### Fetching data
You must run script for fetching data for correct working API: `python run_scraper.py`

### Serve API
* `python run_api.py`
