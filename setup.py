from setuptools import setup, find_packages
from django_admin_shell import __version__ as version


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='django-admin-shell',
    version=version,
    description='',
    url='https://github.com/djk2/django-admin-shell',
    author='Grzegorz Tężycki',
    author_email='grzegorz.tezycki@gmail.com',
    long_description=(
        """Django application can execute python code in your """
        """project's environment on django admin site."""
    ),
    license='MIT',
    packages=find_packages(exclude=['docs']),
    package_data={'django_admin_shell': [
        'templates/django_admin_shell/*',
        'static/django_admin_shell/js/*',
        'static/django_admin_shell/js/linedtextarea/*',
        'static/django_admin_shell/fonts/*',
        'static/django_admin_shell/css/*',
    ]},
    tests_require=['Django', 'ruff'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Django>=4.2'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Framework :: Django :: 5.1',
        'Framework :: Django :: 5.2',
        'Framework :: Django :: 6.0',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Topic :: Utilities',
    ],
    keywords='django admin shell console terminal',
)
