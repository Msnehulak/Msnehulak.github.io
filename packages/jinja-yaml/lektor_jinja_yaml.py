import yaml
from lektor.pluginsystem import Plugin


class JinjaYamlPlugin(Plugin):
    name = "Jinja YAML Filter"

    def on_setup_env(self, **extra):
        def from_yaml(value):
            print("start")
            if not value:
                return []

            return yaml.safe_load(value)

        self.env.jinja_env.filters["from_yaml"] = from_yaml
