from setuptools import setup, find_packages

setup(
    name='housekeeper',
    version='1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
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