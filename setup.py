import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="acoustic_surveillance_subsystem",
    version="0.0.1",
    author="Robertas Stankevičius",
    author_email="rob.stankevicius@gmail.com",
    description="Passive acoustic localization prototype implementation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/robertasstankevicius/acoustic-surveillance-subsystem",
    project_urls={
        "Bug Tracker": "https://github.com/robertasstankevicius/acoustic-surveillance-subsystem/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires="3.6",
)