from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(
    name='Flask-Graylog',
    version='1.1.2',
    url='https://github.com/underdogio/flask-graylog.git',
    license='MIT',
    author='Brett Langdon',
    author_email='me@brett.is',
    description='Configure Graylog logging handlers and middleware for your Flask app',
    long_description=long_description,
    py_modules=['flask_graylog'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=['Flask', 'graypy'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
