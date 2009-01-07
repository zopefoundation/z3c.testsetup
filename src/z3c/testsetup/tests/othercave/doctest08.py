"""
Doctests in a Python module
===========================

We can place doctests also in Python modules.

:doctest:

Here the Cave class is defined::

  >>> from z3c.testsetup.tests.othercave.doctest08 import Cave
  >>> Cave
  <class 'z3c.testsetup...doctest08.Cave'>

"""
class Cave(object):
    """A Cave.

    A cave has a number::

      >>> hasattr(Cave, 'number')
      True
    
    """
    number = None

    def __init__(self, number):
        """Create a Cave.

        We have to give a number if we create a cave::

          >>> c = Cave(12)
          >>> c.number
          12
          
        """
        self.number = number
