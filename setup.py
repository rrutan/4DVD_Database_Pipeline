from setuptools import setup, find_packages

setup(
    name="4DVD Database Pipeline",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'requests',
        'mysql-connector-python',
        'xarray'
    ],
    author="Riley Rutan",
    author_email="riley.rutan@gmail.com",
    description="A python package to update the 4DVD Database.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/", ## add this later
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license="MIT"
)
