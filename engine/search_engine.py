# engine/search_engine.py

from collections import Counter
from typing import Dict, List, Optional


class SearchEngine:

    def __init__(
        self,
        min_matches: int = 3,
        max_pattern_length: int = 12,
    ):
        self.min_matches = min_matches
        self.max_pattern_length = max_pattern_length

    # =====================================================
    # SEQUENCE
    # =====================================================

    @staticmethod
    def to_sequence(data: List[dict]) -> List[str]:

        sequence = []

        for item in data:

            bs = item.get("bs")

            if bs in ("B", "S"):
                sequence.append(bs)

        return sequence

    # =====================================================
    # EXACT SEARCH
    # =====================================================

    def find_exact_matches(
        self,
        sequence: List[str],
        pattern: str,
    ) -> List[dict]:

        results = []

        pattern_length = len(pattern)

        if pattern_length == 0:
            return results

        # နောက်က result ရှိတဲ့နေရာအထိပဲရှာ
        for i in range(
            0,
            len(sequence) - pattern_length
        ):

            current = "".join(
                sequence[
                    i:i + pattern_length
                ]
            )

            if current != pattern:
                continue

            next_index = i + pattern_length

            if next_index >= len(sequence):
                continue

            next_result = sequence[next_index]

            results.append({
                "index": i,
                "pattern": pattern,
                "next": next_result,
            })

        return results

    # =====================================================
    # NEXT RESULT COUNTER
    # =====================================================

    def count_next_results(
        self,
        matches: List[dict],
    ) -> Dict[str, int]:

        counter = Counter()

        for match in matches:

            result = match.get("next")

            if result in ("B", "S"):
                counter[result] += 1

        return {
            "B": counter["B"],
            "S": counter["S"],
            "total": (
                counter["B"] +
                counter["S"]
            ),
        }

    # =====================================================
    # SEARCH ONE PATTERN
    # =====================================================

    def search_pattern(
        self,
        sequence: List[str],
        pattern: str,
    ) -> Optional[dict]:

        matches = self.find_exact_matches(
            sequence,
            pattern,
        )

        if len(matches) < self.min_matches:
            return None

        counts = self.count_next_results(
            matches
        )

        total = counts["total"]

        if total == 0:
            return None

        if counts["B"] > counts["S"]:

            prediction = "B"

        elif counts["S"] > counts["B"]:

            prediction = "S"

        else:

            prediction = None

        rate = 0.0

        if prediction:

            rate = (
                counts[prediction]
                / total
                * 100
            )

        return {
            "pattern": pattern,
            "length": len(pattern),
            "matches": len(matches),
            "B": counts["B"],
            "S": counts["S"],
            "prediction": prediction,
            "historical_rate": round(
                rate,
                2
            ),
            "locations": [
                match["index"]
                for match in matches
            ],
        }

    # =====================================================
    # SEARCH LONGEST PATTERN
    # =====================================================

    def search_longest(
        self,
        sequence: List[str],
        min_length: int = 3,
    ) -> Optional[dict]:

        if len(sequence) < min_length:
            return None

        max_length = min(
            self.max_pattern_length,
            len(sequence) - 1,
        )

        # အရှည်ဆုံးကနေ စရှာ
        for length in range(
            max_length,
            min_length - 1,
            -1,
        ):

            pattern = "".join(
                sequence[-length:]
            )

            result = self.search_pattern(
                sequence,
                pattern,
            )

            if result is not None:

                return result

        return None

    # =====================================================
    # SEARCH ALL LENGTHS
    # =====================================================

    def search_all(
        self,
        sequence: List[str],
        min_length: int = 3,
    ) -> List[dict]:

        results = []

        if len(sequence) < min_length:
            return results

        max_length = min(
            self.max_pattern_length,
            len(sequence) - 1,
        )

        for length in range(
            min_length,
            max_length + 1,
        ):

            pattern = "".join(
                sequence[-length:]
            )

            result = self.search_pattern(
                sequence,
                pattern,
            )

            if result is not None:

                results.append(result)

        # Pattern length အရှည်ဆုံးကို အပေါ်တင်
        results.sort(
            key=lambda x: (
                x["length"],
                x["historical_rate"],
                x["matches"],
            ),
            reverse=True,
        )

        return results

    # =====================================================
    # SIMILAR SEQUENCE SEARCH
    # =====================================================

    def find_similar_sequences(
        self,
        sequence: List[str],
        target_length: int = 6,
    ) -> List[dict]:

        results = []

        if len(sequence) <= target_length:
            return results

        target = sequence[-target_length:]

        for i in range(
            len(sequence) - target_length
        ):

            candidate = sequence[
                i:i + target_length
            ]

            if candidate == target:
                continue

            similarity = self.sequence_similarity(
                target,
                candidate,
            )

            results.append({
                "index": i,
                "sequence": "".join(candidate),
                "similarity": round(
                    similarity,
                    2
                ),
                "next": (
                    sequence[i + target_length]
                    if (
                        i + target_length
                        < len(sequence)
                    )
                    else None
                ),
            })

        results.sort(
            key=lambda x: x["similarity"],
            reverse=True,
        )

        return results

    # =====================================================
    # SIMILARITY
    # =====================================================

    @staticmethod
    def sequence_similarity(
        a: List[str],
        b: List[str],
    ) -> float:

        if not a or not b:
            return 0.0

        length = min(
            len(a),
            len(b),
        )

        if length == 0:
            return 0.0

        same = 0

        for i in range(length):

            if a[i] == b[i]:
                same += 1

        return (
            same / length * 100
        )

    # =====================================================
    # SUMMARY
    # =====================================================

    def analyze(
        self,
        data: List[dict],
    ) -> dict:

        sequence = self.to_sequence(data)

        if len(sequence) < 3:

            return {
                "sequence": "",
                "length": len(sequence),
                "pattern": None,
                "similar": [],
                "status": "INSUFFICIENT_DATA",
            }

        longest = self.search_longest(
            sequence
        )

        similar = self.find_similar_sequences(
            sequence,
            target_length=min(
                6,
                len(sequence) - 1,
            ),
        )

        return {
            "sequence": "".join(sequence),
            "length": len(sequence),
            "pattern": longest,
            "similar": similar[:20],
            "status": "OK",
        }
