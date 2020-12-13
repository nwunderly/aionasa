
import setuptools


with open("./README.md", "r") as fp:
    long_description = fp.read()


with open('./aionasa/__init__.py', 'r') as fp:
    # FIRST LINE:
    # __version__ = '<version>'
    line = fp.readline()
    version = eval(line[14:])


extras_require = {
    'docs': [
        'sphinx',
        'sphinxcontrib_trio',
    ]
}


setuptools.setup(
    name="aionasa",
    version=version,
    author="nwunderly",
    author_email="",
    description="An async python wrapper for NASA open APIs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    extras_require=extras_require,
    url="https://github.com/nwunderly/aionasa",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
