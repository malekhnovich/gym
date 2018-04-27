from setuptools import setup

setup(
    name='gym',
    packages=['gym'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)