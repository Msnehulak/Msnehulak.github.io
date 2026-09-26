from setuptools import setup

setup(
    name="lektor-jinja-yaml",
    version="0.1",
    py_modules=["lektor_jinja_yaml"],
    entry_points={
        "lektor.plugins": [
            "jinja-yaml = lektor_jinja_yaml:JinjaYamlPlugin",
        ]
    },
)
