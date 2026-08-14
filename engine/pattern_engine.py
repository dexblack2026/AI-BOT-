# engine/pattern_engine.py

from collections import Counter
from typing import Dict, List, Optional


class PatternEngine:

    def __init__(
        self,
        min_length: int = 3,
        max_length: int = 12,
        min_matches: int = 3,
    ):
        self.min_length = min_length
        self.max_length = max_length
        self.min_matches = min_matches

    # =====================================================
    # CURRENT CONTEXT
    # =====================================================

    def current_context(
        self,
        sequence: List[str],
        length: int,
    ) -> str:

        if not sequence:
            return ""

        length = min(
            length,
            len(sequence)
        )

        return "".join(
            sequence[-length:]
        )

    # =====================================================
    # FIND PATTERN
    # =====================================================

    def find_pattern(
        self,
        sequence: List[str],
        pattern: str,
    ) -> List[Dict]:

        results = []

        if not pattern:
            return results

        length = len(pattern)

        for i in range(
            len(sequence) - length
        ):

            current = "".join(
                sequence[
                    i:i + length
                ]
            )

            if current != pattern:
                continue

            next_index = i + length

            if next_index >= len(sequence):
                continue

            next_result = sequence[
                next_index
            ]

            results.append({
                "index": i,
                "pattern": pattern,
                "next": next_result,
            })

        return results

    # =====================================================
    # PATTERN STATISTICS
    # =====================================================

    def pattern_statistics(
        self,
        sequence: List[str],
        pattern: str,
    ) -> Optional[Dict]:

        matches = self.find_pattern(
            sequence,
            pattern,
        )

        if len(matches) < self.min_matches:
            return None

        counter = Counter(
            item["next"]
            for item in matches
        )

        total = (
            counter["B"] +
            counter["S"]
        )

        if total == 0:
            return None

        prediction = None

        if counter["B"] > counter["S"]:
            prediction = "B"

        elif counter["S"] > counter["B"]:
            prediction = "S"

        if prediction:

            rate = (
                counter[prediction]
                / total
                * 100
            )

        else:

            rate = 50.0

        return {
            "pattern": pattern,
            "length": len(pattern),
            "matches": len(matches),
            "B": counter["B"],
            "S": counter["S"],
            "prediction": prediction,
            "rate": round(rate, 2),
        }

    # =====================================================
    # ANALYZE ALL CURRENT PATTERNS
    # =====================================================

    def analyze_patterns(
        self,
        sequence: List[str],
    ) -> List[Dict]:

        results = []

        if len(sequence) < self.min_length:
            return results

        max_length = min(
            self.max_length,
            len(sequence) - 1,
        )

        for length in range(
            self.min_length,
            max_length + 1,
        ):

            pattern = self.current_context(
                sequence,
                length,
            )

            stats = self.pattern_statistics(
                sequence,
                pattern,
            )

            if stats:

                results.append(stats)

        # အရှည်ဆုံး pattern ကို ဦးစားပေး
        results.sort(
            key=lambda x: (
                x["length"],
                x["matches"],
                x["rate"],
            ),
            reverse=True,
        )

        return results

    # =====================================================
    # RUN-LENGTH PATTERN
    # =====================================================

    def get_current_run(
        self,
        sequence: List[str],
    ) -> Dict:

        if not sequence:

            return {
                "type": None,
                "length": 0,
                "pattern": "",
            }

        current = sequence[-1]

        count = 0

        for value in reversed(sequence):

            if value != current:
                break

            count += 1

        return {
            "type": current,
            "length": count,
            "pattern": current * count,
        }

    # =====================================================
    # ALTERNATING PATTERN
    # =====================================================

    def detect_alternating(
        self,
        sequence: List[str],
        min_length: int = 4,
    ) -> Optional[Dict]:

        if len(sequence) < min_length:
            return None

        current = sequence[-min_length:]

        for i in range(1, len(current)):

            if current[i] == current[i - 1]:

                return None

        return {
            "pattern": "".join(current),
            "type": "ALTERNATING",
            "length": len(current),
        }

    # =====================================================
    # STREAK PATTERN
    # =====================================================

    def detect_streak(
        self,
        sequence: List[str],
    ) -> Optional[Dict]:

        run = self.get_current_run(
            sequence
        )

        if run["length"] < 2:
            return None

        return {
            "pattern": run["pattern"],
            "type": "STREAK",
            "value": run["type"],
            "length": run["length"],
        }

    # =====================================================
    # TRANSITION PATTERN
    # =====================================================

    def transition_pattern(
        self,
        sequence: List[str],
        length: int = 5,
    ) -> Optional[Dict]:

        if len(sequence) < length + 1:
            return None

        context = sequence[-length:]

        transitions = []

        for i in range(
            1,
            len(context)
        ):

            transitions.append(
                context[i - 1]
                + "→"
                + context[i]
            )

        return {
            "pattern": "".join(context),
            "transitions": transitions,
            "length": len(context),
        }

    # =====================================================
    # FULL PATTERN ANALYSIS
    # =====================================================

    def analyze(
        self,
        sequence: List[str],
    ) -> Dict:

        if not sequence:

            return {
                "status": "NO_DATA",
                "patterns": [],
            }

        patterns = self.analyze_patterns(
            sequence
        )

        run = self.detect_streak(
            sequence
        )

        alternating = self.detect_alternating(
            sequence
        )

        transition = self.transition_pattern(
            sequence
        )

        return {
            "status": "OK",
            "current": "".join(
                sequence[-12:]
            ),
            "patterns": patterns,
            "run": run,
            "alternating": alternating,
            "transition": transition,
        }
