from typing import Any, Dict, List


class EvidenceEngine:
    """
    Collects and evaluates evidence from different engines.

    Evidence sources:
    - Pattern
    - Formula
    - Backtest
    - Historical trend
    """

    def __init__(self):
        self.sources: List[Dict[str, Any]] = []

    def add(
        self,
        source: str,
        prediction: str,
        confidence: float,
        reason: str = ""
    ):
        evidence = {
            "source": source,
            "prediction": prediction,
            "confidence": float(confidence),
            "reason": reason,
        }

        self.sources.append(evidence)

    def clear(self):
        self.sources.clear()

    def collect(
        self,
        pattern_result: Dict[str, Any] | None = None,
        formula_result: Dict[str, Any] | None = None,
        backtest_result: Dict[str, Any] | None = None,
    ) -> List[Dict[str, Any]]:

        self.clear()

        results = [
            ("pattern", pattern_result),
            ("formula", formula_result),
            ("backtest", backtest_result),
        ]

        for source, result in results:

            if not isinstance(result, dict):
                continue

            prediction = result.get("prediction")

            if prediction is None:
                prediction = result.get("pred")

            confidence = result.get(
                "confidence",
                result.get("conf", 0)
            )

            reason = result.get(
                "reason",
                result.get("name", "")
            )

            if prediction:
                self.add(
                    source=source,
                    prediction=str(prediction),
                    confidence=float(confidence),
                    reason=str(reason)
                )

        return self.sources

    def summarize(self) -> Dict[str, Any]:

        if not self.sources:
            return {
                "prediction": None,
                "confidence": 0,
                "agreement": 0,
                "evidence": [],
            }

        scores: Dict[str, float] = {}
        counts: Dict[str, int] = {}

        for item in self.sources:

            prediction = item["prediction"]
            confidence = item["confidence"]

            scores[prediction] = (
                scores.get(prediction, 0)
                + confidence
            )

            counts[prediction] = (
                counts.get(prediction, 0)
                + 1
            )

        best_prediction = max(
            scores,
            key=scores.get
        )

        total_sources = len(self.sources)

        agreement = (
            counts[best_prediction]
            / total_sources
        ) * 100

        confidence = (
            scores[best_prediction]
            / counts[best_prediction]
        )

        return {
            "prediction": best_prediction,
            "confidence": round(
                min(confidence, 100),
                2
            ),
            "agreement": round(
                agreement,
                2
            ),
            "evidence": self.sources,
        }
