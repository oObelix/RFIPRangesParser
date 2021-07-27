from typing import Any
from db_session import engine
import models

collected_data: Any = models.CollectedData()
users: models.Users = models.Users()


if __name__ == "__main__":
    models.Base.metadata.create_all(engine)
