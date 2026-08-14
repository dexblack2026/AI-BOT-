# engine/backtest_engine.py

from collections import Counter
from typing import Dict, List, Optional


class BacktestEngine:

    def __init__(
        self,
        min_history: int = 20,
    ):
        self.min_history = min_history

    # =====================================================
    # BASIC RESULT
    # =====================================================

    @staticmethod
    def empty_result() -> Dict:

        return {
            "samples": 0,
            "correct": 0,
            "wrong": 0,
            "accuracy": 0.0,
        }

    # =====================================================
    # UPDATE RESULT
    # =====================================================

    @staticmethod
    def update_result(
        result: Dict,
        prediction: Optional[str],
        actual: str,
    ):

        if prediction not in ("B", "S"):
            return

        result["samples"] += 1

        if prediction == actual:
            result["correct"] += 1
        else:
            result["wrong"] += 1

    # =====================================================
    # CALCULATE ACCURACY
    # =====================================================

    @staticmethod
    def calculate_accuracy(
        result: Dict,
    ) -> float:

        samples = result["samples"]

        if samples <= 0:
            return 0.0

        return round(
            result["correct"]
            / samples
            * 100,
            2,
        )

    # =====================================================
    # PATTERN SEARCH
    # =====================================================

    @staticmethod
    def find_pattern(
        history: List[str],
        pattern: str,
    ) -> List[str]:

        results = []

        length = len(pattern)

        if length == 0:
            return results

        for i in range(
            len(history) - length
        ):

            current = "".join(
                history[
                    i:i + length
                ]
            )

            if current != pattern:
                continue

            next_index = i + length

            if next_index >= len(history):
                continue

            results.append(
                history[next_index]
            )

        return results

    # =====================================================
    # PATTERN PREDICTION
    # =====================================================

    def pattern_prediction(
        self,
        history: List[str],
        min_pattern: int = 3,
        max_pattern: int = 12,
        min_matches: int = 3,
    ) -> Optional[Dict]:

        if len(history) < min_pattern:
            return None

        max_length = min(
            max_pattern,
            len(history) - 1,
        )

        # Longest context first
        for length in range(
            max_length,
            min_pattern - 1,
            -1,
        ):

            pattern = "".join(
                history[-length:]
            )

            matches = self.find_pattern(
                history[:-0] if False else history,
                pattern,
            )

            if len(matches) < min_matches:
                continue

            counter = Counter(matches)

            if counter["B"] > counter["S"]:
                prediction = "B"

            elif counter["S"] > counter["B"]:
                prediction = "S"

            else:
                prediction = None

            return {
                "prediction": prediction,
                "pattern": pattern,
                "matches": len(matches),
                "B": counter["B"],
                "S": counter["S"],
            }

        return None

    # =====================================================
    # WALK-FORWARD PATTERN BACKTEST
    # =====================================================

    def backtest_pattern(
        self,
        sequence: List[str],
        min_pattern: int = 3,
        max_pattern: int = 12,
        min_matches: int = 3,
    ) -> Dict:

        result = self.empty_result()

        if len(sequence) <= self.min_history:
            return result

        for index in range(
            self.min_history,
            len(sequence),
        ):

            # အဲဒီအချိန်ထိ ရှိတဲ့ data ပဲသုံး
            past = sequence[:index]

            actual = sequence[index]

            analysis = self.pattern_prediction(
                past,
                min_pattern=min_pattern,
                max_pattern=max_pattern,
                min_matches=min_matches,
            )

            if not analysis:
                continue

            prediction = analysis[
                "prediction"
            ]

            self.update_result(
                result,
                prediction,
                actual,
            )

        result["accuracy"] = (
            self.calculate_accuracy(result)
        )

        return result

    # =====================================================
    # FORMULA PREDICTION
    # =====================================================

    @staticmethod
    def formula_prediction(
        sequence: List[str],
        s_formula: Dict[int, str],
        b_formula: Dict[int, str],
    ) -> Optional[str]:

        if not sequence:
            return None

        current = sequence[-1]

        run_length = 0

        for value in reversed(sequence):

            if value != current:
                break

            run_length += 1

        if current == "S":

            return s_formula.get(
                run_length
            )

        if current == "B":

            return b_formula.get(
                run_length
            )

        return None

    # =====================================================
    # WALK-FORWARD FORMULA BACKTEST
    # =====================================================

    def backtest_formula(
        self,
        sequence: List[str],
        s_formula: Dict[int, str],
        b_formula: Dict[int, str],
    ) -> Dict:

        result = self.empty_result()

        if len(sequence) <= self.min_history:
            return result

        for index in range(
            self.min_history,
            len(sequence),
        ):

            past = sequence[:index]

            actual = sequence[index]

            prediction = self.formula_prediction(
                past,
                s_formula,
                b_formula,
            )

            self.update_result(
                result,
                prediction,
                actual,
            )

        result["accuracy"] = (
            self.calculate_accuracy(result)
        )

        return result

    # =====================================================
    # FULL BACKTEST
    # =====================================================

    def run(
        self,
        sequence: List[str],
        s_formula: Dict[int, str],
        b_formula: Dict[int, str],
    ) -> Dict:

        pattern_result = (
            self.backtest_pattern(sequence)
        )

        formula_result = (
            self.backtest_formula(
                sequence,
                s_formula,
                b_formula,
            )
        )

        return {
            "status": "OK",
            "total_data": len(sequence),
            "pattern": pattern_result,
            "formula": formula_result,
        }
