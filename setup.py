from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [
        line.strip() 
        for line in fh 
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="ibt-cognitive-decision-layer",
    version="1.0.1",
    author="Ibtesham Akhtar",
    author_email="ibtesham.akhtar@example.com",
    description="Production-grade cognitive decision engine for AI systems with emotion awareness and reasoning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ibtesham42/ibt-cognitive-decision-layer",
    project_urls={
        "Bug Tracker": "https://github.com/Ibtesham42/ibt-cognitive-decision-layer/issues",
        "Source Code": "https://github.com/Ibtesham42/ibt-cognitive-decision-layer",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=["tests", "tests.*", "venv", "venv.*", "logs"]),
    python_requires=">=3.8",
    install_requires=requirements,
    include_package_data=True,
    zip_safe=False,
)