from setuptools import setup

setup(
    name='bloodhound-convert',
    version='1.1.0',
    description='Python based Bloodhound data converter from the legacy pre 4.1 format to 4.1+ format',
    author='Szymon Borecki',
    author_email='self@szymex.pw',
    url="https://github.com/szymex73/bloodhound-convert",
    packages=[
        'bloodhound_convert'
    ],
    license='MIT',
    classifiers=[
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3"
    ],
    entry_points={
        'console_scripts': ['bloodhound-convert=bloodhound_convert:main']
    }
)
