from dataclasses import dataclass

import models.setup_models


@dataclass
class User:
    id: str
    name: str
    setup: models.setup_models.Setup | None = None
    game_id: str | None = None
    elo: int = 1500 * 100  # 1/100th of a point

    def get_rounded_elo(self):
        return round(self.elo / 100)


