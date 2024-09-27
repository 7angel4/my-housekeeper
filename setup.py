from setuptools import setup

setup(
    name='my-housekeeper',  
    version='1.0',          
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
