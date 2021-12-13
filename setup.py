
import setuptools


setuptools.setup(
    name='T_Lock',
    version='0.0.1',
    author='DAF201',
    description='lock your file with time',
    url='https://github.com/DAF201/T_Lock',
    packages=['T_Lock'],
    package_data={
        '':'default_image.jpg',
        '':'customize.json'
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=[],
    python_requires='>=3.6',
)
