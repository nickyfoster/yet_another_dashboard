from setuptools import find_packages

from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install


class PostDevelopCommand(develop):
    """Post-installation for development mode."""

    def run(self):
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        develop.run(self)


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        install.run(self)


setup(
    name='dash_core',
    url='https://github.com/nickyfoster/yet_another_dashboard',
    description='Yet Another Dashboard Backend Service',
    keywords='python dashboard backend',
    packages=find_packages(exclude=['test', 'test.*']),
    package_dir={'dash_core': 'dash_core'},
    install_requires=[
        "aniso8601==9.0.1",
        "beautifulsoup4==4.11.1",
        "certifi==2022.9.24",
        "charset-normalizer==2.1.1",
        "click==8.1.3",
        "Flask==2.2.2",
        "Flask-Cors==3.0.10",
        "graphene==3.1.1",
        "graphql-core==3.2.3",
        "graphql-relay==3.2.0",
        "idna==3.4",
        "importlib-metadata==5.0.0",
        "itsdangerous==2.1.2",
        "Jinja2==3.1.2",
        "MarkupSafe==2.1.1",
        "requests==2.28.1",
        "six==1.16.0",
        "soupsieve==2.3.2.post1",
        "Unidecode==1.3.6",
        "urllib3==1.26.12",
        "Werkzeug==2.2.2",
        "zipp==3.10.0"
    ],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    }
)
