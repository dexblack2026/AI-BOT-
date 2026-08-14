# =========================================================
# AI-BOT - GAME API
# =========================================================

import asyncio
import json
import logging
import time

from typing import Any, Dict, List, Optional

import aiohttp

from config import (
    HEADERS,
    HISTORY_API_URL,
    ISSUE_API_URL,
    PAGE_NUMBER,
    PAGE_SIZE,
    REQUEST_TIMEOUT,
    MIN_NUMBER,
    MAX_NUMBER,
    BIG_MIN_NUMBER,
)


logger = logging.getLogger("GameAPI")


class GameAPI:

    def __init__(self):

        self.issue_url = ISSUE_API_URL
        self.history_url = HISTORY_API_URL

        self.headers = HEADERS.copy()

        self.session = None

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

            self.session = aiohttp.ClientSession(
                headers=self.headers,
                timeout=timeout,
            )

        return self.session

    # =====================================================
    # BUILD PAYLOAD
    # =====================================================

    def build_payload(
        self,
        pagination=False,
    ):

        payload = {

            "typeId": 1,

            "language": 7,

            "random":
                "t8g1dwtbcmujvsr72m8j5e465ukhrsh6",

            "timestamp":
                int(time.time()),

            "signature":
                "0000000000000000000000002B29B4CD",
        }

        if pagination:

            payload.update({

                "pageSize":
                    PAGE_SIZE,

                "pageNo":
                    PAGE_NUMBER,
            })

        return payload

    # =====================================================
    # POST
    # =====================================================

    async def post(
        self,
        url: str,
        payload: Dict[str, Any],
    ):

        session = await self.get_session()

        try:

            async with session.post(
                url,
                json=payload,
            ) as response:

                text = await response.text()

                if response.status != 200:

                    logger.error(
                        "HTTP %s: %s",
                        response.status,
                        text[:300],
                    )

                    return None

                if not text:

                    return None

                try:

                    return json.loads(text)

                except json.JSONDecodeError:

                    logger.error(
                        "Invalid JSON response"
                    )

                    return None

        except asyncio.TimeoutError:

            logger.error(
                "API request timeout"
            )

        except aiohttp.ClientError as error:

            logger.error(
                "API connection error: %s",
                error,
            )

        except Exception as error:

            logger.exception(
                "Unexpected API error: %s",
                error,
            )

        return None

    # =====================================================
    # CURRENT GAME
    # =====================================================

    async def get_current_game(
        self,
    ) -> Optional[Dict[str, Any]]:

        response = await self.post(
            self.issue_url,
            self.build_payload(),
        )

        if not isinstance(
            response,
            dict,
        ):

            return None

        data = response.get(
            "data"
        )

        if not isinstance(
            data,
            dict,
        ):

            data = response

        # -------------------------------------------------
        # PERIOD
        # -------------------------------------------------

        period = (

            data.get(
                "issueNumber"
            )

            or data.get(
                "issue"
            )

            or data.get(
                "issueNo"
            )

            or data.get(
                "period"
            )

            or data.get(
                "periodNumber"
            )
        )

        # -------------------------------------------------
        # TIME
        # -------------------------------------------------

        game_time = (

            data.get(
                "gameTime"
            )

            or data.get(
                "time"
            )

            or data.get(
                "drawTime"
            )

            or data.get(
                "timestamp"
            )
        )

        if period is None:

            return None

        return {

            "period":
                str(period),

            "time":
                game_time,

            "raw":
                data,
        }

    # =====================================================
    # HISTORY
    # =====================================================

    async def get_history(
        self,
    ) -> List[Dict[str, Any]]:

        response = await self.post(
            self.history_url,
            self.build_payload(
                pagination=True
            ),
        )

        if not isinstance(
            response,
            dict,
        ):

            return []

        raw_list = self.extract_list(
            response
        )

        history = []

        for item in raw_list:

            record = self.normalize_result(
                item
            )

            if record:

                history.append(
                    record
                )

        return self.clean_history(
            history
        )

    # =====================================================
    # EXTRACT LIST
    # =====================================================

    def extract_list(
        self,
        response: Dict[str, Any],
    ) -> List[Any]:

        data = response.get(
            "data"
        )

        # data = list
        if isinstance(
            data,
            list,
        ):

            return data

        # data = object
        if isinstance(
            data,
            dict,
        ):

            for key in (
                "list",
                "rows",
                "records",
                "history",
                "data",
            ):

                value = data.get(
                    key
                )

                if isinstance(
                    value,
                    list,
                ):

                    return value

        # root level
        for key in (
            "list",
            "rows",
            "records",
            "history",
        ):

            value = response.get(
                key
            )

            if isinstance(
                value,
                list,
            ):

                return value

        return []

    # =====================================================
    # NORMALIZE RESULT
    # =====================================================

    def normalize_result(
        self,
        item: Any,
    ) -> Optional[Dict[str, Any]]:

        if not isinstance(
            item,
            dict,
        ):

            return None

        # -------------------------------------------------
        # PERIOD
        # -------------------------------------------------

        period = (

            item.get(
                "issueNumber"
            )

            or item.get(
                "issue"
            )

            or item.get(
                "issueNo"
            )

            or item.get(
                "period"
            )

            or item.get(
                "periodNumber"
            )
        )

        # -------------------------------------------------
        # NUMBER
        # -------------------------------------------------

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

        if number is None:

            number = item.get(
                "num"
            )

        if number is None:

            number = item.get(
                "result"
            )

        # -------------------------------------------------
        # TIME
        # -------------------------------------------------

        game_time = (

            item.get(
                "gameTime"
            )

            or item.get(
                "time"
            )

            or item.get(
                "drawTime"
            )

            or item.get(
                "createdAt"
            )

            or item.get(
                "timestamp"
            )
        )

        if period is None:
            return None

        if number is None:
            return None

        try:

            number = int(
                number
            )

        except (
            ValueError,
            TypeError,
        ):

            return None

        if not (
            MIN_NUMBER
            <= number
            <= MAX_NUMBER
        ):

            return None

        # -------------------------------------------------
        # BIG / SMALL
        # -------------------------------------------------

        bs = (
            "B"
            if number >= BIG_MIN_NUMBER
            else "S"
        )

        return {

            "period":
                str(period),

            "number":
                number,

            "bs":
                bs,

            "time":
                game_time,
        }

    # =====================================================
    # CLEAN HISTORY
    # =====================================================

    def clean_history(
        self,
        history: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:

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

        result = list(
            unique.values()
        )

        try:

            result.sort(
                key=lambda x: int(
                    x["period"]
                )
            )

        except (
            ValueError,
            TypeError,
        ):

            result.sort(
                key=lambda x: str(
                    x["period"]
                )
            )

        return result

    # =====================================================
    # GET ALL DATA
    # =====================================================

    async def fetch_all(
        self,
    ):

        current_task = (
            self.get_current_game()
        )

        history_task = (
            self.get_history()
        )

        current, history = (
            await asyncio.gather(
                current_task,
                history_task,
            )
        )

        return {
            "current":
                current,

            "history":
                history,
        }

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


# =========================================================
# TEST
# =========================================================

async def test_api():

    logging.basicConfig(
        level=logging.INFO
    )

    api = GameAPI()

    try:

        data = await api.fetch_all()

        print()
        print(
            "=============================="
        )

        print(
            "CURRENT:"
        )

        print(
            data["current"]
        )

        print()
        print(
            "HISTORY:",
            len(
                data["history"]
            )
        )

        if data["history"]:

            print()
            print(
                "LATEST:"
            )

            print(
                data["history"][-1]
            )

        print(
            "=============================="
        )

    finally:

        await api.close()


# =========================================================
# DIRECT TEST
# =========================================================

if __name__ == "__main__":

    asyncio.run(
        test_api()
    )
