# engine/formula_engine.py

from typing import Dict, Optional


class FormulaEngine:

    def __init__(self):

        # =================================================
        # S RUN FORMULA
        #
        # S      -> B
        # SS     -> B
        # SSS    -> S
        # SSSS   -> B
        # SSSSS  -> S
        # =================================================

        self.s_formula: Dict[int, str] = {
            1: "B",
            2: "B",
            3: "S",
            4: "B",
            5: "S",
        }

        # =================================================
        # B RUN FORMULA
        #
        # B       -> S
        # BB      -> S
        # BBB     -> B
        # BBBB    -> S
        # BBBBB   -> B
        # BBBBBB  -> S
        # =================================================

        self.b_formula: Dict[int, str] = {
            1: "S",
            2: "S",
            3: "B",
            4: "S",
            5: "B",
            6: "S",
        }

    # =====================================================
    # GET CURRENT RUN
    # =====================================================

    @staticmethod
    def get_current_run(
        sequence: list[str],
    ) -> tuple[str, int]:

        if not sequence:
            return "", 0

        current = sequence[-1]

        count = 0

        for value in reversed(sequence):

            if value != current:
                break

            count += 1

        return current, count

    # =====================================================
    # GET FORMULA PREDICTION
    # =====================================================

    def predict(
        self,
        sequence: list[str],
    ) -> Optional[str]:

        run_type, run_length = (
            self.get_current_run(sequence)
        )

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
    # GET RULE INFORMATION
    # =====================================================

    def get_rule(
        self,
        sequence: list[str],
    ) -> Dict:

        run_type, run_length = (
            self.get_current_run(sequence)
        )

        prediction = self.predict(
            sequence
        )

        if run_type:

            pattern = (
                run_type * run_length
            )

        else:

            pattern = ""

        return {
            "run_type": run_type,
            "run_length": run_length,
            "pattern": pattern,
            "prediction": prediction,
            "rule_key": (
                f"{run_type}_{run_length}"
                if run_type
                else None
            ),
        }

    # =====================================================
    # FORMULA TABLE
    # =====================================================

    def get_formula_table(self) -> Dict:

        return {
            "S": self.s_formula.copy(),
            "B": self.b_formula.copy(),
        }

    # =====================================================
    # CHECK WHETHER RULE EXISTS
    # =====================================================

    def has_rule(
        self,
        sequence: list[str],
    ) -> bool:

        return (
            self.predict(sequence)
            is not None
        )

    # =====================================================
    # ANALYZE
    # =====================================================

    def analyze(
        self,
        sequence: list[str],
    ) -> Dict:

        rule = self.get_rule(
            sequence
        )

        return {
            "status": (
                "FOUND"
                if rule["prediction"]
                else "NO_RULE"
            ),
            **rule,
        }
