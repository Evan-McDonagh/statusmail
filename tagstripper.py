from html.parser import HTMLParser
from io import StringIO

class TagStripper(HTMLParser):
    '''Strips HTML tags from string'''
    def __init__(self) -> None:
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, data: str) -> None:
        self.text.write(data)

    def get_data(self):
        return self.text.getvalue()

def strip_tags(html: str):
    s = TagStripper()
    s.feed(html)
    return s.get_data()

