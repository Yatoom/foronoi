.. Foronoi documentation master file, created by
   sphinx-quickstart on Sun Apr  4 20:32:46 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Foronoi's documentation!
===================================

Foronoi is a Python implementation of the Fortune's algorithm based on the description of "Computational Geometry:
Algorithms and Applications" by de Berg et al.

This algorithm is a sweep line algorithm that scans top down over the
cell points and traces out the lines via breakpoints in between parabola's (arcs). Once a new point is inserted, a check
is done to see if it will converge with the lines on the left or right. If that's the case, it will insert a so-called
circle-event which causes a new vertex (i.e. a cross-way between edges) to be created in the middle of the circle.

The algorithm keeps track of the status (everything above the line is handled) in a so-called status-structure. This
status-structure is a balanced binary search tree that keeps track of the positions of the arcs (in its leaf nodes) and
the breakpoints (in its internal nodes). This data structure allows for fast look-up times, so that the entire
algorithm can run in `O(n log n)` time.

This implementation includes some additional features to the standard algorithm. For example, this implementation is
able to clip the diagram to a bounding box in different shapes. And it will clean up zero-length edges that occur in
edge-cases where two events happen at the same time so that it is more practical to use.


.. image:: ../voronoi.gif
  :width: 800
  :alt: Voronoi diagram under construction

Table of contents
+++++++++++++++++

.. toctree::
   :maxdepth: 2
   :glob:

   installation
   api
   private


Indices and tables
++++++++++++++++++

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
