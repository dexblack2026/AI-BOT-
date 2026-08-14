# =========================================================
# AI-BOT - BACKTEST ENGINE
# =========================================================

from collections import Counter
from typing import Any, Dict, List, Optional


class BacktestEngine:

    def __init__(
        self,
        min_samples: int = 10,
    ):
        self.min_samples = max(
            1,
            min_samples,
        )

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

            if not 0 <= number <= 9:
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
    # B/S PREDICTION
    # =====================================================

    def predict_bs(
        self,
        history: List[Dict[str, Any]],
        lookback: int = 5,
    ) -> Optional[str]:

        if len(history) < lookback:
            return None

        recent = history[-lookback:]

        counter = Counter(
            item["bs"]
            for item in recent
        )

        if not counter:
            return None

        return max(
            counter,
            key=counter.get,
        )

    # =====================================================
    # NUMBER PREDICTION
    # =====================================================

    def predict_number(
        self,
        history: List[Dict[str, Any]],
        lookback: int = 20,
    ) -> Optional[int]:

        if not history:
            return None

        recent = history[-lookback:]

        counter = Counter(
            item["number"]
            for item in recent
        )

        if not counter:
            return None

        return max(
            counter,
            key=counter.get,
        )

    # =====================================================
    # B/S BACKTEST
    # =====================================================

    def backtest_bs(
        self,
        history: List[Dict[str, Any]],
        lookback: int = 5,
    ) -> Dict[str, Any]:

        history = self.normalize(history)

        total = 0
        correct = 0

        results = []

        if len(history) <= lookback:
            return self.empty_result("B/S")

        for index in range(
            lookback,
            len(history),
        ):

            training = history[
                :index
            ]

            actual = history[
                index
            ]

            prediction = self.predict_bs(
                training,
                lookback,
            )

            if prediction is None:
                continue

            is_correct = (
                prediction
                == actual["bs"]
            )

            total += 1

            if is_correct:
                correct += 1

            results.append({

                "period":
                    actual["period"],

                "prediction":
                    prediction,

                "actual":
                    actual["bs"],

                "correct":
                    is_correct,
            })

        accuracy = (
            correct / total * 100
            if total
            else 0.0
        )

        return {

            "type": "B/S",

            "samples": total,

            "correct": correct,

            "wrong":
                total - correct,

            "accuracy":
                round(
                    accuracy,
                    2,
                ),

            "results":
                results,
        }

    # =====================================================
    # NUMBER BACKTEST
    # =====================================================

    def backtest_number(
        self,
        history: List[Dict[str, Any]],
        lookback: int = 20,
    ) -> Dict[str, Any]:

        history = self.normalize(history)

        total = 0
        correct = 0

        results = []

        if len(history) <= lookback:
            return self.empty_result(
                "NUMBER"
            )

        for index in range(
            lookback,
            len(history),
        ):

            training = history[
                :index
            ]

            actual = history[
                index
            ]

            prediction = self.predict_number(
                training,
                lookback,
            )

            if prediction is None:
                continue

            is_correct = (
                prediction
                == actual["number"]
            )

            total += 1

            if is_correct:
                correct += 1

            results.append({

                "period":
                    actual["period"],

                "prediction":
                    prediction,

                "actual":
                    actual["number"],

                "correct":
                    is_correct,
            })

        accuracy = (
            correct / total * 100
            if total
            else 0.0
        )

        return {

            "type": "NUMBER",

            "samples": total,

            "correct": correct,

            "wrong":
                total - correct,

            "accuracy":
                round(
                    accuracy,
                    2,
                ),

            "results":
                results,
        }

    # =====================================================
    # FULL BACKTEST
    # =====================================================

    def run(
        self,
        history: List[Dict[str, Any]],
    ) -> Dict[str, Any]:

        history = self.normalize(history)

        bs_result = self.backtest_bs(
            history,
            lookback=5,
        )

        number_result = (
            self.backtest_number(
                history,
                lookback=20,
            )
        )

        # -------------------------------------------------
        # Combined
        # -------------------------------------------------

        total_samples = (
            bs_result["samples"]
            + number_result["samples"]
        )

        total_correct = (
            bs_result["correct"]
            + number_result["correct"]
        )

        combined_accuracy = (
            total_correct
            / total_samples
            * 100
            if total_samples
            else 0.0
        )

        return {

            "bs":
                bs_result,

            "number":
                number_result,

            "combined": {

                "samples":
                    total_samples,

                "correct":
                    total_correct,

                "wrong":
                    (
                        total_samples
                        - total_correct
                    ),

                "accuracy":
                    round(
                        combined_accuracy,
                        2,
                    ),
            },
        }

    # =====================================================
    # RECENT BACKTEST
    # =====================================================

    def recent_backtest(
        self,
        history: List[Dict[str, Any]],
        samples: int = 100,
    ) -> Dict[str, Any]:

        history = self.normalize(history)

        if len(history) > samples:
            history = history[-samples:]

        return self.run(
            history
        )

    # =====================================================
    # EMPTY RESULT
    # =====================================================

    def empty_result(
        self,
        result_type: str,
    ) -> Dict[str, Any]:

        return {

            "type":
                result_type,

            "samples":
                0,

            "correct":
                0,

            "wrong":
                0,

            "accuracy":
                0.0,

            "results":
                [],
        }


# =========================================================
# HELPER
# =========================================================

def run_backtest(
    history: List[Dict[str, Any]],
) -> Dict[str, Any]:

    engine = BacktestEngine()

    return engine.run(
        history
    )
