from setuptools import setup

setup(
    name='housekeeper',
    version='1.0',
    py_modules=['housekeeper'],
    install_requires=[
        'tabulate',            
        'google-generativeai',  
    ],
    entry_points={
        'console_scripts': [
            'housekeeper=src.housekeeper:main',
        ],
    },
)
