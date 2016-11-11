from setuptools import setup, find_packages
setup(
    name="kartotek",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        'falcon',
        'yoyo-migrations',
        'scrypt'
    ],
    author="Johan Hägg",
    author_email="johan.hagg@shard.se",
    license="MIT",
    entry_points={
        'console_scripts': [
            "api=kartotek:api",
            "load_csv=kartotek:csv",
            "load_cards=kartotek:cards"
        ]
    }
)
