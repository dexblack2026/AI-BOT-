# =========================================================
# AI-BOT - MEMORY ENGINE
# =========================================================

import json
import logging
import os
from typing import Dict, Optional


logger = logging.getLogger("MemoryEngine")


class MemoryEngine:

    def __init__(
        self,
        pattern_file: str = "models/pattern_memory.json",
        formula_file: str = "models/formula_memory.json",
    ):

        self.pattern_file = pattern_file
        self.formula_file = formula_file

        self.pattern_memory = self._load(
            self.pattern_file
        )

        self.formula_memory = self._load(
            self.formula_file
        )

    # =====================================================
    # LOAD
    # =====================================================

    @staticmethod
    def _load(
        filename: str,
    ) -> Dict:

        try:

            if not os.path.exists(
                filename
            ):

                return {}

            with open(
                filename,
                "r",
                encoding="utf-8",
            ) as file:

                data = json.load(
                    file
                )

            return (
                data
                if isinstance(data, dict)
                else {}
            )

        except (
            OSError,
            json.JSONDecodeError,
        ) as error:

            logger.error(
                "Memory load error %s: %s",
                filename,
                error,
            )

            return {}

    # =====================================================
    # SAVE
    # =====================================================

    @staticmethod
    def _save(
        filename: str,
        data: Dict,
    ) -> bool:

        try:

            directory = os.path.dirname(
                filename
            )

            if directory:

                os.makedirs(
                    directory,
                    exist_ok=True,
                )

            temp_file = (
                filename + ".tmp"
            )

            with open(
                temp_file,
                "w",
                encoding="utf-8",
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4,
                    ensure_ascii=False,
                )

            os.replace(
                temp_file,
                filename,
            )

            return True

        except OSError as error:

            logger.error(
                "Memory save error %s: %s",
                filename,
                error,
            )

            return False

    # =====================================================
    # DEFAULT RECORD
    # =====================================================

    @staticmethod
    def _default_record() -> Dict:

        return {

            "samples": 0,

            "wins": 0,

            "losses": 0,

            "accuracy": 0.0,

            "last_prediction": None,

            "last_actual": None,

        }

    # =====================================================
    # GET PATTERN
    # =====================================================

    def get_pattern(
        self,
        pattern: str,
    ) -> Dict:

        if not pattern:
            return self._default_record()

        record = self.pattern_memory.get(
            pattern
        )

        if not isinstance(
            record,
            dict,
        ):

            record = self._default_record()

        return record

    # =====================================================
    # GET FORMULA
    # =====================================================

    def get_formula(
        self,
        rule_key: str,
    ) -> Dict:

        if not rule_key:
            return self._default_record()

        record = self.formula_memory.get(
            rule_key
        )

        if not isinstance(
            record,
            dict,
        ):

            record = self._default_record()

        return record

    # =====================================================
    # UPDATE RECORD
    # =====================================================

    @staticmethod
    def _update_record(
        memory: Dict,
        key: str,
        prediction: Optional[str],
        actual: Optional[str],
    ) -> Dict:

        if not key:
            return {}

        if key not in memory:

            memory[key] = (
                MemoryEngine._default_record()
            )

        record = memory[key]

        if not isinstance(
            record,
            dict,
        ):

            record = (
                MemoryEngine._default_record()
            )

            memory[key] = record

        prediction = (
            str(prediction).upper()
            if prediction is not None
            else None
        )

        actual = (
            str(actual).upper()
            if actual is not None
            else None
        )

        record["samples"] = int(
            record.get(
                "samples",
                0,
            )
        ) + 1

        if (
            prediction is not None
            and actual is not None
            and prediction == actual
        ):

            record["wins"] = int(
                record.get(
                    "wins",
                    0,
                )
            ) + 1

        else:

            record["losses"] = int(
                record.get(
                    "losses",
                    0,
                )
            ) + 1

        samples = record[
            "samples"
        ]

        wins = record[
            "wins"
        ]

        record["accuracy"] = round(
            wins / samples * 100.0,
            2,
        )

        record[
            "last_prediction"
        ] = prediction

        record[
            "last_actual"
        ] = actual

        return record

    # =====================================================
    # UPDATE PATTERN
    # =====================================================

    def update_pattern(
        self,
        pattern: str,
        prediction: Optional[str],
        actual: Optional[str],
    ) -> Dict:

        record = self._update_record(
            self.pattern_memory,
            pattern,
            prediction,
            actual,
        )

        self._save(
            self.pattern_file,
            self.pattern_memory,
        )

        return record

    # =====================================================
    # UPDATE FORMULA
    # =====================================================

    def update_formula(
        self,
        rule_key: str,
        prediction: Optional[str],
        actual: Optional[str],
    ) -> Dict:

        record = self._update_record(
            self.formula_memory,
            rule_key,
            prediction,
            actual,
        )

        self._save(
            self.formula_file,
            self.formula_memory,
        )

        return record

    # =====================================================
    # UPDATE BOTH
    # =====================================================

    def update(
        self,
        pattern: Optional[str],
        pattern_prediction: Optional[str],
        formula_key: Optional[str],
        formula_prediction: Optional[str],
        actual: Optional[str],
    ) -> Dict:

        result = {

            "pattern": None,

            "formula": None,

        }

        if pattern:

            result["pattern"] = (
                self.update_pattern(
                    pattern,
                    pattern_prediction,
                    actual,
                )
            )

        if formula_key:

            result["formula"] = (
                self.update_formula(
                    formula_key,
                    formula_prediction,
                    actual,
                )
            )

        return result

    # =====================================================
    # STATISTICS
    # =====================================================

    @staticmethod
    def statistics(
        memory: Dict,
    ) -> Dict:

        total_samples = 0
        total_wins = 0
        total_losses = 0

        for record in memory.values():

            if not isinstance(
                record,
                dict,
            ):
                continue

            total_samples += int(
                record.get(
                    "samples",
                    0,
                )
            )

            total_wins += int(
                record.get(
                    "wins",
                    0,
                )
            )

            total_losses += int(
                record.get(
                    "losses",
                    0,
                )
            )

        accuracy = (
            total_wins
            / total_samples
            * 100.0
            if total_samples
            else 0.0
        )

        return {

            "rules":
                len(memory),

            "samples":
                total_samples,

            "wins":
                total_wins,

            "losses":
                total_losses,

            "accuracy":
                round(
                    accuracy,
                    2,
                ),

        }

    # =====================================================
    # ALL MEMORY
    # =====================================================

    def get_all(
        self,
    ) -> Dict:

        return {

            "pattern":
                self.pattern_memory,

            "formula":
                self.formula_memory,

        }

    # =====================================================
    # MEMORY STATS
    # =====================================================

    def get_statistics(
        self,
    ) -> Dict:

        return {

            "pattern":
                self.statistics(
                    self.pattern_memory
                ),

            "formula":
                self.statistics(
                    self.formula_memory
                ),

        }

    # =====================================================
    # BEST PATTERN
    # =====================================================

    def best_pattern(
        self,
        minimum_samples: int = 3,
    ) -> Optional[Dict]:

        candidates = []

        for pattern, record in (
            self.pattern_memory.items()
        ):

            if not isinstance(
                record,
                dict,
            ):
                continue

            samples = int(
                record.get(
                    "samples",
                    0,
                )
            )

            accuracy = float(
                record.get(
                    "accuracy",
                    0.0,
                )
            )

            if samples >= minimum_samples:

                candidates.append({

                    "pattern":
                        pattern,

                    "samples":
                        samples,

                    "accuracy":
                        accuracy,

                })

        if not candidates:
            return None

        candidates.sort(
            key=lambda item: (
                item["accuracy"],
                item["samples"],
            ),
            reverse=True,
        )

        return candidates[0]

    # =====================================================
    # BEST FORMULA
    # =====================================================

    def best_formula(
        self,
        minimum_samples: int = 3,
    ) -> Optional[Dict]:

        candidates = []

        for rule_key, record in (
            self.formula_memory.items()
        ):

            if not isinstance(
                record,
                dict,
            ):
                continue

            samples = int(
                record.get(
                    "samples",
                    0,
                )
            )

            accuracy = float(
                record.get(
                    "accuracy",
                    0.0,
                )
            )

            if samples >= minimum_samples:

                candidates.append({

                    "rule_key":
                        rule_key,

                    "samples":
                        samples,

                    "accuracy":
                        accuracy,

                })

        if not candidates:
            return None

        candidates.sort(
            key=lambda item: (
                item["accuracy"],
                item["samples"],
            ),
            reverse=True,
        )

        return candidates[0]
