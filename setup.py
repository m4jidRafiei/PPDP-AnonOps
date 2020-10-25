
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ppdp_anonops",
    version="0.0.1",
    author="Alexander 'DevSchnitzel' Schnitzler",
    author_email="DevSchnitzel@outlook.com",
    description="A package providing multiple anonymization methods for PM4PY's XES-event logs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheDevSchnitzel/PPDP-AnonOps",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3 License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    test_suite='nose.collector',
    tests_require=['nose'],
)