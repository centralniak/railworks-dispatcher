Railworks Dispatcher
====================

Creates a work order by choosing a random scenario from your Railworks folder. Here is
what your work order can look like:

.. image:: docs/_static/example_work_order.png

Don't worry! It is created in vector, so it prints nice.

The scenario briefing and description is taken from
`Armstrong Powerhouse's AP37 Scenario pack <http://www.armstrongpowerhouse.com/index.php?route=product/product&path=29_81&product_id=139>`_.


Setup
-----

* Install Python 2.7 (this dependency will be removed soon)

* Place in the same folder as your ``railworks.exe``.


Usage
-----

* Unpack using 7Zip or RW-Tools all the routes and scenarios you want to be scanned.
  Since 2014 DTG have started packing some assets in loseless ZIP files with .ap extension
  which Dispatcher is not able to look through at the moment for performance reasons.
  This has been described in detail by Mike, the author of RW-Tools, in his
  `*.AP file tutorial <http://www.rstools.info/RW_Tools_and_APfiles.pdf>`_.

* Run from console using ``python dispatcher.py`` -
  a ``WorkOrder.html`` file will be created and opened in your default browser
  containing a description of your duties.


Acknowledgements
----------------

* The created work order uses dot matrix fonts created by
  `Svein Kåre Gunnarson <http://dionaea.com/information/fonts.php>`_.

* The logos of Train Operating Companies are properties of their respective owners.
