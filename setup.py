#!/usr/bin/env/python

from setuptools import setup, find_packages
import os

if __name__ == "__main__":

	VERSION = os.getenv("GITHUB_PROGRAM_VERSION")

	with open("README.md", "r") as fh:
		long_description = fh.read()
		
	if not VERSION:
		raise ValueError("Did not receive version info from GitHub")
		
	setup(
		name="robotframework-apprise",
		version=VERSION,
		description="Robot Framework keywords for Apprise push messaging Python library, https://github.com/caronc/apprise",
		long_description=long_description,
		long_description_content_type="text/markdown",
		author="Joerg Schultze-Lutter",
		author_email="joerg.schultze.lutter@gmail.com",
		url="https://github.com/joergschultzelutter/robotframework-apprise",
		packages=find_packages(),
		classifiers=[
			"Intended Audience :: Developers",
			"Programming Language :: Python",
			"Programming Language :: Python :: 3",
			"Topic :: Software Development",
			"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
			"Operating System :: OS Independent",
			"Development Status :: 4 - Beta",
			"Framework :: Robot Framework",
			"Topic :: Software Development :: Testing",
		],
		license="GNU General Public License v3 (GPLv3)",
		install_requires=["robotframework>=4.1.3", "apprise>=0.9.6"],
		keywords=["Notifications", "Notification Service", "Push Notifications", "Notifier", "Alerts", "Robot Framework"]
	)
