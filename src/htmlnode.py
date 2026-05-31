class HTMLNode:
    def __init__(self, tag: str|None =None, value: str|None =None, children: list|None =None, props: dict|None =None):
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

class LeafNode(HTMLNode):
    def __init__(self, value: str|None, tag: str|None, props: dict|None =None):
        super().__init__(value,tag,props = props)
        
    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return self.value
        if self.props:
            props = ""
            for value in self.props:
                props = props.join(f"{value}=\"{self.props[value]}\" ")
            return f"<{self.tag} {props[:-1]}>{self.value}</{self.tag}>" 
        return f"<{self.tag}>{self.value}</{self.tag}>" 

    def __repr__(self):
        print(f"tag:{self.tag} value:{self.value} props:{self.props}") 