import asyncio
import json
import logging
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
)


logger = logging.getLogger("GameAPI")


class GameAPI:

    def __init__(
        self,
        issue_url: str = ISSUE_API_URL,
        history_url: str = HISTORY_API_URL,
        headers: Optional[dict] = None,
    ):
        self.issue_url = issue_url
        self.history_url = history_url
        self.headers = headers or HEADERS
        self.session: Optional[aiohttp.ClientSession] = None

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
    # REQUEST
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
                        "API Error: %s | %s",
                        response.status,
                        url,
                    )

                    return None

                text = await response.text()

                if not text:
                    return None

                try:
                    return json.loads(text)

                except json.JSONDecodeError:

                    logger.error(
                        "Invalid JSON response."
                    )

                    return None

        except asyncio.TimeoutError:

            logger.error(
                "Request timeout: %s",
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
    # PAYLOAD
    # =====================================================

    def build_payload(self) -> dict:

        return {
            "typeId": 1,
            "language": 7,
            "random": (
                "t8g1dwtbcmujvsr72m8j5e465ukhrsh6"
            ),
            "timestamp": int(time.time()),
            "signature": (
                "0000000000000000000000002B29B4CD"
            ),
        }

    # =====================================================
    # CURRENT ISSUE
    # =====================================================

    async def get_current_issue(
        self,
    ) -> Optional[str]:

        response = await self.post(
            self.issue_url,
            self.build_payload(),
        )

        if not isinstance(response, dict):
            return None

        data = response.get("data")

        if isinstance(data, dict):

            issue = (
                data.get("issueNumber")
                or data.get("issue")
            )

            if issue is not None:
                return str(issue)

        elif isinstance(data, (str, int)):

            return str(data)

        return None

    # =====================================================
    # HISTORY
    # =====================================================

    async def get_history(
        self,
    ) -> List[Dict]:

        payload = self.build_payload()

        payload.update({
            "pageSize": PAGE_SIZE,
            "pageNo": PAGE_NUMBER,
        })

        response = await self.post(
            self.history_url,
            payload,
        )

        if not isinstance(response, dict):
            return []

        raw_data = (
            response.get("data")
            or response.get("list")
            or []
        )

        if isinstance(raw_data, dict):

            results = (
                raw_data.get("list")
                or raw_data.get("rows")
                or []
            )

        elif isinstance(raw_data, list):

            results = raw_data

        else:

            results = []

        history = []

        for item in results:

            if not isinstance(item, dict):
                continue

            issue = (
                item.get("issueNumber")
                or item.get("issue")
            )

            number = (
                item.get("number")
                if item.get("number") is not None
                else item.get("resultNum")
            )

            if issue is None or number is None:
                continue

            try:
                number = int(number)

            except (ValueError, TypeError):
                continue

            # =============================================
            # Big / Small
            # =============================================

            bs = "B" if number >= 5 else "S"

            history.append({
                "issue": str(issue),
                "number": number,
                "bs": bs,
            })

        return self.clean_history(history)

    # =====================================================
    # CLEAN HISTORY
    # =====================================================

    def clean_history(
        self,
        history: List[Dict],
    ) -> List[Dict]:

        unique = {}

        for item in history:

            issue = item.get("issue")

            if not issue:
                continue

            unique[str(issue)] = item

        cleaned = list(unique.values())

        # Oldest → Newest
        try:

            cleaned.sort(
                key=lambda x: int(x["issue"])
            )

        except (ValueError, TypeError):

            cleaned.sort(
                key=lambda x: x["issue"]
            )

        return cleaned

    # =====================================================
    # FETCH ALL
    # =====================================================

    async def fetch_all(
        self,
    ) -> Tuple[
        Optional[str],
        List[Dict],
    ]:

        issue_task = self.get_current_issue()
        history_task = self.get_history()

        issue, history = await asyncio.gather(
            issue_task,
            history_task,
        )

        logger.info(
            "Current Issue: %s | History: %d",
            issue,
            len(history),
        )

        return issue, history

    # =====================================================
    # CLOSE
    # =====================================================

    async def close(self):

        if (
            self.session is not None
            and not self.session.closed
        ):

            await self.session.close()

            self.session = None
