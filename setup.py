"""保留 setup.py 以兼容旧版 pip 和 editable install。"""

from setuptools import find_packages, setup

setup(
    name="hutool-python",
    version="1.1.2",
    description="Python port of Java Hutool utility library",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Hutool-Python",
    url="https://github.com/wgp520/hutool-python",
    project_urls={
        "Documentation": "https://wgp520.github.io/hutool-python",
        "Repository": "https://github.com/wgp520/hutool-python",
        "Issues": "https://github.com/wgp520/hutool-python/issues",
    },
    license="MulanPSL-2.0",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(exclude=["tests*", "docs*"]),
    install_requires=[
        "pendulum>=3.0",
        "httpx>=0.27",
        "cryptography>=42.0",
        "qrcode[pil]>=7.0",
        "Pillow>=10.0",
        "pypinyin>=0.50",
        "emoji>=2.0",
        "jinja2>=3.0",
        "pyjwt>=2.8",
        "pyyaml>=6.0",
        "watchdog>=4.0",
        "sortedcontainers>=2.0",
        "pytz>=2023.3",
        "bcrypt>=4.0",
    ],
    extras_require={
        "dev": ["pytest>=8.0", "ruff>=0.4.0"],
    },
)
