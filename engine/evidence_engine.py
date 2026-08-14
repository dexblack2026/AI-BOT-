# =========================================================
# AI-BOT - EVIDENCE ENGINE
# =========================================================

import logging
from typing import Dict, Optional


logger = logging.getLogger("EvidenceEngine")


class EvidenceEngine:

    # =====================================================
    # INIT
    # =====================================================

    def __init__(
        self,
        minimum_confidence: float = 50.0,
        strong_confidence: float = 70.0,
    ):

        self.minimum_confidence = (
            minimum_confidence
        )

        self.strong_confidence = (
            strong_confidence
        )

    # =====================================================
    # NORMALIZE PREDICTION
    # =====================================================

    @staticmethod
    def normalize_prediction(
        value: Optional[str],
    ) -> Optional[str]:

        if value is None:
            return None

        value = str(
            value
        ).upper().strip()

        if value in ("B", "S"):
            return value

        return None

    # =====================================================
    # ADD SIGNAL
    # =====================================================

    def add_signal(
        self,
        signals: Dict,
        name: str,
        prediction: Optional[str],
        confidence: float,
        samples: int = 0,
    ):

        prediction = (
            self.normalize_prediction(
                prediction
            )
        )

        if prediction is None:
            return

        try:
            confidence = float(
                confidence
            )
        except (
            ValueError,
            TypeError,
        ):
            confidence = 0.0

        signals[name] = {

            "prediction":
                prediction,

            "confidence":
                round(
                    max(
                        0.0,
                        min(
                            100.0,
                            confidence,
                        ),
                    ),
                    2,
                ),

            "samples":
                int(samples),

        }

    # =====================================================
    # COLLECT SIGNALS
    # =====================================================

    def collect(
        self,
        pattern_result: Optional[Dict],
        formula_result: Optional[Dict],
        backtest_result: Optional[Dict],
    ) -> Dict:

        signals = {}

        # =================================================
        # PATTERN SIGNAL
        # =================================================

        if pattern_result:

            bs_result = (
                pattern_result.get(
                    "bs"
                )
            )

            if bs_result:

                self.add_signal(

                    signals,

                    "pattern",

                    bs_result.get(
                        "prediction"
                    ),

                    bs_result.get(
                        "confidence",
                        0.0,
                    ),

                    bs_result.get(
                        "matches",
                        0,
                    ),
                )

        # =================================================
        # FORMULA SIGNAL
        # =================================================

        if formula_result:

            analysis = (
                formula_result.get(
                    "analysis",
                    {},
                )
            )

            rule_stats = (
                formula_result.get(
                    "rule_stats",
                    {},
                )
            )

            self.add_signal(

                signals,

                "formula",

                analysis.get(
                    "prediction"
                ),

                rule_stats.get(
                    "accuracy",
                    0.0,
                ),

                rule_stats.get(
                    "samples",
                    0,
                ),
            )

        # =================================================
        # BACKTEST PATTERN
        # =================================================

        if backtest_result:

            pattern_stats = (
                backtest_result.get(
                    "pattern",
                    {},
                )
            )

            # Backtest pattern itself does not contain
            # a current prediction, so this signal is
            # only used as historical reliability.
            #
            # Current pattern prediction comes from
            # pattern_result.

            if "pattern" in signals:

                signals["pattern"][
                    "backtest_accuracy"
                ] = pattern_stats.get(
                    "accuracy",
                    0.0,
                )

        # =================================================
        # BACKTEST FORMULA
        # =================================================

        if "formula" in signals:

            formula_stats = (
                backtest_result.get(
                    "formula",
                    {},
                )
                if backtest_result
                else {}
            )

            signals["formula"][
                "backtest_accuracy"
            ] = formula_stats.get(
                "accuracy",
                0.0,
            )

        return signals

    # =====================================================
    # SCORE SIGNAL
    # =====================================================

    def score_signal(
        self,
        signal: Dict,
    ) -> float:

        confidence = float(
            signal.get(
                "confidence",
                0.0,
            )
        )

        backtest_accuracy = float(
            signal.get(
                "backtest_accuracy",
                confidence,
            )
        )

        samples = int(
            signal.get(
                "samples",
                0,
            )
        )

        # ---------------------------------------------
        # Main confidence
        # ---------------------------------------------

        score = (
            confidence * 0.60
            + backtest_accuracy * 0.40
        )

        # ---------------------------------------------
        # Small sample penalty
        # ---------------------------------------------

        if samples < 3:

            score *= 0.70

        elif samples < 5:

            score *= 0.85

        elif samples < 10:

            score *= 0.95

        return round(
            max(
                0.0,
                min(
                    100.0,
                    score,
                ),
            ),
            2,
        )

    # =====================================================
    # BUILD EVIDENCE
    # =====================================================

    def build(
        self,
        pattern_result: Optional[Dict],
        formula_result: Optional[Dict],
        backtest_result: Optional[Dict],
    ) -> Dict:

        signals = self.collect(
            pattern_result,
            formula_result,
            backtest_result,
        )

        if not signals:

            return {

                "prediction":
                    None,

                "confidence":
                    0.0,

                "status":
                    "NO_EVIDENCE",

                "signals":
                    {},

                "support":
                    {},

                "conflict":
                    False,

            }

        # =================================================
        # SCORE EACH SIGNAL
        # =================================================

        for name, signal in signals.items():

            signal["score"] = (
                self.score_signal(
                    signal
                )
            )

        # =================================================
        # GROUP BY B / S
        # =================================================

        support = {

            "B": {
                "signals": [],
                "score": 0.0,
            },

            "S": {
                "signals": [],
                "score": 0.0,
            },

        }

        for name, signal in signals.items():

            prediction = signal[
                "prediction"
            ]

            score = signal[
                "score"
            ]

            support[
                prediction
            ]["signals"].append(
                name
            )

            support[
                prediction
            ]["score"] += score

        # =================================================
        # ROUND SCORES
        # =================================================

        support["B"]["score"] = round(
            support["B"]["score"],
            2,
        )

        support["S"]["score"] = round(
            support["S"]["score"],
            2,
        )

        # =================================================
        # FINAL SIDE
        # =================================================

        b_score = support[
            "B"
        ]["score"]

        s_score = support[
            "S"
        ]["score"]

        if b_score > s_score:

            prediction = "B"

            winning_score = b_score
            losing_score = s_score

        elif s_score > b_score:

            prediction = "S"

            winning_score = s_score
            losing_score = b_score

        else:

            prediction = None

            winning_score = 0.0
            losing_score = 0.0

        # =================================================
        # EVIDENCE CONFIDENCE
        # =================================================

        total_score = (
            b_score + s_score
        )

        if prediction and total_score > 0:

            confidence = (
                winning_score
                / total_score
                * 100.0
            )

        else:

            confidence = 0.0

        # =================================================
        # CONFLICT
        # =================================================

        conflict = (
            b_score > 0
            and s_score > 0
        )

        # =================================================
        # STATUS
        # =================================================

        if not prediction:

            status = "NEUTRAL"

        elif confidence >= (
            self.strong_confidence
        ):

            status = "STRONG"

        elif confidence >= (
            self.minimum_confidence
        ):

            status = "MODERATE"

        else:

            status = "WEAK"

        result = {

            "prediction":
                prediction,

            "confidence":
                round(
                    confidence,
                    2,
                ),

            "status":
                status,

            "signals":
                signals,

            "support":
                support,

            "conflict":
                conflict,

            "winning_score":
                round(
                    winning_score,
                    2,
                ),

            "losing_score":
                round(
                    losing_score,
                    2,
                ),

        }

        logger.info(
            "Evidence | prediction=%s | "
            "confidence=%.2f | status=%s",
            prediction,
            confidence,
            status,
        )

        return result

    # =====================================================
    # SUMMARY
    # =====================================================

    @staticmethod
    def summary(
        evidence: Dict,
    ) -> str:

        prediction = evidence.get(
            "prediction"
        )

        confidence = evidence.get(
            "confidence",
            0.0,
        )

        status = evidence.get(
            "status",
            "UNKNOWN",
        )

        if prediction == "B":
            prediction_text = "BIG"

        elif prediction == "S":
            prediction_text = "SMALL"

        else:
            prediction_text = "N/A"

        return (
            f"Prediction={prediction_text} | "
            f"Confidence={confidence:.2f}% | "
            f"Status={status}"
        )
