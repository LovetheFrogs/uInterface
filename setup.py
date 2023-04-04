from setuptools import setup


setup(
    name="uInterface",
    version="1.0",
    author="LovetheFrogs",
    description="GUI application to use as alternative to UVa judge/uHunt websites",
    python_requires="==3.10",
    install_requires=[
        'customtkinter==5.1.2',
        'matplotlib==3.7.1',
        'uInterface'
    ]
)
