# =========================================================
# AI-BOT - SEARCH ENGINE
# =========================================================

from collections import Counter
from typing import Any, Dict, List, Optional


class SearchEngine:

    def __init__(
        self,
        min_length: int = 3,
        max_length: int = 12,
        min_matches: int = 1,
    ):

        self.min_length = min_length
        self.max_length = max_length
        self.min_matches = min_matches

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

            period = item.get("period")
            number = item.get("number")

            if period is None or number is None:
                continue

            try:
                number = int(number)
            except (ValueError, TypeError):
                continue

            bs = item.get("bs")

            if bs not in ("B", "S"):

                bs = (
                    "B"
                    if number >= 5
                    else "S"
                )

            result.append({
                "period": str(period),
                "number": number,
                "bs": bs,
                "time": item.get("time"),
            })

        return result

    # =====================================================
    # B/S SEQUENCE
    # =====================================================

    def get_sequence(
        self,
        history: List[Dict[str, Any]],
    ) -> str:

        return "".join(
            item["bs"]
            for item in history
            if item["bs"] in ("B", "S")
        )

    # =====================================================
    # LATEST PATTERN
    # =====================================================

    def latest_pattern(
        self,
        history: List[Dict[str, Any]],
        length: int,
    ) -> Optional[str]:

        history = self.normalize(history)

        if len(history) < length:
            return None

        sequence = self.get_sequence(history)

        if len(sequence) < length:
            return None

        return sequence[-length:]

    # =====================================================
    # SEARCH PATTERN
    # =====================================================

    def search(
        self,
        history: List[Dict[str, Any]],
        pattern: str,
    ) -> List[Dict[str, Any]]:

        history = self.normalize(history)

        pattern = pattern.upper().strip()

        if not pattern:
            return []

        if any(
            char not in ("B", "S")
            for char in pattern
        ):
            return []

        length = len(pattern)

        matches = []

        # Need one result after pattern
        if len(history) <= length:
            return []

        for index in range(
            len(history) - length
        ):

            window = history[
                index:index + length
            ]

            sequence = "".join(
                item["bs"]
                for item in window
            )

            if sequence != pattern:
                continue

            next_item = history[
                index + length
            ]

            matches.append({

                "pattern": pattern,

                "matched_period": (
                    window[-1]["period"]
                ),

                "next_period": (
                    next_item["period"]
                ),

                "next_number": (
                    next_item["number"]
                ),

                "next_bs": (
                    next_item["bs"]
                ),

                "next_time": (
                    next_item.get("time")
                ),
            })

        return matches

    # =====================================================
    # SEARCH LATEST
    # =====================================================

    def search_latest(
        self,
        history: List[Dict[str, Any]],
        length: int,
    ) -> Dict[str, Any]:

        history = self.normalize(history)

        pattern = self.latest_pattern(
            history,
            length,
        )

        if pattern is None:

            return {
                "pattern": None,
                "matches": [],
                "match_count": 0,
                "numbers": {},
                "bs": {},
            }

        matches = self.search(
            history,
            pattern,
        )

        number_counter = Counter(
            item["next_number"]
            for item in matches
        )

        bs_counter = Counter(
            item["next_bs"]
            for item in matches
        )

        return {

            "pattern": pattern,

            "matches": matches,

            "match_count": len(matches),

            "numbers": dict(
                number_counter
            ),

            "bs": dict(
                bs_counter
            ),
        }

    # =====================================================
    # SEARCH ALL PATTERN LENGTHS
    # =====================================================

    def search_all(
        self,
        history: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:

        history = self.normalize(history)

        results = []

        maximum = min(
            self.max_length,
            len(history) - 1,
        )

        for length in range(
            self.min_length,
            maximum + 1,
        ):

            result = self.search_latest(
                history,
                length,
            )

            if (
                result["match_count"]
                >= self.min_matches
            ):

                results.append({
                    "length": length,
                    **result,
                })

        return results

    # =====================================================
    # NUMBER COUNTS
    # =====================================================

    def number_counts(
        self,
        matches: List[Dict[str, Any]],
    ) -> Dict[int, int]:

        counter = Counter()

        for item in matches:

            number = item.get(
                "next_number"
            )

            if number is None:
                continue

            counter[int(number)] += 1

        return dict(
            sorted(
                counter.items()
            )
        )

    # =====================================================
    # B/S COUNTS
    # =====================================================

    def bs_counts(
        self,
        matches: List[Dict[str, Any]],
    ) -> Dict[str, int]:

        counter = Counter()

        for item in matches:

            bs = item.get(
                "next_bs"
            )

            if bs in ("B", "S"):

                counter[bs] += 1

        return dict(counter)

    # =====================================================
    # BEST RESULT
    # =====================================================

    def best_result(
        self,
        history: List[Dict[str, Any]],
    ) -> Optional[Dict[str, Any]]:

        results = self.search_all(
            history
        )

        if not results:
            return None

        # Prefer:
        # 1. More matches
        # 2. Longer pattern

        results.sort(
            key=lambda item: (
                item["match_count"],
                item["length"],
            ),
            reverse=True,
        )

        best = results[0]

        matches = best["matches"]

        number_counts = self.number_counts(
            matches
        )

        bs_counts = self.bs_counts(
            matches
        )

        best_number = None

        if number_counts:

            best_number = max(
                number_counts,
                key=number_counts.get,
            )

        best_bs = None

        if bs_counts:

            best_bs = max(
                bs_counts,
                key=bs_counts.get,
            )

        return {

            "pattern":
                best["pattern"],

            "length":
                best["length"],

            "match_count":
                best["match_count"],

            "matches":
                matches,

            "number_counts":
                number_counts,

            "bs_counts":
                bs_counts,

            "best_number":
                best_number,

            "best_bs":
                best_bs,
        }


# =========================================================
# HELPER
# =========================================================

def find_pattern(
    history: List[Dict[str, Any]],
    pattern: str,
) -> List[Dict[str, Any]]:

    engine = SearchEngine()

    return engine.search(
        history,
        pattern,
    )
