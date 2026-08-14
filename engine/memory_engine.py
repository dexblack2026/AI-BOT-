# =========================================================
# AI-BOT - MEMORY ENGINE
# =========================================================

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional


logger = logging.getLogger("MemoryEngine")


class MemoryEngine:

    def __init__(
        self,
        pattern_file: str = "models/pattern_memory.json",
        formula_file: str = "models/formula_memory.json",
        max_records: int = 5000,
    ):

        self.pattern_file = Path(
            pattern_file
        )

        self.formula_file = Path(
            formula_file
        )

        self.max_records = max(
            100,
            max_records,
        )

        self.pattern_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.formula_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._ensure_file(
            self.pattern_file
        )

        self._ensure_file(
            self.formula_file
        )

    # =====================================================
    # FILE
    # =====================================================

    def _ensure_file(
        self,
        path: Path,
    ) -> None:

        if path.exists():
            return

        try:

            path.write_text(
                "[]",
                encoding="utf-8",
            )

        except OSError as error:

            logger.error(
                "Cannot create %s: %s",
                path,
                error,
            )

    # =====================================================
    # LOAD
    # =====================================================

    def _load(
        self,
        path: Path,
    ) -> List[Dict[str, Any]]:

        try:

            if not path.exists():
                return []

            text = path.read_text(
                encoding="utf-8"
            ).strip()

            if not text:
                return []

            data = json.loads(
                text
            )

            if not isinstance(
                data,
                list,
            ):

                return []

            return [
                item
                for item in data
                if isinstance(
                    item,
                    dict,
                )
            ]

        except (
            OSError,
            json.JSONDecodeError,
        ) as error:

            logger.error(
                "Memory load error: %s",
                error,
            )

            return []

    # =====================================================
    # SAVE
    # =====================================================

    def _save(
        self,
        path: Path,
        records: List[
            Dict[str, Any]
        ],
    ) -> bool:

        try:

            records = records[
                -self.max_records:
            ]

            path.write_text(
                json.dumps(
                    records,
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            return True

        except OSError as error:

            logger.error(
                "Memory save error: %s",
                error,
            )

            return False

    # =====================================================
    # PATTERN MEMORY
    # =====================================================

    def load_patterns(
        self,
    ) -> List[Dict[str, Any]]:

        return self._load(
            self.pattern_file
        )

    def save_pattern(
        self,
        record: Dict[str, Any],
    ) -> bool:

        records = self.load_patterns()

        records.append(
            record
        )

        return self._save(
            self.pattern_file,
            records,
        )

    # =====================================================
    # FORMULA MEMORY
    # =====================================================

    def load_formulas(
        self,
    ) -> List[Dict[str, Any]]:

        return self._load(
            self.formula_file
        )

    def save_formula(
        self,
        record: Dict[str, Any],
    ) -> bool:

        records = self.load_formulas()

        records.append(
            record
        )

        return self._save(
            self.formula_file,
            records,
        )

    # =====================================================
    # RECORD PREDICTION
    # =====================================================

    def record_prediction(
        self,
        *,
        period: str,
        prediction: int,
        actual: Optional[int] = None,
        pattern: Optional[str] = None,
        confidence: float = 0.0,
        evidence: float = 0.0,
    ) -> bool:

        correct = None

        if actual is not None:

            correct = (
                int(prediction)
                == int(actual)
            )

        record = {

            "period":
                str(period),

            "prediction":
                int(prediction),

            "actual":
                (
                    int(actual)
                    if actual is not None
                    else None
                ),

            "correct":
                correct,

            "pattern":
                pattern,

            "confidence":
                round(
                    float(confidence),
                    2,
                ),

            "evidence":
                round(
                    float(evidence),
                    2,
                ),
        }

        return self.save_pattern(
            record
        )

    # =====================================================
    # PATTERN STATISTICS
    # =====================================================

    def pattern_statistics(
        self,
    ) -> Dict[str, Any]:

        records = self.load_patterns()

        total = 0
        correct = 0

        for record in records:

            actual = record.get(
                "actual"
            )

            result = record.get(
                "correct"
            )

            if actual is None:
                continue

            total += 1

            if result is True:
                correct += 1

        accuracy = (
            correct / total * 100
            if total
            else 0.0
        )

        return {

            "total":
                total,

            "correct":
                correct,

            "wrong":
                total - correct,

            "accuracy":
                round(
                    accuracy,
                    2,
                ),
        }

    # =====================================================
    # FORMULA STATISTICS
    # =====================================================

    def formula_statistics(
        self,
    ) -> Dict[str, Any]:

        records = self.load_formulas()

        total = 0
        correct = 0

        for record in records:

            actual = record.get(
                "actual"
            )

            if actual is None:
                continue

            total += 1

            if record.get(
                "correct"
            ) is True:

                correct += 1

        accuracy = (
            correct / total * 100
            if total
            else 0.0
        )

        return {

            "total":
                total,

            "correct":
                correct,

            "wrong":
                total - correct,

            "accuracy":
                round(
                    accuracy,
                    2,
                ),
        }

    # =====================================================
    # RECENT MEMORY
    # =====================================================

    def recent_patterns(
        self,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:

        records = self.load_patterns()

        return records[-limit:]

    def recent_formulas(
        self,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:

        records = self.load_formulas()

        return records[-limit:]

    # =====================================================
    # CLEAR
    # =====================================================

    def clear_patterns(self) -> bool:

        return self._save(
            self.pattern_file,
            [],
        )

    def clear_formulas(self) -> bool:

        return self._save(
            self.formula_file,
            [],
        )
