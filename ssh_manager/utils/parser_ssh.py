import re
import shlex


class ParserSSH():

    SETTINGS_REGEX = re.compile(r"(\w+)(?:\s*=\s*|\s+)(.+)")

    def __init__(self, path_to_config="~/.ssh/config"):
        self._config = []
        self.path_to_config = path_to_config

    def parse(self) -> list:
        with open(self.path_to_config) as f:
            self.__parse_config(f)

        return self._config[1:]

    def __parse_config(self, file_obj):
        context = {"config": {}}
        create_new_context = True
        for line in file_obj:
            line = line.strip()
            # Skip blanks, comments
            if not line:
                create_new_context = True
                continue

            # Skip
            if line.startswith("#") and not line.startswith("# Description: ") and not line.startswith("# Folder: "):
                continue

            if line.startswith("# Folder: "):
                if create_new_context:
                    self._config.append(context)
                    context = {"config": {}}
                create_new_context = False

                folder = None
                if line.startswith("# Folder: "):
                    folder = line.replace("# Folder: ", "")
                context["folder"] = folder
                context["description"] = None

            if line.startswith("# Description: "):
                if line.startswith("# Description: "):
                    description = line.replace("# Description: ", "")
                    context["description"] = description

            if line.startswith("#"):
                continue

            # Parse line into key, value
            match = re.match(self.SETTINGS_REGEX, line)
            if not match and not line.startswith("#"):
                raise ConfigParseError("Unparsable line {}".format(line))

            key = match.group(1).lower()
            value = match.group(2)

            # Host keyword triggers switch to new block/context
            if key in ("host", "match"):
                if key == "host":
                    context["host"] = self._get_hosts(value)
                else:
                    context["matches"] = self._get_matches(value)
            else:
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]

                if key in ["identityfile", "localforward", "remoteforward"]:
                    if key in context["config"]:
                        context["config"][key].append(value)
                    else:
                        context["config"][key] = [value]
                elif key not in context["config"]:
                    context["config"][key] = value
        self._config.append(context)

    def _get_hosts(self, host):
        """
        Return a list of host_names from host value.
        """
        try:
            return shlex.split(host)
        except ValueError:
            raise ConfigParseError("Unparsable host {}".format(host))

    def _get_matches(self, match):
        """
        Parse a specific Match config line into a list-of-dicts for its values.

        Performs some parse-time validation as well.
        """
        matches = []
        tokens = shlex.split(match)
        while tokens:
            match = {"type": None, "param": None, "negate": False}
            type_ = tokens.pop(0)
            # Handle per-keyword negation
            if type_.startswith("!"):
                match["negate"] = True
                type_ = type_[1:]
            match["type"] = type_
            # all/canonical have no params (everything else does)
            if type_ in ("all", "canonical", "final"):
                matches.append(match)
                continue
            if not tokens:
                raise ConfigParseError(
                    "Missing parameter to Match '{}' keyword".format(type_)
                )
            match["param"] = tokens.pop(0)
            matches.append(match)
        # Perform some (easier to do now than in the middle) validation that is
        # better handled here than at lookup time.
        keywords = [x["type"] for x in matches]
        if "all" in keywords:
            allowable = ("all", "canonical")
            ok, bad = (
                list(filter(lambda x: x in allowable, keywords)),
                list(filter(lambda x: x not in allowable, keywords)),
            )
            err = None
            if any(bad):
                err = "Match does not allow 'all' mixed with anything but 'canonical'"  # noqa
            elif "canonical" in ok and ok.index("canonical") > ok.index("all"):
                err = "Match does not allow 'all' before 'canonical'"
            if err is not None:
                raise ConfigParseError(err)
        return matches



class ConfigParseError(Exception):
    pass