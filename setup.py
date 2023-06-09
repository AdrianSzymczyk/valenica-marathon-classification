from pathlib import Path
from setuptools import find_namespace_packages, setup

# Load packages from requirements.txt
BASE_DIR = Path(__file__).parent
with open(Path(BASE_DIR, 'requirements.txt'), 'r') as file:
    required_packages = [ln.strip() for ln in file.readlines()]

# Define package
setup(
    name='valmar',
    version=0.1,
    description='Classify machine learning project',
    author='Adrian Szymczyk',
    python_requires='>=3.8',
    packages=find_namespace_packages(),
    install_requires=[required_packages],
)
