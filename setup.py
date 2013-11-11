from setuptools import setup

setup(
    name='collektr-testserver',
    version='0.1',
    packages=['testserver'],
    entry_points={
        'console_scripts': [
            'collektr-test = testserver.application:main',
        ]
    },
    install_requires=['bottle'],
    url='https://github.com/collektr/testserver',
    license='MIT',
    author='Sebastian Rahlf',
    author_email='basti@redtoad.de',
    description='Stand-alone test server with dummy data for the Collektr API.'
)
