from distutils.core import setup
setup(
    name='salem_parser',
    packages=['salem_parser'],
    version='v1.1.4-beta',
    license='MIT',
    description='A module used to parse reports from the Town of Salem Trial System into a format that can be easily used for data analysis.',
    author='Shortty10',
    url='https://github.com/Shortty10/salem_parser',
    download_url='https://github.com/Shortty10/salem_parser/archive/v1.1.4-beta.tar.gz',
    keywords=['Town', 'of', 'Salem'],
    install_requires=[
        'requests',
        'lxml',
        'beautifulsoup4',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
