from setuptools import setup

setup(
    name="weather-cli",
    version="0.2.0",
    py_modules=["weather"],
    install_requires=["httpx", "rich"],
    entry_points={"console_scripts": ["weather=weather:main"]},
)