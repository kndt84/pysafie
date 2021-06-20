import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysafie",  # Replace with your own username
    version="0.0.1",
    install_requires=[
        "requests",
    ],
    author="kndt84",
    author_email="takashi.kaneda@gmail.com",
    description="Safie API client library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kndt84/pysafie",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
