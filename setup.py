"""
Packaging script for PyPI.
"""
import setuptools

from bedspread import front_end
front_end._refresh_grammar()

exec(open('python/bedspread/version.py').read())

setuptools.setup(
	name='bedspread',
	author='Ian Kjos',
	author_email='kjosib@gmail.com',
	version=__version__,
	packages=['bedspread', ],
	package_dir = {'': 'python'},
	package_data={
		'bedspread': ['grammar.automaton',],
	},
	license='MIT',
	description='Bed Spread: an Expression-Oriented Code-in-Database System',
	long_description=open('README.md').read(),
	long_description_content_type="text/markdown",
	url="https://github.com/kjosib/mistake",
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Development Status :: 2 - Pre-Alpha",
		"Intended Audience :: Developers",
		"Intended Audience :: Education",
		"Topic :: Software Development :: Interpreters",
		"Topic :: Software Development :: Libraries",
		"Topic :: Education",
		"Environment :: Console",
    ],
	python_requires='>=3.7',
	install_requires=[
		'booze-tools>=0.5.1',
	]
)