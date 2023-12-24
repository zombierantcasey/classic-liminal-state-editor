from setuptools import setup

setup(
    name="liminalstate",
    version="0.1.8",
    author="Pierre MacKay",
    author_email="mail@pierremackay.com",
    install_requires=["mysql-connector-python"],
    entry_points={"console_scripts": ["liminalstate = liminalstate.__main__:main"]},
)
