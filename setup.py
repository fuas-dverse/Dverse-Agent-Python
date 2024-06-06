import codecs

from setuptools import setup, find_packages


# Read requirements.txt and parse into a list
def read_requirements(file_path):
    try:
        with codecs.open(file_path, 'r', 'utf-8-sig') as f:
            return [line.strip() for line in f.read().splitlines() if line.strip()]
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []


requirements_file_path = 'requirements.txt'
requirements = read_requirements(requirements_file_path)

setup(
    name="dverse_agent_python",
    version="0.1.0",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            # If we have scripts to expose as CLI commands, specify them here
        ],
    },
    author="Fontys-Dverse",
    description="A package for creating an Agent for the DVerse platform.",
    long_description="A package for creating an Agent for the DVerse platform. "
                     "You can see an example at "
                     "https://github.com/fuas-dverse/dverse-agent-python/blob/main/demo_agent.py "
                     "for how you can create your own."
)

# In the dverse-agent-python repository
# Make sure that you do not cd away from the base directory of the repository for the next few steps.
# First, run : pip install . # This will clone the repository and create a package out of it.
# Then execute : python setup.py bdist_wheel # This will create a tar.gz. file of the package.
# You can find the tar file in the dist folder in the same repository as where you are now.
