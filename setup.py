from setuptools import setup, find_packages

setup(
    name="datahub",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # Add dependencies from requirements.txt if needed
    ],
)