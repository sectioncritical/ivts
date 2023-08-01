from setuptools import setup

setup(
    name = 'ivts',
    version = '0.1',
    description =  "Library and utility for communicating with IVT-S current sensor over CAN bus.",
    packages = ["ivts"],
    install_requires = ['python-can'],
    entry_points = {
        "console_scripts": [
            "monitor=ivts.init:cli"]
    }
)
