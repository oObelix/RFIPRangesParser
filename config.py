from typing import Dict, Any
import yaml


class Config:
    """
    Read config.yaml variables
    """
    def __init__(self, path: str = "config.yaml"):
        with open(path) as f:
            self.config: Dict[str, Any] = yaml.safe_load(f)

    @property
    def db_server_dsn(self) -> str:
        return self.config['db_server']['DSN']

    @property
    def server_port(self) -> int:
        return self.config.get('server', {}).get('port', 8888)
