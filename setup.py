from setuptools import setup

setup(
    name='django-YAInvite',
    version=__import__('yainvite').__version__,
    description='Yet Another Invite system for Django',
    long_description=open('README.rst').read(),
    author='Mike Fogel',
    author_email='mike@fogel.ca',
    url='https://github.com/mfogel/django-YAInvite',
    license='BSD',
    packages=['yainvite'],
    install_requires=[
        'django', 'South', 'django-appconf', 'django-extra-views',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)
