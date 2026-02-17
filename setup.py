from setuptools import setup

setup(
    name="wit",
    version="1.0",
    py_modules=["cli", "repository", "utils"],
    install_requires=["click"],
    entry_points={
        "console_scripts": [
            "wit=cli:cli",
        ],
    },
)

