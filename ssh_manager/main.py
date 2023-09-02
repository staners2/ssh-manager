from textual import on

from ssh_manager.utils.generate_fs import generate_fs
from ssh_manager.utils.parser_ssh import ParserSSH
from textual.app import App, ComposeResult
from textual.widgets import Button, Header, Input, Label, Select, Static, Tree
from textual.widgets import ListView

class MyApp(App[str]):
    CSS_PATH = "ui/css/box.css"
    TITLE = "A Question App"
    SUB_TITLE = "The most important question"

    def __init__(self, options):
        super().__init__()
        self.options = options

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("One", classes="box")
        yield Static("Two", classes="box")
        yield Input(placeholder="Input ...")
        yield Button("Clean", id="clean")

        tree: Tree[dict] = Tree("SSH CONNECTIONS")
        tree.root.expand()
        root = tree.root.add("/", expand=True)
        self.generate_tree(self.options.folders, root)
        yield tree

    def generate_tree(self, head_folder, tree):
        for folder in head_folder.folders:
            tree = tree.add(f"{folder.title}", expand=True)
            self.generate_tree(folder, tree)
        for item in head_folder.connections:
            tree.add_leaf(', '.join(item.host))

    # def on_button_pressed(self) -> None:
    #     """Clear the text input."""
    #     input = self.query_one(Input)
    #     with input.prevent(Input.Changed):
    #         input.value = ""
    #
    # def on_input_changed(self) -> None:
    #     """Called as the user types."""
    #     self.bell()


def main():
    parser = ParserSSH(path_to_config="tests/mock_data/more_ssh")
    config = parser.parse()
    file_system = generate_fs(config)
    app = MyApp(file_system)
    reply = app.run()
    print(reply)

    return generate_fs(config)
