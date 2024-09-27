from setuptools import setup, find_packages

setup(
    name='my-housekeeper',  
    version='1.0',          
    packages=find_packages(where='src'),  
    package_dir={'': 'src'},              
    entry_points={
        'console_scripts': [
            'housekeeper=housekeeper:main', 
        ],
    },
    install_requires=[
        'tabulate',                      
        'google-generativeai',
    ],
    classifiers=[                     
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',          
)
