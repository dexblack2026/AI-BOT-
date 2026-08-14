# =========================================================
# AI-BOT - PATTERN ENGINE
# =========================================================

from collections import Counter
from typing import Any, Dict, List, Optional


class PatternEngine:

    def __init__(
        self,
        min_matches: int = 1,
    ):

        self.min_matches = max(
            1,
            min_matches,
        )

    # =====================================================
    # ANALYZE SEARCH RESULT
    # =====================================================

    def analyze(
        self,
        search_result: Optional[Dict[str, Any]],
    ) -> Optional[Dict[str, Any]]:

        if not search_result:
            return None

        matches = search_result.get(
            "matches",
            [],
        )

        if len(matches) < self.min_matches:
            return None

        pattern = search_result.get(
            "pattern"
        )

        if not pattern:
            return None

        # -------------------------------------------------
        # NUMBER
        # -------------------------------------------------

        number_counter = Counter()

        # -------------------------------------------------
        # B/S
        # -------------------------------------------------

        bs_counter = Counter()

        for match in matches:

            number = match.get(
                "next_number"
            )

            bs = match.get(
                "next_bs"
            )

            if number is not None:

                try:
                    number_counter[
                        int(number)
                    ] += 1

                except (
                    ValueError,
                    TypeError,
                ):
                    pass

            if bs in ("B", "S"):

                bs_counter[bs] += 1

        total = len(matches)

        # -------------------------------------------------
        # BEST NUMBER
        # -------------------------------------------------

        best_number = None
        best_number_count = 0

        if number_counter:

            best_number = max(
                number_counter,
                key=number_counter.get,
            )

            best_number_count = (
                number_counter[
                    best_number
                ]
            )

        # -------------------------------------------------
        # BEST B/S
        # -------------------------------------------------

        best_bs = None
        best_bs_count = 0

        if bs_counter:

            best_bs = max(
                bs_counter,
                key=bs_counter.get,
            )

            best_bs_count = (
                bs_counter[
                    best_bs
                ]
            )

        # -------------------------------------------------
        # RATES
        # -------------------------------------------------

        number_rate = 0.0

        if total:

            number_rate = (
                best_number_count
                / total
                * 100
            )

        bs_rate = 0.0

        if total:

            bs_rate = (
                best_bs_count
                / total
                * 100
            )

        # -------------------------------------------------
        # PATTERN STRENGTH
        # -------------------------------------------------

        pattern_length = len(
            pattern
        )

        length_score = min(
            pattern_length * 5,
            30,
        )

        match_score = min(
            total * 5,
            30,
        )

        frequency_score = (
            number_rate * 0.40
        )

        strength = (
            length_score
            + match_score
            + frequency_score
        )

        strength = min(
            100.0,
            round(
                strength,
                2,
            ),
        )

        return {

            "pattern":
                pattern,

            "pattern_length":
                pattern_length,

            "match_count":
                total,

            "number_counts":
                dict(
                    number_counter
                ),

            "bs_counts":
                dict(
                    bs_counter
                ),

            "best_number":
                best_number,

            "best_number_count":
                best_number_count,

            "number_rate":
                round(
                    number_rate,
                    2,
                ),

            "best_bs":
                best_bs,

            "best_bs_count":
                best_bs_count,

            "bs_rate":
                round(
                    bs_rate,
                    2,
                ),

            "strength":
                strength,
        }

    # =====================================================
    # ANALYZE ALL PATTERNS
    # =====================================================

    def analyze_all(
        self,
        search_results: List[
            Dict[str, Any]
        ],
    ) -> List[
        Dict[str, Any]
    ]:

        results = []

        for item in search_results:

            analyzed = self.analyze(
                item
            )

            if analyzed:

                results.append(
                    analyzed
                )

        # Strongest first
        results.sort(
            key=lambda item: (
                item["strength"],
                item["number_rate"],
                item["match_count"],
            ),
            reverse=True,
        )

        return results

    # =====================================================
    # BEST PATTERN
    # =====================================================

    def best_pattern(
        self,
        search_results: List[
            Dict[str, Any]
        ],
    ) -> Optional[
        Dict[str, Any]
    ]:

        results = self.analyze_all(
            search_results
        )

        if not results:

            return None

        return results[0]

    # =====================================================
    # COMPARE PATTERNS
    # =====================================================

    def compare(
        self,
        patterns: List[
            Dict[str, Any]
        ],
    ) -> Optional[
        Dict[str, Any]
    ]:

        if not patterns:

            return None

        number_votes = Counter()
        bs_votes = Counter()

        for pattern in patterns:

            number = pattern.get(
                "best_number"
            )

            bs = pattern.get(
                "best_bs"
            )

            strength = float(
                pattern.get(
                    "strength",
                    0,
                )
            )

            weight = max(
                1.0,
                strength / 20.0,
            )

            if number is not None:

                number_votes[
                    int(number)
                ] += weight

            if bs in ("B", "S"):

                bs_votes[bs] += weight

        best_number = None

        if number_votes:

            best_number = max(
                number_votes,
                key=number_votes.get,
            )

        best_bs = None

        if bs_votes:

            best_bs = max(
                bs_votes,
                key=bs_votes.get,
            )

        return {

            "best_number":
                best_number,

            "best_bs":
                best_bs,

            "number_votes":
                dict(
                    number_votes
                ),

            "bs_votes":
                dict(
                    bs_votes
                ),

            "pattern_count":
                len(patterns),
        }


# =========================================================
# HELPER
# =========================================================

def analyze_pattern(
    search_result: Dict[str, Any],
) -> Optional[Dict[str, Any]]:

    engine = PatternEngine()

    return engine.analyze(
        search_result
    )
