from PyQt5.Qsci import QsciScintilla, QsciLexerCustom
from PyQt5.QtGui import QColor, QFont
from collections import namedtuple
import re

DEFAULT_FONT_SIZE = 10

Token = namedtuple("Token", ["type", "value", "len"])
keywords = ["move", "say", "include", "char", "while", "for", "func"]

IDENTIFIER = r"(?P<ID>[a-zA-Z_][a-zA-Z_0-9]*)"
NUMBER = r"(?P<NUM>\d+)"
OPERATOR = r"(?P<OP>\+|\-|\*|>|<|=)"
COMMENT = r"(?P<COMMENT>//)"
DELIMITER = r"(?P<DELIM>{|}|\(|\))"
WS = r"(?P<WS>\s+)"

master_pat = re.compile(
    "|".join([IDENTIFIER, NUMBER, OPERATOR, COMMENT, DELIMITER, WS])
)


class AddLexer(QsciLexerCustom):
    def __init__(self, editor: QsciScintilla):
        super().__init__(editor)

        self._editor = editor

        self.setDefaultColor(QColor("#ffAAB1C0"))
        self.setDefaultPaper(QColor("#ff161821"))
        self.setDefaultFont(QFont("Fira Code", DEFAULT_FONT_SIZE))

        self.setFont(QFont("Fira Code", DEFAULT_FONT_SIZE), 0)
        self.setFont(QFont("Fira Code", DEFAULT_FONT_SIZE, weight=QFont.Bold), 1)
        self.setFont(QFont("Fira Code", DEFAULT_FONT_SIZE), 2)
        self.setFont(QFont("Fira Code", DEFAULT_FONT_SIZE), 3)
        self.setFont(QFont("Fira Code", DEFAULT_FONT_SIZE, italic=True), 4)

        self.setColor(QColor("#ffAAB1C0"), 0)  # default
        self.setColor(QColor("#ff8b3639"), 1)  # keywords
        self.setColor(QColor("#ff0000bf"), 2)  # delimiters
        self.setColor(QColor("#ffD19A66"), 3)  # numbers
        self.setColor(QColor("#ff5C6370"), 4)  # comments

        # Initialize paper colors per style
        # ----------------------------------
        self.setPaper(QColor("#ff161821"), 0)
        self.setPaper(QColor("#ff161821"), 1)
        self.setPaper(QColor("#ff161821"), 2)
        self.setPaper(QColor("#ff161821"), 3)
        self.setPaper(QColor("#ff161821"), 4)

        # hotspots and clickable text
        # this is not related to the lexer should be in the editor class
        self._editor.SendScintilla(QsciScintilla.SCI_STYLESETHOTSPOT, 1, True)
        self._editor.setHotspotBackgroundColor(QColor("#ff33415D"))
        self._editor.setHotspotUnderline(False)
        self._editor.SCN_HOTSPOTCLICK.connect(self._hotspot_click_handler)

    def _get_clicked_hotspot_name(self, position: int) -> str:
        """
        Position holds the index of the character clicked in the whole text buffer
        """
        text = bytearray(self._editor.text(), "utf-8").decode("utf-8")

        boundaries = [" ", "\n", "\t", "\r"]
        left = right = position

        while left > 0:
            if not text[left] in boundaries:
                left -= 1
            else:
                break

        while right < len(text):
            if not text[right] in boundaries:
                right += 1
            else:
                break

        return text[left:right].strip()

    def _hotspot_click_handler(self, position: int, modifiers) -> None:

        name = self._get_clicked_hotspot_name(position)

        print(f"hotspot {name} clicked at {position:d}")

    def language(self) -> str:
        return "Adventure Drive Script"

    def description(self, style: int) -> str:
        if style == 0:
            return "default"

        elif style == 1:
            return "keywords"

        elif style == 2:
            return "delimiters"

        elif style == 3:
            return "numbers"

        elif style == 4:
            return "comments"

        return ""

    def _generate_tokens(self, pattern, text: str) -> Token:
        scanner = pattern.scanner(text)
        for m in iter(scanner.match, None):
            yield Token(m.lastgroup, m.group(), len(m.group()))

    def styleText(self, start: int, end: int) -> None:
        self.startStyling(start)

        text = bytearray(self._editor.text(), "utf-8")[start:end].decode("utf-8")
        tokens = [tok for tok in self._generate_tokens(master_pat, text)]

        is_comment_line = False
        for tok in tokens:
            if is_comment_line:
                self.setStyling(tok.len, 4)
                if "\n" in tok.value:
                    is_comment_line = False

            elif tok.type == "ID":
                if tok.value in keywords:
                    self.setStyling(tok.len, 1)
                else:
                    self.setStyling(tok.len, 0)

            elif tok.type == "OP":
                self.setStyling(tok.len, 2)

            elif tok.type == "DELIM":
                self.setStyling(tok.len, 2)

            elif tok.type == "NUM":
                self.setStyling(tok.len, 3)

            elif tok.type == "COMMENT":
                self.setStyling(tok.len, 4)
                is_comment_line = True
            else:
                # include whitespace for computing current character position
                self.setStyling(tok.len, 0)
