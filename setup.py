"""
py2app build script for MyApplication

Usage:
    python setup.py py2app
    """
from setuptools import setup
from glob import glob

OPTIONS = {'argv_emulation': True, 'iconfile': 'icon.icns', 'plist':{'CFBundleShortVersionString':'0.1.0',}}
DATA_FILES = [('', ['ball']),('',['obstacle']), ('', ['character']), ('', glob('*.*'))]
setup(
    app=['menu.py'],
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
