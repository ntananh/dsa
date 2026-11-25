"""Convert LeetCode problem HTML to Markdown for offline reading.

Covers the tags LeetCode descriptions use: p, div, pre, ul, ol, li, strong,
b, em, i, code, sup, sub, img, br. Other tags keep only their text.
"""

import re
from html.parser import HTMLParser

INLINE_MARKERS = {"strong": "**", "b": "**", "em": "*", "i": "*", "code": "`"}
BLOCK_TAGS = {"p", "div"}
HEADING = re.compile(r"^\*\*(Example \d+|Constraints|Follow[- ]up):?\*\*$")
BLANK_RUN = re.compile(r"\n{3,}")
SPACES = re.compile(r"[ \t\r\n]+")
NBSP = "\xa0"


class _Converter(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        # Open inline tags: (tag, marker, index in out where the marker sits).
        self.inline: list[tuple[str, str, int]] = []
        self.lists: list[str] = []
        self.in_pre = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in BLOCK_TAGS:
            self.out.append("\n\n")
            return
        if tag == "pre":
            self.in_pre = True
            self.out.append("\n\n```\n")
            return
        if tag in ("ul", "ol"):
            self.lists.append(tag)
            self.out.append("\n")
            return
        if tag == "li":
            bullet = "1. " if self.lists and self.lists[-1] == "ol" else "* "
            self.out.append("\n" + bullet)
            return
        if tag == "br":
            self.out.append("\n")
            return
        if tag == "img":
            self.out.append(f"![]({dict(attrs).get('src', '')})")
            return
        if tag == "sup":
            self.out.append("^")
            return
        if tag == "sub":
            self.out.append("_")
            return
        self._open_inline(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag in BLOCK_TAGS:
            self.out.append("\n\n")
            return
        if tag == "pre":
            self.in_pre = False
            self.out.append("\n```\n\n")
            return
        if tag in ("ul", "ol"):
            if self.lists:
                self.lists.pop()
            self.out.append("\n\n")
            return
        self._close_inline(tag)

    def handle_data(self, data: str) -> None:
        if self.in_pre:
            # HTML drops the newline right after <pre>.
            if self.out and self.out[-1].endswith("```\n"):
                data = data.removeprefix("\n")
            self.out.append(data)
            return
        self.out.append(SPACES.sub(" ", data.replace(NBSP, " ")))

    def _open_inline(self, tag: str) -> None:
        marker = INLINE_MARKERS.get(tag)
        if marker is None or self.in_pre or self._inside_code():
            return
        self.inline.append((tag, marker, len(self.out)))
        self.out.append(marker)

    def _close_inline(self, tag: str) -> None:
        if not self.inline or self.inline[-1][0] != tag:
            return
        _, marker, start = self.inline.pop()
        inner = "".join(self.out[start + 1 :])
        if inner.strip():
            self.out.append(marker)
            return
        # Blank emphasis such as "<em> </em>" would print as "* *".
        self.out[start] = ""

    def _inside_code(self) -> bool:
        return any(tag == "code" for tag, _, _ in self.inline)


def html_to_markdown(content_html: str) -> str:
    converter = _Converter()
    converter.feed(content_html)
    converter.close()

    lines = []
    for line in "".join(converter.out).split("\n"):
        stripped = line.rstrip()
        heading = HEADING.match(stripped.strip())
        lines.append(f"## {heading.group(1)}" if heading else stripped)

    text = "\n".join(lines)
    text = re.sub(r"^[ \t]+$", "", text, flags=re.MULTILINE)
    return BLANK_RUN.sub("\n\n", text).strip() + "\n"
