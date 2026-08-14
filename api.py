# =========================================================
# AI-BOT - GAME API
# SC 60s GAME
# =========================================================

import asyncio
import json
import logging
import os
import time

from typing import Dict, List, Optional, Tuple

import aiohttp

from config import (
    HEADERS,
    HISTORY_API_URL,
    ISSUE_API_URL,
    PAGE_NUMBER,
    PAGE_SIZE,
    REQUEST_TIMEOUT,
    DATA_FILE,
    MAX_HISTORY,
    BIG_THRESHOLD,
)


logger = logging.getLogger("GameAPI")


class GameAPI:

    # =====================================================
    # INIT
    # =====================================================

    def __init__(
        self,
        issue_url: str = ISSUE_API_URL,
        history_url: str = HISTORY_API_URL,
        headers: Optional[dict] = None,
    ):

        self.issue_url = issue_url

        self.history_url = history_url

        self.headers = (
            headers
            if headers is not None
            else HEADERS.copy()
        )

        self.session: Optional[
            aiohttp.ClientSession
        ] = None

    # =====================================================
    # SESSION
    # =====================================================

    async def get_session(self):

        if (
            self.session is None
            or self.session.closed
        ):

            timeout = aiohttp.ClientTimeout(
                total=REQUEST_TIMEOUT
            )

            self.session = (
                aiohttp.ClientSession(
                    headers=self.headers,
                    timeout=timeout,
                )
            )

        return self.session

    # =====================================================
    # BUILD PAYLOAD
    # =====================================================

    def build_payload(self) -> dict:

        return {

            "typeId": 1,

            "language": 7,

            "random":
                "yylpj8cxd125q9vy7jyousm0d59m2hgq",

            "timestamp":
                int(time.time()),

            "signature":
                "0000000000000000000000005763BF05",
        }

    # =====================================================
    # POST REQUEST
    # =====================================================

    async def post(
        self,
        url: str,
        payload: dict,
    ):

        session = await self.get_session()

        try:

            async with session.post(
                url,
                json=payload,
            ) as response:

                if response.status != 200:

                    logger.error(
                        "API HTTP %s: %s",
                        response.status,
                        url,
                    )

                    return None

                text = await response.text()

                if not text:

                    logger.error(
                        "Empty API response: %s",
                        url,
                    )

                    return None

                try:

                    return json.loads(
                        text
                    )

                except json.JSONDecodeError:

                    logger.error(
                        "Invalid JSON response: %s",
                        url,
                    )

                    return None

        except asyncio.TimeoutError:

            logger.error(
                "API timeout: %s",
                url,
            )

        except aiohttp.ClientError as error:

            logger.error(
                "Network error: %s",
                error,
            )

        except Exception as error:

            logger.exception(
                "Unexpected API error: %s",
                error,
            )

        return None

    # =====================================================
    # CURRENT PERIOD
    # =====================================================

    async def get_current_period(
        self,
    ) -> Optional[str]:

        payload = self.build_payload()

        response = await self.post(
            self.issue_url,
            payload,
        )

        if not isinstance(
            response,
            dict,
        ):

            return None

        data = response.get(
            "data"
        )

        # ---------------------------------------------
        # data = dict
        # ---------------------------------------------

        if isinstance(
            data,
            dict,
        ):

            period = (
                data.get("issueNumber")
                or data.get("issue")
                or data.get("period")
            )

            if period is not None:

                return str(
                    period
                ).strip()

        # ---------------------------------------------
        # data = string / integer
        # ---------------------------------------------

        if isinstance(
            data,
            (str, int),
        ):

            return str(
                data
            ).strip()

        # ---------------------------------------------
        # fallback
        # ---------------------------------------------

        period = (
            response.get(
                "issueNumber"
            )
            or response.get(
                "issue"
            )
            or response.get(
                "period"
            )
        )

        if period is not None:

            return str(
                period
            ).strip()

        return None

    # =====================================================
    # HISTORY
    # =====================================================

    async def get_history(
        self,
    ) -> List[Dict]:

        payload = self.build_payload()

        payload.update({

            "pageSize":
                PAGE_SIZE,

            "pageNo":
                PAGE_NUMBER,

        })

        response = await self.post(
            self.history_url,
            payload,
        )

        if not isinstance(
            response,
            dict,
        ):

            return []

        # ---------------------------------------------
        # Extract data
        # ---------------------------------------------

        raw_data = (
            response.get("data")
            or response.get("list")
            or []
        )

        if isinstance(
            raw_data,
            dict,
        ):

            results = (
                raw_data.get("list")
                or raw_data.get("rows")
                or raw_data.get("data")
                or []
            )

        elif isinstance(
            raw_data,
            list,
        ):

            results = raw_data

        else:

            results = []

        # ---------------------------------------------
        # Parse
        # ---------------------------------------------

        history = []

        for item in results:

            if not isinstance(
                item,
                dict,
            ):

                continue

            # -----------------------------------------
            # Period
            # -----------------------------------------

            period = (
                item.get(
                    "issueNumber"
                )
                or item.get(
                    "issue"
                )
                or item.get(
                    "period"
                )
            )

            # -----------------------------------------
            # Number
            # -----------------------------------------

            number = (
                item.get(
                    "number"
                )
                if item.get(
                    "number"
                ) is not None
                else item.get(
                    "resultNum"
                )
            )

            if period is None:
                continue

            if number is None:
                continue

            try:

                number = int(
                    number
                )

            except (
                ValueError,
                TypeError,
            ):

                continue

            # -----------------------------------------
            # Validate Number
            # -----------------------------------------

            if number < 0 or number > 9:

                continue

            # -----------------------------------------
            # B / S
            # -----------------------------------------

            bs = (
                "B"
                if number >= BIG_THRESHOLD
                else "S"
            )

            history.append({

                "period":
                    str(period).strip(),

                "number":
                    number,

                "bs":
                    bs,

            })

        return self.clean_history(
            history
        )

    # =====================================================
    # CLEAN HISTORY
    # =====================================================

    def clean_history(
        self,
        history: List[Dict],
    ) -> List[Dict]:

        unique = {}

        for item in history:

            period = item.get(
                "period"
            )

            if not period:

                continue

            unique[
                str(period)
            ] = item

        cleaned = list(
            unique.values()
        )

        # ---------------------------------------------
        # Sort oldest → newest
        # ---------------------------------------------

        try:

            cleaned.sort(
                key=lambda x: int(
                    x["period"]
                )
            )

        except (
            ValueError,
            TypeError,
        ):

            cleaned.sort(
                key=lambda x: x["period"]
            )

        return cleaned

    # =====================================================
    # SAVE HISTORY
    # =====================================================

    def save_history(
        self,
        history: List[Dict],
    ) -> List[Dict]:

        existing = []

        # ---------------------------------------------
        # Create directory
        # ---------------------------------------------

        directory = os.path.dirname(
            DATA_FILE
        )

        if directory:

            os.makedirs(
                directory,
                exist_ok=True,
            )

        # ---------------------------------------------
        # Load existing
        # ---------------------------------------------

        if os.path.exists(
            DATA_FILE
        ):

            try:

                with open(
                    DATA_FILE,
                    "r",
                    encoding="utf-8",
                ) as file:

                    data = json.load(
                        file
                    )

                    if isinstance(
                        data,
                        list,
                    ):

                        existing = data

            except (
                json.JSONDecodeError,
                OSError,
            ) as error:

                logger.warning(
                    "Could not load history: %s",
                    error,
                )

        # ---------------------------------------------
        # Merge
        # ---------------------------------------------

        combined = (
            existing + history
        )

        cleaned = (
            self.clean_history(
                combined
            )
        )

        # ---------------------------------------------
        # Limit history
        # ---------------------------------------------

        cleaned = cleaned[
            -MAX_HISTORY:
        ]

        # ---------------------------------------------
        # Save
        # ---------------------------------------------

        try:

            with open(
                DATA_FILE,
                "w",
                encoding="utf-8",
            ) as file:

                json.dump(
                    cleaned,
                    file,
                    indent=4,
                    ensure_ascii=False,
                )

        except OSError as error:

            logger.error(
                "History save error: %s",
                error,
            )

        return cleaned

    # =====================================================
    # LOAD HISTORY
    # =====================================================

    def load_history(
        self,
    ) -> List[Dict]:

        if not os.path.exists(
            DATA_FILE
        ):

            return []

        try:

            with open(
                DATA_FILE,
                "r",
                encoding="utf-8",
            ) as file:

                data = json.load(
                    file
                )

            if not isinstance(
                data,
                list,
            ):

                return []

            return self.clean_history(
                data
            )

        except (
            json.JSONDecodeError,
            OSError,
        ) as error:

            logger.error(
                "History load error: %s",
                error,
            )

            return []

    # =====================================================
    # FETCH ALL
    # =====================================================

    async def fetch_all(
        self,
    ) -> Tuple[
        Optional[str],
        List[Dict],
    ]:

        # ---------------------------------------------
        # Request both APIs together
        # ---------------------------------------------

        period_task = (
            self.get_current_period()
        )

        history_task = (
            self.get_history()
        )

        period, history = (
            await asyncio.gather(
                period_task,
                history_task,
            )
        )

        # ---------------------------------------------
        # If API history available
        # ---------------------------------------------

        if history:

            history = self.save_history(
                history
            )

        # ---------------------------------------------
        # Fallback local history
        # ---------------------------------------------

        else:

            history = self.load_history()

        logger.info(
            "Current Period: %s | History: %d",
            period,
            len(history),
        )

        return (
            period,
            history,
        )

    # =====================================================
    # CLOSE
    # =====================================================

    async def close(
        self,
    ):

        if (
            self.session is not None
            and not self.session.closed
        ):

            await self.session.close()

            self.session = None

            logger.info(
                "API session closed."
            )
