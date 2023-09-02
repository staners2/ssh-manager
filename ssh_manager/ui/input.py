from textual.widgets import Input


class InputField(Input):
    def __init__(self, placeholder = ""):
        self.placeholder = placeholder
        super().__init__()

    # def on_click(self) -> None:
    #     pass
        # The post_message method sends an event to be handled in the DOM
        # self.post_message(self.Selected(self.color))

    # def render(self) -> str:
        # return str(self.color)

    # def on_mount(self) -> None:
    #     pass
        # self.styles.margin = (1, 2)
        # self.styles.content_align = ("center", "middle")
        # self.styles.background = Color.parse("#ffffff33")
        # self.styles.border = ("tall", self.color)
