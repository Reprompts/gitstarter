from setuptools import setup, find_packages

setup(
    name="gitstarter",
    version="0.1.0",
    author="RePromptsQuest",
    author_email="repromptsquest@gmail.com",
    description="Hybrid Streamlit UI: automates Git-CLI + GitHub API workflows",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/reprompts/gitstarter",
    packages=find_packages(include=["streamgit", "streamgit.*"]),
    py_modules=["app"],
    include_package_data=True,
    install_requires=[
        "streamlit>=1.0",
        "GitPython>=3.1",
        "PyGithub>=1.55"
    ],
    entry_points={
        "console_scripts": [
            "gitstarter=streamgit.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Environment :: Web Environment",
        "Topic :: Software Development :: Version Control",
        "Topic :: Utilities"
    ],
    python_requires=">=3.7",
)
