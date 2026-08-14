import json
from pathlib import Path
from typing import Any, Dict, List

from config import Config


class MemoryEngine:

    def __init__(
        self,
        file_path=None
    ):
        self.file_path = Path(
            file_path or Config.HISTORY_FILE
        )

        self.data = self._load()

    def _default_data(self):
        return {
            "games": [],
            "predictions": [],
            "stats": {
                "total": 0,
                "wins": 0,
                "losses": 0,
            },
        }

    def _load(self) -> Dict[str, Any]:

        if not self.file_path.exists():
            return self._default_data()

        try:
            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            if not isinstance(data, dict):
                return self._default_data()

            return data

        except (
            json.JSONDecodeError,
            OSError
        ):
            return self._default_data()

    def save(self):

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.data,
                file,
                ensure_ascii=False,
                indent=2
            )

    def add_game(
        self,
        game: Dict[str, Any]
    ):

        games = self.data.setdefault(
            "games",
            []
        )

        games.append(game)

        max_history = Config.MAX_HISTORY

        if len(games) > max_history:
            del games[:-max_history]

        self.save()

    def add_prediction(
        self,
        prediction: Dict[str, Any]
    ):

        predictions = self.data.setdefault(
            "predictions",
            []
        )

        predictions.append(prediction)

        if len(predictions) > Config.MAX_HISTORY:
            del predictions[:-Config.MAX_HISTORY]

        self.save()

    def update_result(
        self,
        prediction: str,
        actual: str
    ) -> bool:

        predictions = self.data.setdefault(
            "predictions",
            []
        )

        matched = None

        for item in reversed(predictions):

            if (
                item.get("result")
                is None
            ):
                matched = item
                break

        if matched is None:
            return False

        matched["actual"] = actual

        is_win = (
            str(prediction).lower()
            == str(actual).lower()
        )

        matched["result"] = (
            "win" if is_win else "loss"
        )

        stats = self.data.setdefault(
            "stats",
            {
                "total": 0,
                "wins": 0,
                "losses": 0,
            }
        )

        stats["total"] += 1

        if is_win:
            stats["wins"] += 1
        else:
            stats["losses"] += 1

        self.save()

        return is_win

    def get_games(
        self,
        limit: int = 100
    ) -> List[Dict[str, Any]]:

        return self.data.get(
            "games",
            []
        )[-limit:]

    def get_predictions(
        self,
        limit: int = 100
    ) -> List[Dict[str, Any]]:

        return self.data.get(
            "predictions",
            []
        )[-limit:]

    def get_stats(self) -> Dict[str, Any]:

        stats = self.data.get(
            "stats",
            {}
        )

        total = stats.get(
            "total",
            0
        )

        wins = stats.get(
            "wins",
            0
        )

        win_rate = (
            (wins / total) * 100
            if total > 0
            else 0
        )

        return {
            **stats,
            "win_rate": round(
                win_rate,
                2
            ),
        }
