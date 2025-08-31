#!/usr/bin/env python3
import logging
import os
import sys
from functools import partial
from pathlib import Path
from socketserver import TCPServer, UnixStreamServer
from typing import Any, Dict, Tuple

from fastcgi import FcgiHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape

from context import CONTEXT, Context

logging.basicConfig(
    format="%(asctime)s - %(levelname)s:  %(message)s",
    level=logging.INFO,
)
_logger = logging.getLogger(__name__)


class FastCGIHandler(FcgiHandler):

    env: Environment = None
    context: Dict[Context, Dict[str, Any]] = None

    def __init__(self, env: Environment, context: Dict[str, Any], *args, **kwargs):
        self.env = env
        self.context = context
        super().__init__(*args, **kwargs)

    def handle(self):
        method = self.environ.get("REQUEST_METHOD")
        path = (self.environ.get("SCRIPT_FILENAME") or "").strip("/")
        query = self.environ.get("QUERY_STRING")
        print("method:", method)
        print("path:", path)
        print("query:", query)

        if path == "event.ics":
            data, content_type = self._get_next_event_ics()
        else:
            data, content_type = self._get_page(path)

        self._write_response(data, content_type=content_type)

    def _get_page(self, path: str) -> Tuple[str, str]:
        if path in {"/", ""}:
            path = "index"

        if path == "robots.txt":
            content_type = "text/plain"
            context = self.context[Context.ROBOTS]
            suffix = ".txt.j2"
        else:
            content_type = "text/html"
            context = self.context[Context.PAGE]
            suffix = ".html.j2"

        template_path = self._get_template_path(path, suffix)
        print(f"get tmpl: {template_path}")
        template = self.env.get_template(template_path)

        return template.render(context), content_type

    def _get_next_event_ics(self) -> Tuple[str, str]:
        return self.context["next_date_ics"], "text/calendar"

    def _write_response(self, body: str, content_type: str = "text/html") -> str:
        self["stdout"].write(
            f"Content-Type: {content_type}\r\n\r\n{body}\r\n".encode("utf-8")
        )

    def _get_template_path(self, path: str, suffix: str) -> str:
        return str((Path("pages") / path).with_suffix(suffix))


def _get_environment():
    templates = Path(".") / "src" / "templates"
    env = Environment(
        loader=FileSystemLoader(str(templates)), autoescape=select_autoescape()
    )
    return env


def main():
    handler = partial(FastCGIHandler, _get_environment(), CONTEXT)

    with UnixStreamServer("/tmp//breso.sock", handler) as srv:
        srv.serve_forever()


if __name__ == "__main__":
    main()
