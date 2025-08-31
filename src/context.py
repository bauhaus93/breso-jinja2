from enum import StrEnum

from context_page import CONTEXT_PAGE
from context_robots import CONTEXT_ROBOTS


class Context(StrEnum):
    PAGE = "page"
    ROBOTS = "robots"


COMMON_CONTEXT = {"domain": "https://brettspielsonntag.at"}


CONTEXT = {
    Context.PAGE: COMMON_CONTEXT | CONTEXT_PAGE,
    Context.ROBOTS: COMMON_CONTEXT | CONTEXT_ROBOTS,
}
print(CONTEXT.items())
