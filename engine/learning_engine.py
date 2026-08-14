# =========================================================
# AI-BOT - LEARNING ENGINE
# =========================================================

import logging
from typing import Dict, Optional


logger = logging.getLogger("LearningEngine")


class LearningEngine:

    def __init__(self, memory_engine):

        self.memory = memory_engine

    # =====================================================
    # NORMALIZE
    # =====================================================

    @staticmethod
    def normalize(value: Optional[str]) -> Optional[str]:

        if value is None:
            return None

        value = str(value).upper().strip()

        if value in ("B", "S"):
            return value

        return None

    # =====================================================
    # LEARN FROM RESULT
    # =====================================================

    def learn(
        self,
        pattern: Optional[str],
        pattern_prediction: Optional[str],
        formula_key: Optional[str],
        formula_prediction: Optional[str],
        actual_result: Optional[str],
    ) -> Dict:

        actual = self.normalize(
            actual_result
        )

        pattern_prediction = self.normalize(
            pattern_prediction
        )

        formula_prediction = self.normalize(
            formula_prediction
        )

        if actual is None:

            return {
                "updated": False,
                "reason": "INVALID_ACTUAL_RESULT",
            }

        result = {
            "updated": True,
            "actual": actual,
            "pattern": None,
            "formula": None,
        }

        # =================================================
        # PATTERN MEMORY
        # =================================================

        if pattern:

            result["pattern"] = (
                self.memory.update_pattern(
                    pattern=pattern,
                    prediction=pattern_prediction,
                    actual=actual,
                )
            )

        # =================================================
        # FORMULA MEMORY
        # =================================================

        if formula_key:

            result["formula"] = (
                self.memory.update_formula(
                    rule_key=formula_key,
                    prediction=formula_prediction,
                    actual=actual,
                )
            )

        logger.info(
            "Learning completed | actual=%s | pattern=%s | formula=%s",
            actual,
            pattern,
            formula_key,
        )

        return result

    # =====================================================
    # CHECK PREDICTION
    # =====================================================

    @staticmethod
    def evaluate(
        prediction: Optional[str],
        actual: Optional[str],
    ) -> Dict:

        prediction = (
            str(prediction).upper()
            if prediction
            else None
        )

        actual = (
            str(actual).upper()
            if actual
            else None
        )

        if prediction not in ("B", "S"):

            return {
                "valid": False,
                "correct": False,
                "status": "NO_PREDICTION",
            }

        if actual not in ("B", "S"):

            return {
                "valid": False,
                "correct": False,
                "status": "INVALID_RESULT",
            }

        correct = (
            prediction == actual
        )

        return {
            "valid": True,
            "correct": correct,
            "status": (
                "WIN"
                if correct
                else "LOSS"
            ),
            "prediction": prediction,
            "actual": actual,
        }

    # =====================================================
    # GET MEMORY STATUS
    # =====================================================

    def status(self) -> Dict:

        try:

            return (
                self.memory.get_statistics()
            )

        except Exception as error:

            logger.error(
                "Unable to read memory status: %s",
                error,
            )

            return {

                "pattern": {},

                "formula": {},

            }
