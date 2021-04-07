from setuptools import setup
from os import path

# Read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='foronoi',
    packages=[
        'foronoi',
        'foronoi.visualization',
        'foronoi.contrib',
        'foronoi.observers',
        'foronoi.tree',
        'foronoi.nodes',
        "foronoi.graph",
        "foronoi.events",
        "foronoi.tests"
    ],
    version="1.0.3",
    description="Fortune's algorithm for fast Voronoi diagram construction with extras.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jeroen van Hoof',
    author_email='jeroen@jeroenvanhoof.nl',
    url='https://github.com/Yatoom/voronoi',
    download_url='',
    keywords=['voronoi', 'polygon', 'fortune', 'algorithm'],
    classifiers=[],
    install_requires=[
        "numpy", "matplotlib", "graphviz"
    ]
)
