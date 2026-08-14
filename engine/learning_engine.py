from collections import defaultdict
from typing import Any, Dict, List


class LearningEngine:

    def __init__(self):

        self.source_stats = defaultdict(
            lambda: {
                "wins": 0,
                "losses": 0,
                "total": 0,
            }
        )

        self.pattern_stats = defaultdict(
            lambda: {
                "wins": 0,
                "losses": 0,
                "total": 0,
            }
        )

    def record_source_result(
        self,
        source: str,
        prediction: str,
        actual: str
    ):

        stats = self.source_stats[
            source
        ]

        stats["total"] += 1

        if (
            str(prediction).lower()
            == str(actual).lower()
        ):
            stats["wins"] += 1
        else:
            stats["losses"] += 1

    def record_pattern_result(
        self,
        pattern: str,
        prediction: str,
        actual: str
    ):

        stats = self.pattern_stats[
            pattern
        ]

        stats["total"] += 1

        if (
            str(prediction).lower()
            == str(actual).lower()
        ):
            stats["wins"] += 1
        else:
            stats["losses"] += 1

    @staticmethod
    def accuracy(
        stats: Dict[str, int]
    ) -> float:

        total = stats.get(
            "total",
            0
        )

        if total == 0:
            return 0.0

        return (
            stats.get("wins", 0)
            / total
        ) * 100

    def get_source_score(
        self,
        source: str
    ) -> float:

        stats = self.source_stats.get(
            source
        )

        if not stats:
            return 50.0

        return self.accuracy(stats)

    def get_pattern_score(
        self,
        pattern: str
    ) -> float:

        stats = self.pattern_stats.get(
            pattern
        )

        if not stats:
            return 50.0

        return self.accuracy(stats)

    def rank_sources(self) -> List[Dict[str, Any]]:

        result = []

        for source, stats in (
            self.source_stats.items()
        ):

            result.append({
                "source": source,
                "total": stats["total"],
                "wins": stats["wins"],
                "losses": stats["losses"],
                "accuracy": round(
                    self.accuracy(stats),
                    2
                ),
            })

        return sorted(
            result,
            key=lambda x: x["accuracy"],
            reverse=True
        )

    def rank_patterns(self) -> List[Dict[str, Any]]:

        result = []

        for pattern, stats in (
            self.pattern_stats.items()
        ):

            result.append({
                "pattern": pattern,
                "total": stats["total"],
                "wins": stats["wins"],
                "losses": stats["losses"],
                "accuracy": round(
                    self.accuracy(stats),
                    2
                ),
            })

        return sorted(
            result,
            key=lambda x: x["accuracy"],
            reverse=True
        )

    def learn_from_prediction(
        self,
        prediction_result: Dict[str, Any],
        actual: str
    ):

        evidence = prediction_result.get(
            "evidence",
            []
        )

        for item in evidence:

            source = item.get(
                "source",
                "unknown"
            )

            prediction = item.get(
                "prediction"
            )

            if prediction is None:
                continue

            self.record_source_result(
                source,
                prediction,
                actual
            )

    def get_report(self) -> Dict[str, Any]:

        return {
            "sources": self.rank_sources(),
            "patterns": self.rank_patterns(),
        }
