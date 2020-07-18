
import setuptools

with open("./README.md", "r") as fh:
    long_description = fh.read()

with open('./aionasa/__init__.py', 'r') as f:
    # FIRST LINE:
    # __version__ = '<version>'
    line = f.readline()
    version = eval(line[14:])

setuptools.setup(
    name="aionasa",
    version=version,
    author="nwunderly",
    author_email="",
    description="An async python wrapper for NASA open APIs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nwunderly/aio-nasa",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
