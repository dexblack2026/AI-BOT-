from typing import Any, Dict, List, Optional


class PredictionEngine:

    def __init__(
        self,
        evidence_engine=None,
        memory_engine=None
    ):
        self.evidence_engine = (
            evidence_engine
        )

        self.memory_engine = (
            memory_engine
        )

    def predict(
        self,
        pattern_result: Optional[Dict[str, Any]] = None,
        formula_result: Optional[Dict[str, Any]] = None,
        backtest_result: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        if self.evidence_engine is None:
            raise ValueError(
                "EvidenceEngine is required."
            )

        evidence = (
            self.evidence_engine.collect(
                pattern_result,
                formula_result,
                backtest_result
            )
        )

        summary = (
            self.evidence_engine.summarize()
        )

        prediction = summary.get(
            "prediction"
        )

        confidence = summary.get(
            "confidence",
            0
        )

        result = {
            "prediction": prediction,
            "confidence": confidence,
            "agreement": summary.get(
                "agreement",
                0
            ),
            "evidence": evidence,
        }

        if self.memory_engine:

            self.memory_engine.add_prediction({
                "prediction": prediction,
                "confidence": confidence,
                "agreement": result[
                    "agreement"
                ],
                "evidence": evidence,
            })

        return result

    @staticmethod
    def format_result(
        result: Dict[str, Any]
    ) -> str:

        prediction = result.get(
            "prediction",
            "N/A"
        )

        confidence = result.get(
            "confidence",
            0
        )

        agreement = result.get(
            "agreement",
            0
        )

        return (
            f"Prediction: {prediction}\n"
            f"Confidence: {confidence:.2f}%\n"
            f"Agreement: {agreement:.2f}%"
        )
