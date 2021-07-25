from typing import Dict
import yaml


class Config:
    """
    Read config.yaml variables
    """
    def __init__(self, path: str = "config.yaml"):
        with open(path) as f:
            self.config: Dict[str] = yaml.safe_load(f)

    @property
    def db_name(self) -> str:
        return self.db_user

    @property
    def db_user(self) -> str:
        return self.config['services']['db']['environment']['POSTGRES_USER']

    @property
    def db_pass(self) -> str:
        return self.config['services']['db']['environment'][
            'POSTGRES_PASSWORD']

    @property
    def server_port(self) -> int:
        return self.config.get('server', {}).get('port', 8888)
