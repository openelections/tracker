from setuptools import setup, find_packages

setup(
    name='tracker',
    version='0.0.1',
    description="Progress tracker Library/app for tracking OpenElections metadata",
    long_description="Library/app for tracking OpenElections metadata",
    author=["Serdar Tumgoren", "Derek Willis"],
    author_email='zstumgoren@gmail.com',
    url='https://github.com/openelections/tracker',
    license="ISCL",
    keywords='openelections',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Environment :: Console',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=['pygithub'],
    entry_points={
        'console_scripts': [
            'openelex-tracker=tracker.cli:main',
        ],
    },
    test_suite='tests',
    tests_require=['pytest', 'pytest-mock'],
    zip_safe=False,
)
