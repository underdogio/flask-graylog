from setuptools import setup

setup(
    name='Flask-Graylog',
    version='1.1.1',
    url='https://github.com/underdogio/flask-graylog.git',
    license='MIT',
    author='Brett Langdon',
    author_email='me@brett.is',
    description='Configure Graylog logging handlers and middleware for your Flask app',
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
