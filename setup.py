from setuptools import setup

setup(
    author="Tomek Joostens",
    author_email='joostenstomek@gmail.com',
    description="Program to ease picture development flow ",
    entry_points={
        'console_scripts': [
            'gurushots=cli:main',
            'gs=cli:main',
        ],
    }
)