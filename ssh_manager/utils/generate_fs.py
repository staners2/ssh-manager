from ssh_manager.models.connection import Connection
from ssh_manager.models.file_system import FileSystem
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

    root_folder = Folder(title="/")

    # Default folder for those withou tags 'Folder'
    # deafult_folder = Folder(title="default")
    # root_folder.folders.append(deafult_folder)

    for conn in connections:

        folder_name_items = conn.full_path_folder.split("/") if conn.full_path_folder is not None else []
        current_folder = root_folder
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

    for conn in connections:
        folder_name_items = conn.full_path_folder.split("/")
        current_folder = root_folder
        for folder_name in folder_name_items:
            current_folder = root_folder.get_folder(folder_name)

        print(f"{current_folder.title} = {conn.host}")
        current_folder.connections.append(conn)

    fs.folders = root_folder
    return fs



    # test/folder/A
    # test/folder/B
    # test/connect_1
    # test/connect_2

    # Собрать общий список folders, потом парсить поле folder и на основе этого изменять Folder. Итоговое название папки получать обрезав по последний /