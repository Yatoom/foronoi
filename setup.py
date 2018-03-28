from setuptools import setup
setup(
  name='voronoi',
  packages=['voronoi', 'voronoi.visualization', 'voronoi.tree', 'voronoi.nodes', "voronoi.graph", "voronoi.events", "voronoi.tests"],
  version='0.9',
  description="Fortune's algorithm for Voronoi diagrams with polygon bounding boxes.",
  author='Jeroen van Hoof',
  author_email='jeroen@jeroenvanhoof.nl',
  url='https://github.com/Yatoom/voronoi',
  download_url='',
  keywords=['voronoi', 'polygon', 'fortune', 'algorithm'],
  classifiers=[],
  install_requires=[
    "numpy", "matplotlib",
  ]
)