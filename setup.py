from setuptools import setup, find_packages

setup(
    name = "scrapy-googlelogin",
    version = "0.1.4",
    keywords = ("pip", "datacanvas", "eds", "xiaoh"),
    description = "google login downloader middleware for scrapy",
    long_description = "google login downloader middleware for scrapy",
    license = "MIT Licence",

    url = "https://github.com/geek-dc/scrapy-googlelogin",
    author = "derekchan",
    author_email = "dchan0831@gmail.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['selenium', 'pyotp']
)


