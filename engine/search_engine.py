# =========================================================
# AI-BOT - SEARCH ENGINE
# =========================================================

import logging
from typing import Dict, List, Optional

from config import (
    MIN_HISTORY_MATCHES,
    MIN_PATTERN_LENGTH,
    MAX_PATTERN_LENGTH,
)


logger = logging.getLogger("SearchEngine")


class SearchEngine:

    # =====================================================
    # INIT
    # =====================================================

    def __init__(
        self,
        min_matches: int = MIN_HISTORY_MATCHES,
        min_length: int = MIN_PATTERN_LENGTH,
        max_length: int = MAX_PATTERN_LENGTH,
    ):

        self.min_matches = min_matches
        self.min_length = min_length
        self.max_length = max_length

    # =====================================================
    # NUMBER SEQUENCE
    # =====================================================

    @staticmethod
    def number_sequence(
        history: List[Dict],
    ) -> List[int]:

        sequence = []

        for item in history:

            number = item.get("number")

            try:
                sequence.append(
                    int(number)
                )

            except (
                ValueError,
                TypeError,
            ):

                continue

        return sequence

    # =====================================================
    # B/S SEQUENCE
    # =====================================================

    @staticmethod
    def bs_sequence(
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
    # EXACT NUMBER CONTEXT SEARCH
    # =====================================================

    def search_number_context(
        self,
        sequence: List[int],
        pattern: List[int],
    ) -> List[int]:

        if not sequence or not pattern:
            return []

        length = len(pattern)

        results = []

        # Need one result after the pattern
        for i in range(
            len(sequence) - length
        ):

            current = sequence[
                i:i + length
            ]

            if current == pattern:

                next_index = i + length

                if next_index < len(sequence):

                    results.append(
                        sequence[next_index]
                    )

        return results

    # =====================================================
    # EXACT B/S CONTEXT SEARCH
    # =====================================================

    def search_bs_context(
        self,
        sequence: List[str],
        pattern: str,
    ) -> List[str]:

        if not sequence or not pattern:
            return []

        length = len(pattern)

        results = []

        for i in range(
            len(sequence) - length
        ):

            current = "".join(
                sequence[
                    i:i + length
                ]
            )

            if current == pattern:

                next_index = i + length

                if next_index < len(sequence):

                    results.append(
                        sequence[next_index]
                    )

        return results

    # =====================================================
    # FIND LONGEST B/S PATTERN
    # =====================================================

    def find_longest_bs_pattern(
        self,
        history: List[Dict],
    ) -> Optional[Dict]:

        sequence = self.bs_sequence(
            history
        )

        if len(sequence) < self.min_length + 1:

            return None

        maximum = min(
            self.max_length,
            len(sequence) - 1,
        )

        # Longest → shortest
        for length in range(
            maximum,
            self.min_length - 1,
            -1,
        ):

            pattern = "".join(
                sequence[-length:]
            )

            matches = (
                self.search_bs_context(
                    sequence[:-1],
                    pattern,
                )
            )

            if len(matches) >= self.min_matches:

                return {

                    "pattern":
                        pattern,

                    "length":
                        length,

                    "matches":
                        matches,

                    "match_count":
                        len(matches),

                }

        return None

    # =====================================================
    # FIND LONGEST NUMBER PATTERN
    # =====================================================

    def find_longest_number_pattern(
        self,
        history: List[Dict],
    ) -> Optional[Dict]:

        sequence = self.number_sequence(
            history
        )

        if len(sequence) < self.min_length + 1:

            return None

        maximum = min(
            self.max_length,
            len(sequence) - 1,
        )

        for length in range(
            maximum,
            self.min_length - 1,
            -1,
        ):

            pattern = sequence[
                -length:
            ]

            matches = (
                self.search_number_context(
                    sequence[:-1],
                    pattern,
                )
            )

            if len(matches) >= self.min_matches:

                return {

                    "pattern":
                        pattern,

                    "length":
                        length,

                    "matches":
                        matches,

                    "match_count":
                        len(matches),

                }

        return None

    # =====================================================
    # SEARCH ALL B/S PATTERNS
    # =====================================================

    def search_bs_patterns(
        self,
        history: List[Dict],
    ) -> List[Dict]:

        sequence = self.bs_sequence(
            history
        )

        if len(sequence) < self.min_length + 1:

            return []

        results = []

        maximum = min(
            self.max_length,
            len(sequence) - 1,
        )

        for length in range(
            maximum,
            self.min_length - 1,
            -1,
        ):

            pattern = "".join(
                sequence[-length:]
            )

            matches = (
                self.search_bs_context(
                    sequence[:-1],
                    pattern,
                )
            )

            if len(matches) >= self.min_matches:

                results.append({

                    "pattern":
                        pattern,

                    "length":
                        length,

                    "matches":
                        matches,

                    "match_count":
                        len(matches),

                })

        return results

    # =====================================================
    # SEARCH ALL NUMBER PATTERNS
    # =====================================================

    def search_number_patterns(
        self,
        history: List[Dict],
    ) -> List[Dict]:

        sequence = self.number_sequence(
            history
        )

        if len(sequence) < self.min_length + 1:

            return []

        results = []

        maximum = min(
            self.max_length,
            len(sequence) - 1,
        )

        for length in range(
            maximum,
            self.min_length - 1,
            -1,
        ):

            pattern = sequence[
                -length:
            ]

            matches = (
                self.search_number_context(
                    sequence[:-1],
                    pattern,
                )
            )

            if len(matches) >= self.min_matches:

                results.append({

                    "pattern":
                        pattern,

                    "length":
                        length,

                    "matches":
                        matches,

                    "match_count":
                        len(matches),

                })

        return results

    # =====================================================
    # CURRENT RUN
    # =====================================================

    @staticmethod
    def current_bs_run(
        history: List[Dict],
    ) -> Dict:

        sequence = SearchEngine.bs_sequence(
            history
        )

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
    # COMPLETE SEARCH
    # =====================================================

    def search(
        self,
        history: List[Dict],
    ) -> Dict:

        if not history:

            return {

                "history_size": 0,

                "bs_sequence": [],

                "number_sequence": [],

                "current_run": None,

                "longest_bs_pattern": None,

                "longest_number_pattern": None,

                "bs_patterns": [],

                "number_patterns": [],

            }

        bs_seq = self.bs_sequence(
            history
        )

        number_seq = self.number_sequence(
            history
        )

        result = {

            "history_size":
                len(history),

            "bs_sequence":
                bs_seq,

            "number_sequence":
                number_seq,

            "current_run":
                self.current_bs_run(
                    history
                ),

            "longest_bs_pattern":
                self.find_longest_bs_pattern(
                    history
                ),

            "longest_number_pattern":
                self.find_longest_number_pattern(
                    history
                ),

            "bs_patterns":
                self.search_bs_patterns(
                    history
                ),

            "number_patterns":
                self.search_number_patterns(
                    history
                ),

        }

        logger.info(
            "Search complete | history=%d",
            len(history),
        )

        return result
