import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="build_subpfam",
    version="0.1.1",
    scripts=['build_subpfam'],
    author="Satria A Kautsar",
    author_email="satriaphd@gmail.com",
    description="Build clade HMMs from a multiple sequence alignment file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/satriaphd/build_subpfam",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.6',
    install_requires=[
        "ete3",
        "six"
    ]
)