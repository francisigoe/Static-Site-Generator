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
    def __init__(self, tag: str|None, value: str|None, props: dict|None =None):
        super().__init__(tag,value,props = props)
        
    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return self.value
        if self.props:
            props = self.props_to_html()
            return f"<{self.tag} {props}>{self.value}</{self.tag}>" 
        return f"<{self.tag}>{self.value}</{self.tag}>" 

    def __repr__(self):
        print(f"tag:{self.tag} value:{self.value} props:{self.props}") 

class ParentNode(HTMLNode):
    def __init__(self, tag: str|None , children: list|None , props: dict|None =None):
        super().__init__(tag,None,children,props = props)

    def to_html(self):
        if not self.tag:
            raise ValueError("parent node missing a tag")
        if not self.children:
            raise ValueError("parent node missing children")
        child_html = ""
        for child in self.children:
            child_html += child.to_html()
        if self.props:
            props = self.props_to_html()
            return (f"<{self.tag} {props}>{child_html}</{self.tag}>")
        return(f"<{self.tag}>{child_html}</{self.tag}>") 

