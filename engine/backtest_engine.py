# =========================================================
# AI-BOT - BACKTEST ENGINE
# =========================================================

import logging
from collections import Counter
from typing import Dict, List, Optional


logger = logging.getLogger("BacktestEngine")


class BacktestEngine:

    # =====================================================
    # INIT
    # =====================================================

    def __init__(
        self,
        min_history: int = 20,
        min_pattern_matches: int = 3,
    ):

        self.min_history = min_history
        self.min_pattern_matches = (
            min_pattern_matches
        )

    # =====================================================
    # B/S SEQUENCE
    # =====================================================

    @staticmethod
    def get_bs_sequence(
        history: List[Dict],
    ) -> List[str]:

        sequence = []

        for item in history:

            bs = str(
                item.get("bs", "")
            ).upper()

            if bs in ("B", "S"):

                sequence.append(bs)

        return sequence

    # =====================================================
    # FIND CURRENT PATTERN
    # =====================================================

    def find_pattern_prediction(
        self,
        sequence: List[str],
        min_length: int = 3,
        max_length: int = 12,
    ) -> Optional[Dict]:

        if len(sequence) < min_length + 1:

            return None

        maximum = min(
            max_length,
            len(sequence) - 1,
        )

        # Longest pattern first
        for length in range(
            maximum,
            min_length - 1,
            -1,
        ):

            pattern = "".join(
                sequence[-length:]
            )

            matches = []

            # Search only in previous data
            for i in range(
                len(sequence) - length
            ):

                previous = "".join(
                    sequence[
                        i:i + length
                    ]
                )

                if previous != pattern:
                    continue

                next_index = i + length

                if next_index >= len(sequence):
                    continue

                matches.append(
                    sequence[next_index]
                )

            if len(matches) < (
                self.min_pattern_matches
            ):

                continue

            counter = Counter(
                matches
            )

            if counter["B"] > counter["S"]:

                prediction = "B"

            elif counter["S"] > counter["B"]:

                prediction = "S"

            else:

                prediction = None

            if prediction is None:
                continue

            confidence = (
                counter[prediction]
                / len(matches)
                * 100.0
            )

            return {

                "method":
                    "HISTORICAL_PATTERN",

                "pattern":
                    pattern,

                "matches":
                    len(matches),

                "B":
                    counter["B"],

                "S":
                    counter["S"],

                "prediction":
                    prediction,

                "confidence":
                    round(
                        confidence,
                        2,
                    ),

            }

        return None

    # =====================================================
    # CURRENT RUN
    # =====================================================

    @staticmethod
    def current_run(
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

        for value in reversed(
            sequence
        ):

            if value == last:

                count += 1

            else:

                break

        return {

            "type":
                last,

            "length":
                count,

            "pattern":
                last * count,

        }

    # =====================================================
    # FORMULA PREDICTION
    # =====================================================

    @staticmethod
    def formula_prediction(
        run_type: Optional[str],
        run_length: int,
        s_formula: Dict[int, str],
        b_formula: Dict[int, str],
    ) -> Optional[str]:

        if not run_type:
            return None

        if run_length <= 0:
            return None

        if run_type == "S":

            return s_formula.get(
                run_length
            )

        if run_type == "B":

            return b_formula.get(
                run_length
            )

        return None

    # =====================================================
    # WALK FORWARD
    # =====================================================

    def run(
        self,
        history: List[Dict],
        s_formula: Dict[int, str],
        b_formula: Dict[int, str],
    ) -> Dict:

        sequence = self.get_bs_sequence(
            history
        )

        if len(sequence) < (
            self.min_history + 1
        ):

            return self.empty_result()

        records = []

        # -------------------------------------------------
        # Every point uses only previous history
        # -------------------------------------------------

        for index in range(
            self.min_history,
            len(sequence),
        ):

            past = sequence[
                :index
            ]

            actual = sequence[
                index
            ]

            # =============================================
            # Pattern signal
            # =============================================

            pattern_signal = (
                self.find_pattern_prediction(
                    past
                )
            )

            # =============================================
            # Formula signal
            # =============================================

            run = self.current_run(
                past
            )

            formula_pred = (
                self.formula_prediction(
                    run["type"],
                    run["length"],
                    s_formula,
                    b_formula,
                )
            )

            # =============================================
            # Record
            # =============================================

            records.append({

                "index":
                    index,

                "actual":
                    actual,

                "pattern_prediction":
                    (
                        pattern_signal.get(
                            "prediction"
                        )
                        if pattern_signal
                        else None
                    ),

                "pattern_confidence":
                    (
                        pattern_signal.get(
                            "confidence",
                            0.0,
                        )
                        if pattern_signal
                        else 0.0
                    ),

                "formula_prediction":
                    formula_pred,

                "run_pattern":
                    run["pattern"],

            })

        return self.calculate_statistics(
            records
        )

    # =====================================================
    # STATISTICS
    # =====================================================

    def calculate_statistics(
        self,
        records: List[Dict],
    ) -> Dict:

        pattern_samples = 0
        pattern_correct = 0

        formula_samples = 0
        formula_correct = 0

        combined_samples = 0
        combined_correct = 0

        for record in records:

            actual = record[
                "actual"
            ]

            pattern_pred = record[
                "pattern_prediction"
            ]

            formula_pred = record[
                "formula_prediction"
            ]

            # ---------------------------------------------
            # Pattern
            # ---------------------------------------------

            if pattern_pred in (
                "B",
                "S",
            ):

                pattern_samples += 1

                if pattern_pred == actual:

                    pattern_correct += 1

            # ---------------------------------------------
            # Formula
            # ---------------------------------------------

            if formula_pred in (
                "B",
                "S",
            ):

                formula_samples += 1

                if formula_pred == actual:

                    formula_correct += 1

            # ---------------------------------------------
            # Combined
            # ---------------------------------------------

            combined_pred = None

            if (
                pattern_pred in ("B", "S")
                and formula_pred in ("B", "S")
                and pattern_pred == formula_pred
            ):

                combined_pred = pattern_pred

            if combined_pred in (
                "B",
                "S",
            ):

                combined_samples += 1

                if combined_pred == actual:

                    combined_correct += 1

        pattern_accuracy = (
            pattern_correct
            / pattern_samples
            * 100.0
            if pattern_samples
            else 0.0
        )

        formula_accuracy = (
            formula_correct
            / formula_samples
            * 100.0
            if formula_samples
            else 0.0
        )

        combined_accuracy = (
            combined_correct
            / combined_samples
            * 100.0
            if combined_samples
            else 0.0
        )

        return {

            "total_records":
                len(records),

            "pattern": {

                "samples":
                    pattern_samples,

                "correct":
                    pattern_correct,

                "wrong":
                    pattern_samples
                    - pattern_correct,

                "accuracy":
                    round(
                        pattern_accuracy,
                        2,
                    ),

            },

            "formula": {

                "samples":
                    formula_samples,

                "correct":
                    formula_correct,

                "wrong":
                    formula_samples
                    - formula_correct,

                "accuracy":
                    round(
                        formula_accuracy,
                        2,
                    ),

            },

            "combined": {

                "samples":
                    combined_samples,

                "correct":
                    combined_correct,

                "wrong":
                    combined_samples
                    - combined_correct,

                "accuracy":
                    round(
                        combined_accuracy,
                        2,
                    ),

            },

            "records":
                records,

        }

    # =====================================================
    # EMPTY RESULT
    # =====================================================

    @staticmethod
    def empty_result() -> Dict:

        return {

            "total_records":
                0,

            "pattern": {

                "samples": 0,
                "correct": 0,
                "wrong": 0,
                "accuracy": 0.0,

            },

            "formula": {

                "samples": 0,
                "correct": 0,
                "wrong": 0,
                "accuracy": 0.0,

            },

            "combined": {

                "samples": 0,
                "correct": 0,
                "wrong": 0,
                "accuracy": 0.0,

            },

            "records": [],

        }

    # =====================================================
    # BEST METHOD
    # =====================================================

    @staticmethod
    def best_method(
        result: Dict,
    ) -> Dict:

        methods = {

            "PATTERN":
                result.get(
                    "pattern",
                    {},
                ),

            "FORMULA":
                result.get(
                    "formula",
                    {},
                ),

            "COMBINED":
                result.get(
                    "combined",
                    {},
                ),

        }

        available = []

        for name, stats in methods.items():

            samples = stats.get(
                "samples",
                0,
            )

            accuracy = stats.get(
                "accuracy",
                0.0,
            )

            if samples > 0:

                available.append(
                    (
                        name,
                        samples,
                        accuracy,
                    )
                )

        if not available:

            return {

                "method": None,
                "samples": 0,
                "accuracy": 0.0,

            }

        # Accuracy first, samples second
        available.sort(
            key=lambda x: (
                x[2],
                x[1],
            ),
            reverse=True,
        )

        name, samples, accuracy = (
            available[0]
        )

        return {

            "method":
                name,

            "samples":
                samples,

            "accuracy":
                accuracy,

        }
