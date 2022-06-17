import os
import sys
from setuptools import setup, find_packages
from kaztau import __version__, __app_name__, __website_url__, __author__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def build_package():
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist bdist_wheel")
    if os.system("twine check dist/*"):
        print("twine check failed. Packages might be outdated.")
        print("Try using `pip install -U twine wheel`.\nExiting.")
        sys.exit()
    print("The version now: ", __version__)


def publish_package():
    build_package()
    os.system("twine upload dist/*")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (__version__, __version__))
    print("  git push --tags")
    sys.exit()


if sys.argv[-1] == 'publish_package':
    publish_package()


if sys.argv[-1] == 'build_package':
    build_package()


setup(
    name=__app_name__,
    version=__version__,
    author=__author__,
    author_email="dev@btech.id",
    description="Python app cli to send message",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=__website_url__,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "typer==0.4.1",
        "pytest==7.1.2",
        "Telethon==1.24.0"
    ],
    python_requires=">=3.6",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'kaztau = kaztau.__main__:main'
        ]
    }
)
