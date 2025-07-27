from setuptools import setup, find_packages

def get_version():
    # Define the version here or read from a file if needed
    return "0.1.0"

setup(
    name="bookstore",
    version=get_version(),
    packages=find_packages(),
    include_package_data=True,
    description="Bookstore Django project",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://example.com/bookstore",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)
