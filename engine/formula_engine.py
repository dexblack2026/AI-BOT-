# =========================================================
# AI-BOT - FORMULA ENGINE
# =========================================================

import logging
from typing import Dict, List, Optional

from config import (
    S_FORMULA,
    B_FORMULA,
)

logger = logging.getLogger("FormulaEngine")


class FormulaEngine:

    # =====================================================
    # INIT
    # =====================================================

    def __init__(
        self,
        s_formula: Optional[Dict[int, str]] = None,
        b_formula: Optional[Dict[int, str]] = None,
    ):

        self.s_formula = (
            s_formula
            if s_formula is not None
            else S_FORMULA
        )

        self.b_formula = (
            b_formula
            if b_formula is not None
            else B_FORMULA
        )

    # =====================================================
    # GET B/S SEQUENCE
    # =====================================================

    @staticmethod
    def get_bs_sequence(
        history: List[Dict],
    ) -> List[str]:

        result = []

        for item in history:

            bs = str(
                item.get("bs", "")
            ).upper()

            if bs in ("B", "S"):
                result.append(bs)

        return result

    # =====================================================
    # CURRENT RUN
    # =====================================================

    @staticmethod
    def get_current_run(
        sequence: List[str],
    ) -> Dict:

        if not sequence:

            return {
                "type": None,
                "length": 0,
                "pattern": "",
            }

        last = sequence[-1]

        count = 0

        for value in reversed(sequence):

            if value == last:
                count += 1
            else:
                break

        return {
            "type": last,
            "length": count,
            "pattern": last * count,
        }

    # =====================================================
    # FORMULA LOOKUP
    # =====================================================

    def get_formula_prediction(
        self,
        run_type: Optional[str],
        run_length: int,
    ) -> Optional[str]:

        if not run_type:
            return None

        if run_length <= 0:
            return None

        run_type = run_type.upper()

        if run_type == "S":

            return self.s_formula.get(
                run_length
            )

        if run_type == "B":

            return self.b_formula.get(
                run_length
            )

        return None

    # =====================================================
    # FORMULA KEY
    # =====================================================

    @staticmethod
    def make_rule_key(
        run_type: Optional[str],
        run_length: int,
    ) -> str:

        if not run_type:
            return "UNKNOWN_0"

        return (
            f"{run_type.upper()}_{run_length}"
        )

    # =====================================================
    # ANALYZE
    # =====================================================

    def analyze(
        self,
        history: List[Dict],
    ) -> Dict:

        sequence = self.get_bs_sequence(
            history
        )

        current_run = self.get_current_run(
            sequence
        )

        run_type = current_run[
            "type"
        ]

        run_length = current_run[
            "length"
        ]

        prediction = (
            self.get_formula_prediction(
                run_type,
                run_length,
            )
        )

        rule_key = self.make_rule_key(
            run_type,
            run_length,
        )

        available = prediction is not None

        result = {

            "available":
                available,

            "run_type":
                run_type,

            "run_length":
                run_length,

            "run_pattern":
                current_run["pattern"],

            "rule_key":
                rule_key,

            "prediction":
                prediction,

            "sequence_length":
                len(sequence),

        }

        logger.info(
            "Formula analysis | "
            "run=%s | prediction=%s",
            current_run["pattern"],
            prediction,
        )

        return result

    # =====================================================
    # TEST FORMULA AGAINST HISTORY
    # =====================================================

    def backtest_rule(
        self,
        history: List[Dict],
    ) -> List[Dict]:

        sequence = self.get_bs_sequence(
            history
        )

        results = []

        # Need enough previous data
        if len(sequence) < 2:
            return results

        for index in range(
            1,
            len(sequence),
        ):

            past = sequence[:index]

            current_run = (
                self.get_current_run(
                    past
                )
            )

            run_type = current_run[
                "type"
            ]

            run_length = current_run[
                "length"
            ]

            prediction = (
                self.get_formula_prediction(
                    run_type,
                    run_length,
                )
            )

            actual = sequence[index]

            rule_key = (
                self.make_rule_key(
                    run_type,
                    run_length,
                )
            )

            if prediction is None:
                continue

            results.append({

                "index":
                    index,

                "rule_key":
                    rule_key,

                "run_pattern":
                    current_run[
                        "pattern"
                    ],

                "prediction":
                    prediction,

                "actual":
                    actual,

                "correct":
                    prediction == actual,

            })

        return results

    # =====================================================
    # RULE STATISTICS
    # =====================================================

    def calculate_rule_stats(
        self,
        history: List[Dict],
    ) -> Dict[str, Dict]:

        backtest = self.backtest_rule(
            history
        )

        stats = {}

        for item in backtest:

            key = item[
                "rule_key"
            ]

            if key not in stats:

                stats[key] = {

                    "samples": 0,

                    "correct": 0,

                    "wrong": 0,

                    "accuracy": 0.0,

                }

            stats[key][
                "samples"
            ] += 1

            if item["correct"]:

                stats[key][
                    "correct"
                ] += 1

            else:

                stats[key][
                    "wrong"
                ] += 1

        # Calculate accuracy
        for key, value in stats.items():

            samples = value[
                "samples"
            ]

            correct = value[
                "correct"
            ]

            if samples > 0:

                value[
                    "accuracy"
                ] = round(
                    correct
                    / samples
                    * 100.0,
                    2,
                )

        return stats

    # =====================================================
    # COMPLETE RESULT
    # =====================================================

    def evaluate(
        self,
        history: List[Dict],
    ) -> Dict:

        analysis = self.analyze(
            history
        )

        statistics = (
            self.calculate_rule_stats(
                history
            )
        )

        rule_key = analysis[
            "rule_key"
        ]

        rule_stats = statistics.get(
            rule_key,
            {
                "samples": 0,
                "correct": 0,
                "wrong": 0,
                "accuracy": 0.0,
            },
        )

        return {

            "analysis":
                analysis,

            "rule_stats":
                rule_stats,

            "all_rule_stats":
                statistics,

        }
