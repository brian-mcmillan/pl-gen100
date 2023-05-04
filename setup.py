from setuptools import setup

setup(
    name='bb100',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'bb100=bb100:run'
        ]
    }
)
