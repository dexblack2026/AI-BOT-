# =========================================================
# AI-BOT - PREDICTION ENGINE
# =========================================================

from typing import Any, Dict, List, Optional


class PredictionEngine:

    def __init__(
        self,
        min_confidence: float = 50.0,
    ):
        self.min_confidence = min_confidence

    # =====================================================
    # NEXT PERIOD
    # =====================================================

    def next_period(
        self,
        history: List[Dict[str, Any]],
        current_period: Optional[str] = None,
    ) -> Optional[str]:

        # Current API period ရှိရင်
        # အဲ့ဒီ period ကို အခြေခံပြီး +1
        if current_period is not None:

            try:
                return str(
                    int(current_period) + 1
                )
            except (
                ValueError,
                TypeError,
            ):
                pass

        # History ထဲက နောက်ဆုံး period
        if history:

            periods = []

            for item in history:

                period = item.get(
                    "period"
                )

                if period is None:
                    continue

                try:
                    periods.append(
                        int(period)
                    )
                except (
                    ValueError,
                    TypeError,
                ):
                    continue

            if periods:

                return str(
                    max(periods) + 1
                )

        return None

    # =====================================================
    # NUMBER FROM PATTERN
    # =====================================================

    def pattern_number(
        self,
        pattern: Optional[
            Dict[str, Any]
        ],
    ) -> Optional[int]:

        if not pattern:
            return None

        value = pattern.get(
            "best_number"
        )

        if value is None:
            return None

        try:
            value = int(value)
        except (
            ValueError,
            TypeError,
        ):
            return None

        if 0 <= value <= 9:
            return value

        return None

    # =====================================================
    # NUMBER FROM FORMULA
    # =====================================================

    def formula_number(
        self,
        formula: Optional[
            Dict[str, Any]
        ],
    ) -> Optional[int]:

        if not formula:
            return None

        value = formula.get(
            "prediction"
        )

        if value is None:
            return None

        try:
            value = int(value)
        except (
            ValueError,
            TypeError,
        ):
            return None

        if 0 <= value <= 9:
            return value

        return None

    # =====================================================
    # SCORE
    # =====================================================

    def calculate_scores(
        self,
        pattern: Optional[
            Dict[str, Any]
        ],
        formula: Optional[
            Dict[str, Any]
        ],
        evidence: Optional[
            Dict[str, Any]
        ],
    ) -> Dict[int, float]:

        scores = {
            number: 0.0
            for number in range(10)
        }

        # -------------------------------------------------
        # Pattern
        # -------------------------------------------------

        pattern_number = (
            self.pattern_number(
                pattern
            )
        )

        if pattern_number is not None:

            pattern_strength = float(
                pattern.get(
                    "strength",
                    0,
                )
            )

            scores[
                pattern_number
            ] += (
                pattern_strength
                * 0.40
            )

        # -------------------------------------------------
        # Formula
        # -------------------------------------------------

        formula_number = (
            self.formula_number(
                formula
            )
        )

        if formula_number is not None:

            formula_confidence = float(
                formula.get(
                    "confidence",
                    0,
                )
            )

            scores[
                formula_number
            ] += (
                formula_confidence
                * 0.30
            )

        # -------------------------------------------------
        # Evidence
        # -------------------------------------------------

        evidence_score = 0.0

        if evidence:

            evidence_score = float(
                evidence.get(
                    "evidence_score",
                    0,
                )
            )

        # Evidence ကို
        # Pattern / Formula signal တွေမှာ
        # အနည်းငယ် weight ပေးထားတယ်။

        if pattern_number is not None:

            scores[
                pattern_number
            ] += (
                evidence_score
                * 0.15
            )

        if formula_number is not None:

            scores[
                formula_number
            ] += (
                evidence_score
                * 0.15
            )

        return scores

    # =====================================================
    # FINAL PREDICTION
    # =====================================================

    def predict(
        self,
        history: List[Dict[str, Any]],
        current_period: Optional[str] = None,
        pattern: Optional[
            Dict[str, Any]
        ] = None,
        formula: Optional[
            Dict[str, Any]
        ] = None,
        evidence: Optional[
            Dict[str, Any]
        ] = None,
    ) -> Dict[str, Any]:

        target_period = self.next_period(
            history,
            current_period,
        )

        scores = self.calculate_scores(
            pattern,
            formula,
            evidence,
        )

        sorted_scores = sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        # -------------------------------------------------
        # No signal
        # -------------------------------------------------

        if not sorted_scores:

            return {
                "target_period":
                    target_period,

                "prediction":
                    None,

                "bs":
                    None,

                "confidence":
                    0.0,

                "method":
                    "NO_SIGNAL",

                "scores":
                    {},
            }

        best_number = (
            sorted_scores[0][0]
        )

        best_score = (
            sorted_scores[0][1]
        )

        second_score = (
            sorted_scores[1][1]
            if len(sorted_scores) > 1
            else 0.0
        )

        # -------------------------------------------------
        # Confidence
        # -------------------------------------------------

        total_score = sum(
            scores.values()
        )

        if total_score > 0:

            confidence = (
                best_score
                / total_score
                * 100
            )

        else:

            confidence = 0.0

        # Add separation bonus
        separation = (
            best_score
            - second_score
        )

        confidence += min(
            separation * 0.10,
            10,
        )

        confidence = min(
            99.0,
            max(
                0.0,
                confidence,
            ),
        )

        confidence = round(
            confidence,
            2,
        )

        # -------------------------------------------------
        # Method
        # -------------------------------------------------

        pattern_number = (
            self.pattern_number(
                pattern
            )
        )

        formula_number = (
            self.formula_number(
                formula
            )
        )

        if (
            pattern_number is not None
            and formula_number is not None
            and pattern_number
            == formula_number
        ):

            method = (
                "PATTERN + FORMULA"
            )

        elif pattern_number is not None:

            method = "PATTERN"

        elif formula_number is not None:

            method = "FORMULA"

        else:

            method = "EVIDENCE"

        prediction_bs = (
            "B"
            if best_number >= 5
            else "S"
        )

        return {

            "target_period":
                target_period,

            "prediction":
                best_number,

            "bs":
                prediction_bs,

            "confidence":
                confidence,

            "method":
                method,

            "pattern_number":
                pattern_number,

            "formula_number":
                formula_number,

            "evidence_score":
                (
                    evidence.get(
                        "evidence_score",
                        0,
                    )
                    if evidence
                    else 0
                ),

            "scores":
                {
                    str(number):
                    round(
                        score,
                        2,
                    )
                    for number, score
                    in sorted_scores
                },
        }

    # =====================================================
    # FORMAT FOR TELEGRAM
    # =====================================================

    def format_prediction(
        self,
        result: Dict[str, Any],
    ) -> str:

        period = result.get(
            "target_period"
        ) or "WAITING"

        number = result.get(
            "prediction"
        )

        bs = result.get(
            "bs"
        ) or "-"

        confidence = result.get(
            "confidence",
            0,
        )

        method = result.get(
            "method",
            "UNKNOWN",
        )

        if number is None:
            number_text = "WAITING"
        else:
            number_text = str(number)

        return (
            "🔮 <b>NEXT PREDICTION</b>\n\n"
            f"🎯 Net Period : "
            f"<code>{period}</code>\n\n"
            f"🔢 Number : "
            f"<b>{number_text}</b>\n"
            f"📊 B/S : "
            f"<b>{bs}</b>\n"
            f"🧠 Confidence : "
            f"<b>{confidence:.2f}%</b>\n"
            f"⚙️ Method : "
            f"<code>{method}</code>"
        )


# =========================================================
# HELPER
# =========================================================

def make_prediction(
    history: List[Dict[str, Any]],
    current_period: Optional[str] = None,
    pattern: Optional[
        Dict[str, Any]
    ] = None,
    formula: Optional[
        Dict[str, Any]
    ] = None,
    evidence: Optional[
        Dict[str, Any]
    ] = None,
) -> Dict[str, Any]:

    engine = PredictionEngine()

    return engine.predict(
        history=history,
        current_period=current_period,
        pattern=pattern,
        formula=formula,
        evidence=evidence,
    )
