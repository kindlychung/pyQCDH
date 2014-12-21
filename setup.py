from setuptools import setup

setup(
    name = "pyQCDH",
    packages = ["pyQCDH"],
    version = "0.0.1",
    # entry_points = {"console_scripts": ['gtranslate = translator.shellscript:main']},
    install_requires = ["pandas", "statsmodels"],
    description = "QCDH",
    author = "Kaiyin Zhong",
    author_email = "kindlychung@gmail.com",
    url = "https://github.com/kindlychung/pyQCDH",
    keywords = ["statistics"]
    )

