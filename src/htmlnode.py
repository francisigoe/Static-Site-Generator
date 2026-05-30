class HTMLNode:
    def __init__(self, tag: str | None = None, value:str|None=None, children:list|None=None, props:dict|None=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        result = ""
        for atribute in self.props:
            result += f"{atribute}=\"{self.props[atribute]}\" "
        return result[:-1]

    def __repr__(self):
        print(f"tag:{self.tag} value:{self.value} children:{self.children} props:{self.props}")