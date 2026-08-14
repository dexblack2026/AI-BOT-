# =========================================================
# AI-BOT - PREDICTION ENGINE
# =========================================================

import logging
from typing import Dict, List, Optional


logger = logging.getLogger("PredictionEngine")


class PredictionEngine:

    def __init__(
        self,
        minimum_confidence: float = 50.0,
    ):

        self.minimum_confidence = (
            minimum_confidence
        )

    # =====================================================
    # PERIOD
    # =====================================================

    @staticmethod
    def next_period(
        current_period: Optional[str],
    ) -> Optional[str]:

        if current_period is None:
            return None

        value = str(
            current_period
        ).strip()

        if not value:
            return None

        # Numeric period
        try:

            return str(
                int(value) + 1
            )

        except ValueError:

            pass

        # If period contains a numeric suffix,
        # increment the suffix.
        digits = ""

        for char in reversed(value):

            if char.isdigit():

                digits = (
                    char + digits
                )

            else:

                break

        if digits:

            prefix = value[
                :-len(digits)
            ]

            try:

                return (
                    prefix
                    + str(
                        int(digits) + 1
                    )
                )

            except ValueError:

                return None

        return None

    # =====================================================
    # B/S TEXT
    # =====================================================

    @staticmethod
    def prediction_text(
        prediction: Optional[str],
    ) -> str:

        if prediction == "B":
            return "🔴 BIG"

        if prediction == "S":
            return "🔵 SMALL"

        return "⚠️ NO SIGNAL"

    # =====================================================
    # SIGNAL SCORE
    # =====================================================

    @staticmethod
    def signal_score(
        evidence: Optional[Dict],
    ) -> float:

        if not evidence:
            return 0.0

        try:

            return float(
                evidence.get(
                    "confidence",
                    0.0,
                )
            )

        except (
            ValueError,
            TypeError,
        ):

            return 0.0

    # =====================================================
    # MEMORY SUPPORT
    # =====================================================

    @staticmethod
    def memory_support(
        memory: Optional[Dict],
        prediction: Optional[str],
    ) -> Dict:

        if not memory or not prediction:

            return {
                "samples": 0,
                "accuracy": 0.0,
                "support": False,
            }

        samples = int(
            memory.get(
                "samples",
                0,
            )
        )

        accuracy = float(
            memory.get(
                "accuracy",
                0.0,
            )
        )

        support = (
            samples >= 3
            and accuracy >= 50.0
        )

        return {

            "samples":
                samples,

            "accuracy":
                round(
                    accuracy,
                    2,
                ),

            "support":
                support,

        }

    # =====================================================
    # BUILD FINAL PREDICTION
    # =====================================================

    def predict(
        self,
        current_period: Optional[str],
        evidence: Optional[Dict],
        pattern_memory: Optional[Dict] = None,
        formula_memory: Optional[Dict] = None,
        pattern: Optional[str] = None,
        formula_key: Optional[str] = None,
    ) -> Dict:

        # -------------------------------------------------
        # Next Period
        # -------------------------------------------------

        next_period = self.next_period(
            current_period
        )

        # -------------------------------------------------
        # Evidence
        # -------------------------------------------------

        evidence_prediction = None

        if evidence:

            value = evidence.get(
                "prediction"
            )

            if value in ("B", "S"):

                evidence_prediction = value

        evidence_confidence = (
            self.signal_score(
                evidence
            )
        )

        # -------------------------------------------------
        # Memory
        # -------------------------------------------------

        pattern_mem = (
            self.memory_support(
                pattern_memory,
                evidence_prediction,
            )
        )

        formula_mem = (
            self.memory_support(
                formula_memory,
                evidence_prediction,
            )
        )

        # -------------------------------------------------
        # Base confidence
        # -------------------------------------------------

        confidence = (
            evidence_confidence
        )

        # Small memory bonus only when
        # memory has enough samples.
        if pattern_mem["support"]:

            confidence += 2.0

        if formula_mem["support"]:

            confidence += 2.0

        confidence = round(
            min(
                100.0,
                confidence,
            ),
            2,
        )

        # -------------------------------------------------
        # Final status
        # -------------------------------------------------

        if not evidence_prediction:

            status = "NO_SIGNAL"

        elif confidence >= 70.0:

            status = "STRONG"

        elif confidence >= (
            self.minimum_confidence
        ):

            status = "MODERATE"

        else:

            status = "WEAK"

        # -------------------------------------------------
        # Method
        # -------------------------------------------------

        if evidence:

            signals = evidence.get(
                "signals",
                {},
            )

        else:

            signals = {}

        method_parts = []

        if "pattern" in signals:
            method_parts.append(
                "PATTERN"
            )

        if "formula" in signals:
            method_parts.append(
                "FORMULA"
            )

        if not method_parts:

            method = "NO_EVIDENCE"

        else:

            method = "+".join(
                method_parts
            )

        # -------------------------------------------------
        # Final result
        # -------------------------------------------------

        result = {

            "current_period":
                current_period,

            "next_period":
                next_period,

            "prediction":
                evidence_prediction,

            "prediction_text":
                self.prediction_text(
                    evidence_prediction
                ),

            "confidence":
                confidence,

            "status":
                status,

            "method":
                method,

            "pattern":
                pattern,

            "formula_key":
                formula_key,

            "evidence":
                evidence or {},

            "memory": {

                "pattern":
                    pattern_mem,

                "formula":
                    formula_mem,

            },

        }

        logger.info(
            "Prediction | "
            "current=%s | next=%s | "
            "prediction=%s | confidence=%.2f",
            current_period,
            next_period,
            evidence_prediction,
            confidence,
        )

        return result

    # =====================================================
    # DISPLAY DATA
    # =====================================================

    @staticmethod
    def display_data(
        result: Dict,
    ) -> Dict:

        return {

            "period":
                result.get(
                    "next_period"
                ),

            "prediction":
                result.get(
                    "prediction_text",
                    "⚠️ NO SIGNAL",
                ),

            "confidence":
                f'{result.get("confidence", 0.0):.2f}%',

            "method":
                result.get(
                    "method",
                    "NO_EVIDENCE",
                ),

            "status":
                result.get(
                    "status",
                    "UNKNOWN",
                ),

        }
