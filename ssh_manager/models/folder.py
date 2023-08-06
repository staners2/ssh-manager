from copy import deepcopy
from dataclasses import dataclass, field
from typing import List

from ssh_manager.models.connection import Connection


@dataclass
class Folder:
    title: str
    connections: List[Connection] = field(default_factory=lambda: [])
    folders: [] = field(default_factory=lambda: [])

    def find_element_in_folder(self, pattern: str) -> object | None:
        found_recursive_item_in_folders = False

        __folders__ = []
        copy_folder = deepcopy(self)

        for folder in copy_folder.folders:
            if len(folder.folders) > 0:
                print(f"Найдены folders: {folder.title}")
                folder.find_in_folder(pattern)
            if pattern in folder.title:
                __folders__.append(folder)
                found_recursive_item_in_folders = True
            else:
                found_recursive_item_in_folders = copy_folder.__find_connection_in_folder__(folder, pattern)

        found_item_in_folder = copy_folder.__find_connection_in_folder__(copy_folder, pattern)

        copy_folder.folders = __folders__

        if found_recursive_item_in_folders or found_item_in_folder:
            return copy_folder
        else:
            return None

    def __find_connection_in_folder__(self, folder, pattern: str) -> bool:
        found_item = False
        __connections__ = []
        for conn in folder.connections:
            if pattern in conn.host or pattern in conn.hostname or pattern in conn.user:
                __connections__.append(deepcopy(conn))
                found_item = True

        folder.connections = __connections__

        return found_item

    def get_title(self):
        return self.title.split("/")[-1]