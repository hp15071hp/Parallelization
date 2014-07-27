from distutils.core import setup

setup(
    name = 'parallelization',
    packages = ['parallelization'],
    version = '0.1',
    author='hp15071hp',
    author_email = 'hp15071hp@gmail.com',
    url = 'https://github.com/hp15071hp/Parallelization',
    description = 'A parallel processing test library based on Robot Framework',
	license='MIT',
    long_description = 
    """
    This is a test library for [Robot framework](https://pypi.python.org/pypi/robotframework) which provides parallel processing keyword function.
    """,
    classifiers  = [
                    'Programming Language :: Python :: 2.7',
                    'License :: OSI Approved :: MIT License',
                    'Operating System :: Microsoft :: Windows :: Windows 7',
                    'Development Status :: 3 - Alpha',
                    'Intended Audience :: Developers',
                    'Topic :: Software Development :: Testing'
                    ]
)