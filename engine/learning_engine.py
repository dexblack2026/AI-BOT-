# =========================================================
# AI-BOT - LEARNING ENGINE
# =========================================================

import logging
from collections import Counter
from typing import Any, Dict, List, Optional


logger = logging.getLogger("LearningEngine")


class LearningEngine:

    def __init__(
        self,
        min_samples: int = 5,
    ):

        self.min_samples = max(
            1,
            min_samples,
        )

    # =====================================================
    # SAFE INT
    # =====================================================

    def safe_int(
        self,
        value: Any,
    ) -> Optional[int]:

        try:
            return int(value)
        except (
            ValueError,
            TypeError,
        ):
            return None

    # =====================================================
    # SAFE FLOAT
    # =====================================================

    def safe_float(
        self,
        value: Any,
    ) -> float:

        try:
            return float(value)
        except (
            ValueError,
            TypeError,
        ):
            return 0.0

    # =====================================================
    # ANALYZE RECORDS
    # =====================================================

    def analyze(
        self,
        records: List[
            Dict[str, Any]
        ],
    ) -> Dict[str, Any]:

        total = 0
        correct = 0

        pattern_stats = {}
        method_stats = {}

        for record in records:

            if not isinstance(
                record,
                dict,
            ):
                continue

            actual = record.get(
                "actual"
            )

            prediction = record.get(
                "prediction"
            )

            # Result မရှိသေးရင်
            # learning ထဲမထည့်
            if (
                actual is None
                or prediction is None
            ):
                continue

            actual = self.safe_int(
                actual
            )

            prediction = self.safe_int(
                prediction
            )

            if (
                actual is None
                or prediction is None
            ):
                continue

            total += 1

            is_correct = (
                actual == prediction
            )

            if is_correct:
                correct += 1

            # -------------------------------------------------
            # Pattern statistics
            # -------------------------------------------------

            pattern = record.get(
                "pattern"
            )

            if pattern:

                if pattern not in pattern_stats:

                    pattern_stats[
                        pattern
                    ] = {
                        "total": 0,
                        "correct": 0,
                    }

                pattern_stats[
                    pattern
                ]["total"] += 1

                if is_correct:

                    pattern_stats[
                        pattern
                    ]["correct"] += 1

            # -------------------------------------------------
            # Method statistics
            # -------------------------------------------------

            method = record.get(
                "method"
            )

            if method:

                if method not in method_stats:

                    method_stats[
                        method
                    ] = {
                        "total": 0,
                        "correct": 0,
                    }

                method_stats[
                    method
                ]["total"] += 1

                if is_correct:

                    method_stats[
                        method
                    ]["correct"] += 1

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

            "pattern_stats":
                self._calculate_rates(
                    pattern_stats
                ),

            "method_stats":
                self._calculate_rates(
                    method_stats
                ),
        }

    # =====================================================
    # CALCULATE RATES
    # =====================================================

    def _calculate_rates(
        self,
        stats: Dict[
            str,
            Dict[str, int]
        ],
    ) -> Dict[str, Any]:

        result = {}

        for key, value in stats.items():

            total = value.get(
                "total",
                0,
            )

            correct = value.get(
                "correct",
                0,
            )

            accuracy = (
                correct / total * 100
                if total
                else 0.0
            )

            result[key] = {

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

        return result

    # =====================================================
    # BEST PATTERNS
    # =====================================================

    def best_patterns(
        self,
        analysis: Dict[str, Any],
        limit: int = 10,
    ) -> List[
        Dict[str, Any]
    ]:

        pattern_stats = analysis.get(
            "pattern_stats",
            {},
        )

        candidates = []

        for pattern, stats in pattern_stats.items():

            total = stats.get(
                "total",
                0,
            )

            accuracy = self.safe_float(
                stats.get(
                    "accuracy",
                    0,
                )
            )

            if total < self.min_samples:
                continue

            candidates.append({

                "pattern":
                    pattern,

                "total":
                    total,

                "correct":
                    stats.get(
                        "correct",
                        0,
                    ),

                "accuracy":
                    accuracy,
            })

        candidates.sort(
            key=lambda item: (
                item["accuracy"],
                item["total"],
            ),
            reverse=True,
        )

        return candidates[:limit]

    # =====================================================
    # BEST METHODS
    # =====================================================

    def best_methods(
        self,
        analysis: Dict[str, Any],
    ) -> List[
        Dict[str, Any]
    ]:

        method_stats = analysis.get(
            "method_stats",
            {},
        )

        candidates = []

        for method, stats in method_stats.items():

            total = stats.get(
                "total",
                0,
            )

            accuracy = self.safe_float(
                stats.get(
                    "accuracy",
                    0,
                )
            )

            if total < self.min_samples:
                continue

            candidates.append({

                "method":
                    method,

                "total":
                    total,

                "correct":
                    stats.get(
                        "correct",
                        0,
                    ),

                "accuracy":
                    accuracy,
            })

        candidates.sort(
            key=lambda item: (
                item["accuracy"],
                item["total"],
            ),
            reverse=True,
        )

        return candidates

    # =====================================================
    # LEARNING SUMMARY
    # =====================================================

    def summary(
        self,
        records: List[
            Dict[str, Any]
        ],
    ) -> Dict[str, Any]:

        analysis = self.analyze(
            records
        )

        best_patterns = (
            self.best_patterns(
                analysis
            )
        )

        best_methods = (
            self.best_methods(
                analysis
            )
        )

        return {

            "overall":
                {
                    "total":
                        analysis[
                            "total"
                        ],

                    "correct":
                        analysis[
                            "correct"
                        ],

                    "wrong":
                        analysis[
                            "wrong"
                        ],

                    "accuracy":
                        analysis[
                            "accuracy"
                        ],
                },

            "best_patterns":
                best_patterns,

            "best_methods":
                best_methods,
        }

    # =====================================================
    # RECOMMENDATION
    # =====================================================

    def recommendation(
        self,
        records: List[
            Dict[str, Any]
        ],
    ) -> Dict[str, Any]:

        summary = self.summary(
            records
        )

        overall = summary[
            "overall"
        ]

        accuracy = self.safe_float(
            overall.get(
                "accuracy",
                0,
            )
        )

        # -------------------------------------------------
        # Learning state
        # -------------------------------------------------

        if overall["total"] < self.min_samples:

            status = "INSUFFICIENT_DATA"

        elif accuracy >= 70:

            status = "STRONG"

        elif accuracy >= 55:

            status = "MODERATE"

        else:

            status = "WEAK"

        best_method = None

        if summary[
            "best_methods"
        ]:

            best_method = (
                summary[
                    "best_methods"
                ][0]
            )

        return {

            "status":
                status,

            "accuracy":
                accuracy,

            "best_method":
                best_method,

            "best_patterns":
                summary[
                    "best_patterns"
                ],
        }


# =========================================================
# HELPER
# =========================================================

def learn(
    records: List[
        Dict[str, Any]
    ],
) -> Dict[str, Any]:

    engine = LearningEngine()

    return engine.recommendation(
        records
    )
