from ssh_manager.models.connection import Connection
from ssh_manager.models.file_system import FileSystem, Node
from ssh_manager.models.folder import Folder


def generate_fs(config: list):
    fs = FileSystem()
    folders = []
    connections = []
    for item in config:
        host = item.get("host")
        folder = item.get("folder", None)
        description = item.get("description", None)
        hostname = item["config"]["hostname"]
        user = item["config"].get("user", None)
        preferred_authentications = item["config"].get("preferredauthentications", None)
        identity_file = item["config"].get("identity_file", None)
        proxy_jump = item["config"].get("proxy_jump", None)

        connection = Connection(host=host, description=description, full_path_folder=folder, hostname=hostname, user=user,
                                preferred_authentications=preferred_authentications, identity_file=identity_file,
                                proxy_jump=proxy_jump)
        connections.append(connection)

    head_folder = Folder(title="/")


    for conn in connections:
        folder_name_items = conn.full_path_folder.split("/")
        current_folder = head_folder
        for folder_name in folder_name_items:
            if not [folder for folder in current_folder.folders if folder_name in folder.title]:
                f = Folder(title=folder_name)
                current_folder.folders.append(f)
                current_folder = f
                continue
            else:
                f = [folder for folder in current_folder.folders if folder_name in folder.title][0]
                current_folder = f
                continue
        print(folder_name_items)
        if folder_name_items is None:
            print("sdfsd")
            # Default folder for those withou tags 'Folder'
            f = Folder(title="default")
            current_folder.folders.append(f)
            continue

    print(head_folder)

    def show(folder, indent=0):
        print(" " * indent + "- " + folder.title)
        for child in folder.folders:
            show(child, indent + 2)

    show(head_folder)

#             test
#          /   |   \
#         a  conn1  b
#        /\
#    conn  conn2

def add_item(header_folder, path):
    folder_name_items = path.split("/")
    current = header_folder
    for part in folder_name_items:
        if part not in current.title:
            current.folders = Folder("")

    # parts = path.split("/")
    # current = root
    # for part in parts:
    #     if part not in current:
    #         current[part] = {}
    #     current = current[part]

    # test/folder/A
    # test/folder/B
    # test/connect_1
    # test/connect_2

    # Собрать общий список folders, потом парсить поле folder и на основе этого изменять Folder. Итоговое название папки получать обрезав по последний /