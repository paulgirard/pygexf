welcome users !
---------------


installation
============

requirements
~~~~~~~~~~~~

pygexf uses lxml as XML engine.
you'll need lxml to use it.

See http://codespeak.net/lxml/ for installation

easy_install method
~~~~~~~~~~~~~~~~~~~

pygexf is hosted in pypi.python.org.
Thus you can use easy_install from setuptools to install it.

First install setup tools if not already in your system : http://pypi.python.org/pypi/setuptools

Then it's quite easy : 

$ sudo easy_install pygexf

to check : 

$ python


>>> import gexf

If no errors are raised then you're done.


embed pygexf in your project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a quick and durty method. Use easy_install instead.
(but still sometime usefull)

pygexf is a single file package.
You can decide not to install it in your python environement but directly in your source where you need it.
In such case go directly to the soruce repository :
http://github.com/paulgirard/pygexf

Download the gexf directory to your source.
$ls 
gexf

$python


>>> import gexf

no errors ? (remember to install lxml first !)
you're done.


Use Cases
=========

You can find useful information here : http://gexf.net and here http://forum.gephi.org, before a real comfy and warm documentation is available. 

