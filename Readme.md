## Russian Federation IP Address Ranges Parser

Parser for page: (https://lite.ip2location.com/russian-federation-ip-address-ranges)

### Requirements
- Python 3.7.5+ 
- Tornado 6.0.4+
- SQLAlchemy 1.3.20+ 
- PostgreSQL 11+

### Install
- rename `config.example.yaml` to `config.yaml` and edit it (you will need DB_HOST, DB_USER, DB_PASS, DB_NAME for your database server).
- to install dependencies `pip install -r requirements.txt`
- grab data `python run_scraper.py`

### Run server
- `python run_api.py`
