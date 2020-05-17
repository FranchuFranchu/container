import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="container",
    version="",
    author="FranchuFranchu",
    description="Python package to parse keyword arguments passed into __init__ into an object's attributes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FranchuFranchu/container",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
