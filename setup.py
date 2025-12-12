"""
Setup script for building Transcription.app with py2app
"""
from setuptools import setup

APP = ['transcription_app.py']
DATA_FILES = [
    ('templates', ['templates/index.html', 'templates/transcript.html']),
]
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'icon.icns',
    'plist': {
        'CFBundleName': 'Transcription',
        'CFBundleDisplayName': 'Transcription',
        'CFBundleIdentifier': 'com.transcription.menubar',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'LSUIElement': True,  # Menu bar app, no dock icon
        'NSMicrophoneUsageDescription': 'Transcription needs microphone access to record audio.',
        'LSApplicationCategoryType': 'public.app-category.productivity',
    },
    'packages': ['flask', 'watchdog', 'rumps', 'jinja2'],
    'includes': ['sqlite3', 'json', 'hashlib'],
}

setup(
    app=APP,
    name='Transcription',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
