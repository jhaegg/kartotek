from setuptools import setup, find_packages
setup(
    name="MTGAPI",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        'falcon',
        'yoyo-migrations'
    ],
    author="Johan Hägg",
    author_email="johan.hagg@shard.se",
    license="MIT",
    entry_points={
        'console_scripts': ["api=mtgapi:api", "load_csv=mtgapi:csv"]
    }
)
