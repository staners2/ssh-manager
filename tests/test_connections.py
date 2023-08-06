from ssh_manager.models.connection import Connection
from ssh_manager.models.file_system import FileSystem
from ssh_manager.models.folder import Folder


def test_find_connection_success():

    connections = [
        Connection(host="host", hostname="hostname", user="user")
    ]
    folder_1 = Folder(title="folder_1", connections=connections)
    folder_2 = Folder(title="folder_2", connections=connections, folders=[Folder(title="folder_3", connections=connections)])
    fs = FileSystem(folders=[folder_1, folder_2])
    pattern = "folder_3"

    result = [fs.find_elements(pattern)]
    print(result)

    result_2 = [fs.find_elements("")]
    print(f"res_2 \n{result_2}")

    count_folders = len(result)

    assert count_folders > 0

# def test_find_connection_failed():
#
#     connections = [
#         Connection(host="host", hostname="hostname", user="user")
#     ]
#     folder = Folder(title="folder", connections=connections)
#     fs = FileSystem(folders=[folder])
#     pattern = "folder"
#
#     assert len([folder.find_item_recursive(pattern) for folder in fs.folders]) == 0