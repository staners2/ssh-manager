from ssh_manager.utils.generate_fs import generate_fs
from ssh_manager.utils.parser_ssh import ParserSSH


def main():
    parser = ParserSSH(path_to_config="tests/mock_data/more_ssh")
    config = parser.parse()
    print(config)
    return generate_fs(config)
