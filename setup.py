from setuptools import setup

setup(
    name='playmusic',
    packages=['playmusic','users'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
