# =========================================================
# AI-BOT - FORMULA ENGINE
# =========================================================

from collections import Counter
from typing import Any, Dict, List, Optional


class FormulaEngine:

    def __init__(self):
        pass

    # =====================================================
    # NORMALIZE
    # =====================================================

    def normalize(
        self,
        history: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:

        result = []

        for item in history:

            if not isinstance(item, dict):
                continue

            number = item.get("number")

            if number is None:
                continue

            try:
                number = int(number)
            except (ValueError, TypeError):
                continue

            if number < 0 or number > 9:
                continue

            bs = item.get("bs")

            if bs not in ("B", "S"):
                bs = "B" if number >= 5 else "S"

            result.append({
                "period": str(
                    item.get("period", "")
                ),
                "number": number,
                "bs": bs,
                "time": item.get("time"),
            })

        return result

    # =====================================================
    # NUMBER FREQUENCY
    # =====================================================

    def number_frequency(
        self,
        history: List[Dict[str, Any]],
    ) -> Dict[int, int]:

        counter = Counter()

        for item in history:

            number = item.get("number")

            if number is not None:
                counter[int(number)] += 1

        return dict(counter)

    # =====================================================
    # RECENT NUMBERS
    # =====================================================

    def recent_numbers(
        self,
        history: List[Dict[str, Any]],
        limit: int = 20,
    ) -> List[int]:

        history = self.normalize(history)

        return [
            item["number"]
            for item in history[-limit:]
        ]

    # =====================================================
    # COLD NUMBERS
    # =====================================================

    def cold_numbers(
        self,
        history: List[Dict[str, Any]],
    ) -> List[int]:

        frequency = self.number_frequency(
            history
        )

        numbers = list(range(10))

        return sorted(
            numbers,
            key=lambda number: frequency.get(
                number,
                0,
            ),
        )

    # =====================================================
    # HOT NUMBERS
    # =====================================================

    def hot_numbers(
        self,
        history: List[Dict[str, Any]],
    ) -> List[int]:

        frequency = self.number_frequency(
            history
        )

        numbers = list(range(10))

        return sorted(
            numbers,
            key=lambda number: frequency.get(
                number,
                0,
            ),
            reverse=True,
        )

    # =====================================================
    # RECENT BS
    # =====================================================

    def recent_bs(
        self,
        history: List[Dict[str, Any]],
        limit: int = 10,
    ) -> str:

        history = self.normalize(history)

        return "".join(
            item["bs"]
            for item in history[-limit:]
        )

    # =====================================================
    # BS COUNTS
    # =====================================================

    def bs_counts(
        self,
        history: List[Dict[str, Any]],
    ) -> Dict[str, int]:

        counter = Counter()

        for item in history:

            bs = item.get("bs")

            if bs in ("B", "S"):
                counter[bs] += 1

        return {
            "B": counter.get("B", 0),
            "S": counter.get("S", 0),
        }

    # =====================================================
    # ODD / EVEN
    # =====================================================

    def odd_even_counts(
        self,
        history: List[Dict[str, Any]],
    ) -> Dict[str, int]:

        odd = 0
        even = 0

        for item in history:

            number = item.get("number")

            if number is None:
                continue

            if int(number) % 2 == 0:
                even += 1
            else:
                odd += 1

        return {
            "odd": odd,
            "even": even,
        }

    # =====================================================
    # SIMPLE FORMULA
    # =====================================================

    def calculate(
        self,
        history: List[Dict[str, Any]],
    ) -> Optional[Dict[str, Any]]:

        history = self.normalize(history)

        if not history:
            return None

        recent = self.recent_numbers(
            history,
            limit=10,
        )

        if not recent:
            return None

        frequency = self.number_frequency(
            history
        )

        bs = self.bs_counts(
            history
        )

        odd_even = self.odd_even_counts(
            history
        )

        # -------------------------------------------------
        # Weighted score
        # -------------------------------------------------

        scores = {
            number: 0.0
            for number in range(10)
        }

        # Historical frequency
        max_frequency = max(
            frequency.values()
        ) if frequency else 1

        for number in range(10):

            freq = frequency.get(
                number,
                0,
            )

            scores[number] += (
                freq
                / max_frequency
                * 30
            )

        # Recent activity
        recent_counter = Counter(
            recent
        )

        max_recent = max(
            recent_counter.values()
        ) if recent_counter else 1

        for number in range(10):

            recent_count = (
                recent_counter.get(
                    number,
                    0,
                )
            )

            scores[number] += (
                recent_count
                / max_recent
                * 40
            )

        # -------------------------------------------------
        # Small recency adjustment
        # -------------------------------------------------

        if recent:

            last_number = recent[-1]

            # Avoid simply repeating the
            # immediately previous number.
            scores[last_number] -= 5

        # -------------------------------------------------
        # Best number
        # -------------------------------------------------

        prediction = max(
            scores,
            key=scores.get,
        )

        sorted_scores = sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        best_score = sorted_scores[0][1]

        second_score = (
            sorted_scores[1][1]
            if len(sorted_scores) > 1
            else 0
        )

        # -------------------------------------------------
        # Confidence
        # -------------------------------------------------

        difference = (
            best_score
            - second_score
        )

        confidence = min(
            95.0,
            50.0 + difference * 3,
        )

        confidence = round(
            confidence,
            2,
        )

        prediction_bs = (
            "B"
            if prediction >= 5
            else "S"
        )

        return {

            "prediction":
                prediction,

            "bs":
                prediction_bs,

            "confidence":
                confidence,

            "scores":
                {
                    str(number):
                        round(
                            score,
                            2,
                        )
                    for number, score
                    in scores.items()
                },

            "recent_numbers":
                recent,

            "recent_bs":
                self.recent_bs(
                    history
                ),

            "number_frequency":
                frequency,

            "bs_counts":
                bs,

            "odd_even":
                odd_even,
        }


# =========================================================
# HELPER
# =========================================================

def calculate_formula(
    history: List[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:

    engine = FormulaEngine()

    return engine.calculate(
        history
    )
