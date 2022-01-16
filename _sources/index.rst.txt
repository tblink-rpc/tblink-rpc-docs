.. TbLink RPC documentation master file, created by
   sphinx-quickstart on Thu Dec 30 14:11:47 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to TbLink RPC's documentation!
======================================

TbLink RPC is a simulation-centric communication framework that is designed
to handle a wide variety of simulation environments and testbench languages.
It emphasizes flexibility and automation, with the goals of supporting 
rich communication between object-oriented environments and dramatically 
simplifying the process of connecting a new reference model to an existing
testbench language, or a new testbench language to an existing simulation 
environment.





.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   architecture
   
.. doxygenclass:: tblink_rpc_core::IEndpoint
   :project: tblink_rpc_cpp
   :members:

.. doxygenclass:: tblink_rpc::IEndpoint
   :project: tblink_rpc_sv
   :members:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
