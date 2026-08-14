# =========================================================
# AI-BOT - EVIDENCE ENGINE
# =========================================================

from typing import Any, Dict, Optional


class EvidenceEngine:

    def __init__(
        self,
        pattern_weight: float = 0.30,
        formula_weight: float = 0.25,
        backtest_weight: float = 0.25,
        history_weight: float = 0.20,
    ):

        self.pattern_weight = pattern_weight
        self.formula_weight = formula_weight
        self.backtest_weight = backtest_weight
        self.history_weight = history_weight

    # =====================================================
    # SAFE VALUE
    # =====================================================

    def safe_float(
        self,
        value: Any,
    ) -> float:

        try:
            return float(value)
        except (
            ValueError,
            TypeError,
        ):
            return 0.0

    # =====================================================
    # PATTERN SCORE
    # =====================================================

    def pattern_score(
        self,
        pattern: Optional[Dict[str, Any]],
    ) -> float:

        if not pattern:
            return 0.0

        strength = self.safe_float(
            pattern.get(
                "strength",
                0,
            )
        )

        rate = self.safe_float(
            pattern.get(
                "number_rate",
                0,
            )
        )

        matches = self.safe_float(
            pattern.get(
                "match_count",
                0,
            )
        )

        # Pattern strength
        score = (
            strength * 0.60
            + rate * 0.30
            + min(
                matches * 2,
                10,
            )
        )

        return min(
            100.0,
            round(
                score,
                2,
            ),
        )

    # =====================================================
    # FORMULA SCORE
    # =====================================================

    def formula_score(
        self,
        formula: Optional[Dict[str, Any]],
    ) -> float:

        if not formula:
            return 0.0

        confidence = self.safe_float(
            formula.get(
                "confidence",
                0,
            )
        )

        return min(
            100.0,
            round(
                confidence,
                2,
            ),
        )

    # =====================================================
    # BACKTEST SCORE
    # =====================================================

    def backtest_score(
        self,
        backtest: Optional[
            Dict[str, Any]
        ],
    ) -> float:

        if not backtest:
            return 0.0

        combined = backtest.get(
            "combined",
            {},
        )

        accuracy = self.safe_float(
            combined.get(
                "accuracy",
                0,
            )
        )

        return min(
            100.0,
            round(
                accuracy,
                2,
            ),
        )

    # =====================================================
    # HISTORY SCORE
    # =====================================================

    def history_score(
        self,
        history_count: int,
    ) -> float:

        try:
            count = int(
                history_count
            )
        except (
            ValueError,
            TypeError,
        ):
            count = 0

        # More historical data gives
        # more stable evidence.
        if count >= 1000:
            return 100.0

        if count >= 500:
            return 90.0

        if count >= 200:
            return 80.0

        if count >= 100:
            return 70.0

        if count >= 50:
            return 60.0

        if count >= 20:
            return 50.0

        if count >= 10:
            return 40.0

        return 20.0

    # =====================================================
    # FINAL EVIDENCE
    # =====================================================

    def calculate(
        self,
        pattern: Optional[
            Dict[str, Any]
        ],
        formula: Optional[
            Dict[str, Any]
        ],
        backtest: Optional[
            Dict[str, Any]
        ],
        history_count: int,
    ) -> Dict[str, Any]:

        pattern_score = (
            self.pattern_score(
                pattern
            )
        )

        formula_score = (
            self.formula_score(
                formula
            )
        )

        backtest_score = (
            self.backtest_score(
                backtest
            )
        )

        history_score = (
            self.history_score(
                history_count
            )
        )

        final_score = (

            pattern_score
            * self.pattern_weight

            + formula_score
            * self.formula_weight

            + backtest_score
            * self.backtest_weight

            + history_score
            * self.history_weight
        )

        final_score = min(
            100.0,
            max(
                0.0,
                final_score,
            ),
        )

        # -------------------------------------------------
        # Evidence level
        # -------------------------------------------------

        if final_score >= 80:
            level = "VERY_STRONG"

        elif final_score >= 70:
            level = "STRONG"

        elif final_score >= 60:
            level = "MEDIUM"

        elif final_score >= 50:
            level = "WEAK"

        else:
            level = "LOW"

        return {

            "pattern_score":
                round(
                    pattern_score,
                    2,
                ),

            "formula_score":
                round(
                    formula_score,
                    2,
                ),

            "backtest_score":
                round(
                    backtest_score,
                    2,
                ),

            "history_score":
                round(
                    history_score,
                    2,
                ),

            "evidence_score":
                round(
                    final_score,
                    2,
                ),

            "level":
                level,
        }


# =========================================================
# HELPER
# =========================================================

def calculate_evidence(
    pattern: Optional[
        Dict[str, Any]
    ],
    formula: Optional[
        Dict[str, Any]
    ],
    backtest: Optional[
        Dict[str, Any]
    ],
    history_count: int,
) -> Dict[str, Any]:

    engine = EvidenceEngine()

    return engine.calculate(
        pattern=pattern,
        formula=formula,
        backtest=backtest,
        history_count=history_count,
    )
