"""Set up for the Tahoe SCORM Customizations package."""

from pathlib import Path
from setuptools import setup


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='tahoe-scorm',
    version='0.1.3',
    description='Tahoe SCORM Customizations package.',
    packages=[
        'tahoe_scorm',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)
