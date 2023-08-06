from dataclasses import dataclass


@dataclass
class Connection:
    # Host
    host: [str]
    # Hostname
    hostname: str
    # User
    user: str
    # IdentityFile
    identity_file: str = None
    # Preferredauthentications
    preferred_authentications: str = None
    # ProxyJump
    proxy_jump: str = None

    # custom options
    full_path_folder: str = ""
    description: str = ""