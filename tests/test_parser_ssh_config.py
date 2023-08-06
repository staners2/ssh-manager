from ssh_manager.utils.parser_ssh import ParserSSH


def test_parse_ssh_config():
    parser = ParserSSH(path_to_config="tests/mock_data/ssh_config")
    config = parser.parse()

    item1 = config[1]
    item2 = config[2]

    assert item1["config"]["hostname"] == "192.168.250.108"
    assert item1["folder"] == "test/a"
    assert item1["description"] == None
    assert item1["host"][0] == "runner-01"

    assert item2["config"]["hostname"] == "192.168.249.125"
    assert item2["folder"] == "test/b"
    assert item2["description"] == "For connect to home"
    assert item2["host"][0] == "runner-02"
    assert item2["host"][1] == "runner-2"
