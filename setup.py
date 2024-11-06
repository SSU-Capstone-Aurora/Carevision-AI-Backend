import setuptools

setuptools.setup(
    name="carevision-ai",
    version="0.0.1",
    author="aurora",
    description="carevision ai lib",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)