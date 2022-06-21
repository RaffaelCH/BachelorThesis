from setuptools import setup, find_packages


with open('README.txt') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='codediffparser',
    version='0.1.0',
    description='Codediffparser',
    long_description=readme,
    author='Raffael Botschen',
    author_email='',
    platforms=['any'],
    install_requires=['jedi==0.18.1'],
    provides=["codediffparser"],
    license=license,
    packages=find_packages(exclude=['test']),
    entry_points={"console_scripts": ['codediffparser = codediffparser.main:main']}
)