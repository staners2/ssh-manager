from dataclasses import dataclass, field

from ssh_manager.models.connection import Connection
from ssh_manager.models.folder import Folder


@dataclass
class FileSystem:
    folders: [Folder] = field(default_factory=lambda: [])

    def find_elements(self, pattern: str) -> [Folder]:
        folders = []

        for folder in self.folders:
            find_folder = folder.find_element_in_folder(pattern)
            folders.append(find_folder)

        return [item for item in folders if item != None]
