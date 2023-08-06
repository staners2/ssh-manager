from ssh_manager import __version__


def test_version():
    """
    Test for app version
    """
    assert __version__ == "0.1.0"
