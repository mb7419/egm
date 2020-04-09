#https://towardsdatascience.com/build-your-first-open-source-python-project-53471c9942a7
from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="egm",
    version="0.0.1",
    author="Mohit Bhatnagar",
    author_email="mohit@uplytics.com",
    description="A python package for plotting Evidence Gap Maps using Plotly",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://https://github.com/mb7419/egm/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
