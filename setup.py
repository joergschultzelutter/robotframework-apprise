#!/usr/bin/env/python

from setuptools import setup, find_packages
import os

if __name__ == "__main__":
	with open("README.md", "r") as fh:
		long_description = fh.read()
		
	VERSION = os.getenv("GITHUB_PROGRAM_VERSION")
	if not VERSION:
		raise ValueError("Did not receive version info from GitHub")
		
	setup(
		name="robotframework-apprise",
		version=VERSION,
		description="Robot Framework keywords for the 'Apprise' push messaging library",
		long_description=long_description,
		long_description_content_type="text/markdown",
		author="Joerg Schultze-Lutter",
		author_email="joerg.schultze.lutter@gmail.com",
		url="https://github.com/joergschultzelutter/robotframework-apprise",
		packages=find_packages(),
                include_package_data=True,
		classifiers=[
			"Intended Audience :: Developers",
			"Programming Language :: Python :: 3",
			"Natural Language :: English",
			"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
			"Operating System :: OS Independent",
			"Development Status :: 4 - Beta",
			"Framework :: Robot Framework",
			"Framework :: Robot Framework :: Library",
			"Topic :: Software Development",
			"Topic :: Software Development :: Testing",
			"Topic :: Software Development :: Quality Assurance",
		],
		license="GNU General Public License v3 (GPLv3)",
		install_requires=["robotframework>=4.0.1", "apprise>=0.9.6"],
		keywords=["Notifications", "Notification Service", "Push Notifications", "Notifier", "Alerts", "Robot Framework"]
	)
