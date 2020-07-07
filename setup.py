
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aio-nasa",
    version="0.0.1",
    author="nwunderly",
    author_email="",
    description="An async python wrapper for NASA APIs.",
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
