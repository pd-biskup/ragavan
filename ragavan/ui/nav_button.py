from dash import dcc, html


class NavButton(html.Li):
    className = "navbutton"

    def __init__(self, href, label):
        super().__init__()
        link = dcc.Link(children=[label], href=href)
        self.children = [link]
