.. Foronoi documentation master file, created by
   sphinx-quickstart on Sun Apr  4 20:32:46 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Foronoi
=======

Foronoi is a Python implementation of the Fortune's algorithm based on the description of "Computational Geometry:
Algorithms and Applications" by de Berg et al.

This algorithm is a sweep line algorithm that scans top down over the cell points. Every time a new cell point is
scanned, a corresponding parabola (arc) is added. The intersections of this arc with other arcs are so-called
"breakpoints". These breakpoints trace out the borders between two cell points. At the same time when an arc is added,
a check is done to see if this arc will converge with the two arcs on the left or the arcs on the right. If that’s the
case, it will insert a so-called circle-event which causes a new vertex (i.e. a cross-way between edges) to be created
in the middle of the circle.

If you would like to play around with a simple example to get a better understanding, I recommend visiting
|desmos|.

.. |desmos| raw:: html

   <a href="https://www.desmos.com/calculator/ejatebvup4" target="_blank">this toy example</a>


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

   self
   pages/installation
   pages/quickstart
   api
   private
   observers


Indices and tables
++++++++++++++++++

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
