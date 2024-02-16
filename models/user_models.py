from dataclasses import dataclass

import models.setup_models


@dataclass
class User:
    id: str
    name: str
    setup: models.setup_models.Setup | None = None
    game_id: str | None = None


