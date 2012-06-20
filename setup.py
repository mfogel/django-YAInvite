from setuptools import setup

setup(
    name='django-YAInvite',
    version='2.0',
    description=(
        'A django invite system where invites allocated to and sent by a '
        'a model of your choosing. (Can be auth.User, but could be your '
        'projects Account model, etc.) Invites are redeemed by a new User '
        'signing up with an valid invite key. Supports default and '
        'invite-specific expiration periods.'
    ),
    author='Mike Fogel',
    author_email='mike@fogel.ca',
    url='https://github.com/mfogel/django-YAInvite',
    license='BSD',
    packages=['yainvite'],
    install_requires=['django', 'South', 'django-appconf'],
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
