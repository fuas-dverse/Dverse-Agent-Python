from setuptools import setup, find_packages

setup(
    name="agentDVerse",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "python-slugify",
        # Add other dependencies here
    ],
    entry_points={
        "console_scripts": [
            # If we have scripts to expose as CLI commands, specify them here
        ],
    },
    author="Fontys-Dverse",
    description="A package for creating an Agent for the DVerse platform."
)

#in the dverse-agent-python
# first, run : pip install .
# then execute : python startup.py sdist to create a tar.gz. file of the package