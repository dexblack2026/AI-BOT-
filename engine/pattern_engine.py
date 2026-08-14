# =========================================================
# AI-BOT - PATTERN ENGINE
# =========================================================

import logging
from collections import Counter
from typing import Dict, List, Optional

from config import BIG_THRESHOLD


logger = logging.getLogger("PatternEngine")


class PatternEngine:

    # =====================================================
    # INIT
    # =====================================================

    def __init__(
        self,
        big_threshold: int = BIG_THRESHOLD,
    ):

        self.big_threshold = big_threshold

    # =====================================================
    # NUMBER -> B/S
    # =====================================================

    def number_to_bs(
        self,
        number: int,
    ) -> str:

        return (
            "B"
            if number >= self.big_threshold
            else "S"
        )

    # =====================================================
    # B/S -> NUMBER RANGE
    # =====================================================

    @staticmethod
    def bs_numbers(
        bs: str,
    ) -> List[int]:

        bs = bs.upper()

        if bs == "B":
            return [5, 6, 7, 8, 9]

        if bs == "S":
            return [0, 1, 2, 3, 4]

        return []

    # =====================================================
    # COUNT NUMBERS
    # =====================================================

    @staticmethod
    def count_numbers(
        numbers: List[int],
    ) -> Dict[int, int]:

        counter = Counter()

        for number in numbers:

            try:
                number = int(number)

            except (
                ValueError,
                TypeError,
            ):

                continue

            if 0 <= number <= 9:

                counter[number] += 1

        return dict(counter)

    # =====================================================
    # COUNT B/S
    # =====================================================

    @staticmethod
    def count_bs(
        results: List[str],
    ) -> Dict[str, int]:

        counter = Counter()

        for value in results:

            value = str(
                value
            ).upper()

            if value in ("B", "S"):

                counter[value] += 1

        return dict(counter)

    # =====================================================
    # MOST COMMON NUMBER
    # =====================================================

    @staticmethod
    def most_common_number(
        numbers: List[int],
    ) -> Optional[int]:

        if not numbers:
            return None

        counter = Counter(
            numbers
        )

        if not counter:
            return None

        return counter.most_common(
            1
        )[0][0]

    # =====================================================
    # MOST COMMON B/S
    # =====================================================

    @staticmethod
    def most_common_bs(
        results: List[str],
    ) -> Optional[str]:

        if not results:
            return None

        counter = Counter(
            results
        )

        if not counter:
            return None

        return counter.most_common(
            1
        )[0][0]

    # =====================================================
    # NUMBER CONFIDENCE
    # =====================================================

    @staticmethod
    def number_confidence(
        numbers: List[int],
        target: Optional[int],
    ) -> float:

        if not numbers or target is None:
            return 0.0

        count = numbers.count(
            target
        )

        return round(
            count / len(numbers) * 100.0,
            2,
        )

    # =====================================================
    # B/S CONFIDENCE
    # =====================================================

    @staticmethod
    def bs_confidence(
        results: List[str],
        target: Optional[str],
    ) -> float:

        if not results or not target:
            return 0.0

        target = target.upper()

        count = sum(
            1
            for value in results
            if value.upper() == target
        )

        return round(
            count / len(results) * 100.0,
            2,
        )

    # =====================================================
    # ANALYZE B/S PATTERN
    # =====================================================

    def analyze_bs_pattern(
        self,
        pattern_data: Optional[Dict],
    ) -> Optional[Dict]:

        if not pattern_data:
            return None

        matches = pattern_data.get(
            "matches",
            [],
        )

        if not matches:
            return None

        results = [
            str(value).upper()
            for value in matches
            if str(value).upper()
            in ("B", "S")
        ]

        if not results:
            return None

        counts = self.count_bs(
            results
        )

        prediction = (
            self.most_common_bs(
                results
            )
        )

        confidence = (
            self.bs_confidence(
                results,
                prediction,
            )
        )

        return {

            "pattern":
                pattern_data.get(
                    "pattern",
                    "",
                ),

            "pattern_length":
                pattern_data.get(
                    "length",
                    0,
                ),

            "matches":
                len(results),

            "B":
                counts.get(
                    "B",
                    0,
                ),

            "S":
                counts.get(
                    "S",
                    0,
                ),

            "prediction":
                prediction,

            "confidence":
                confidence,

        }

    # =====================================================
    # ANALYZE NUMBER PATTERN
    # =====================================================

    def analyze_number_pattern(
        self,
        pattern_data: Optional[Dict],
    ) -> Optional[Dict]:

        if not pattern_data:
            return None

        matches = pattern_data.get(
            "matches",
            [],
        )

        numbers = []

        for value in matches:

            try:

                number = int(
                    value
                )

            except (
                ValueError,
                TypeError,
            ):

                continue

            if 0 <= number <= 9:

                numbers.append(
                    number
                )

        if not numbers:
            return None

        counts = self.count_numbers(
            numbers
        )

        prediction = (
            self.most_common_number(
                numbers
            )
        )

        confidence = (
            self.number_confidence(
                numbers,
                prediction,
            )
        )

        bs_prediction = (
            self.number_to_bs(
                prediction
            )
            if prediction is not None
            else None
        )

        return {

            "pattern":
                pattern_data.get(
                    "pattern",
                    [],
                ),

            "pattern_length":
                pattern_data.get(
                    "length",
                    0,
                ),

            "matches":
                len(numbers),

            "number_counts":
                counts,

            "prediction":
                prediction,

            "bs_prediction":
                bs_prediction,

            "confidence":
                confidence,

        }

    # =====================================================
    # ANALYZE ALL PATTERNS
    # =====================================================

    def analyze(
        self,
        search_result: Dict,
    ) -> Dict:

        if not search_result:

            return {

                "bs":
                    None,

                "number":
                    None,

                "bs_candidates":
                    [],

                "number_candidates":
                    [],

            }

        # ---------------------------------------------
        # Longest B/S pattern
        # ---------------------------------------------

        longest_bs = (
            search_result.get(
                "longest_bs_pattern"
            )
        )

        bs_analysis = (
            self.analyze_bs_pattern(
                longest_bs
            )
        )

        # ---------------------------------------------
        # Longest Number pattern
        # ---------------------------------------------

        longest_number = (
            search_result.get(
                "longest_number_pattern"
            )
        )

        number_analysis = (
            self.analyze_number_pattern(
                longest_number
            )
        )

        # ---------------------------------------------
        # All B/S patterns
        # ---------------------------------------------

        bs_candidates = []

        for item in search_result.get(
            "bs_patterns",
            [],
        ):

            result = (
                self.analyze_bs_pattern(
                    item
                )
            )

            if result:

                bs_candidates.append(
                    result
                )

        # ---------------------------------------------
        # All Number patterns
        # ---------------------------------------------

        number_candidates = []

        for item in search_result.get(
            "number_patterns",
            [],
        ):

            result = (
                self.analyze_number_pattern(
                    item
                )
            )

            if result:

                number_candidates.append(
                    result
                )

        # ---------------------------------------------
        # Sort by confidence
        # ---------------------------------------------

        bs_candidates.sort(
            key=lambda x:
                x.get(
                    "confidence",
                    0.0,
                ),
            reverse=True,
        )

        number_candidates.sort(
            key=lambda x:
                x.get(
                    "confidence",
                    0.0,
                ),
            reverse=True,
        )

        result = {

            "bs":
                bs_analysis,

            "number":
                number_analysis,

            "bs_candidates":
                bs_candidates,

            "number_candidates":
                number_candidates,

        }

        logger.info(
            "Pattern analysis complete | "
            "BS=%s | Number=%s",
            bool(bs_analysis),
            bool(number_analysis),
        )

        return result
