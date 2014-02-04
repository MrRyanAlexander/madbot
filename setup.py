from setuptools import setup, find_packages

setup(
    name         = 'mad_bot',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = mad_bot.settings']},
    scripts = ['bin/testargs.py']
)