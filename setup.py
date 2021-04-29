import os
from setuptools import setup
from nvpy import nvpy

setup(
    name = "aquaman",
    version = "0.1",
    author = "Oliver Muir",
    author_email = "ojcmuir@gmail.com",
    description = "Moisture sensor monitoring",
    license = "GPLv3",
    url = "https://github.com/ojcm/aquaman",
    packages=['aquaman'],
    entry_points = {
        'console_scripts' : ['aquaman = aquaman.aquaman:main']
    },
    classifiers=[
        "License :: OSI Approved :: GPLv3 License",
    ],
)
