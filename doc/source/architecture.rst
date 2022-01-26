************
Architecture
************

Due to the requirements for flexibility and scalability, TbLink RPC
uses a layered architecture. It's reasonable to think of this 
layered architecture as being similar to a network stack. 

Concept Model
=============

Let's start with some key concepts that are used across the document.
There is implementation behind these concepts, but it's useful to 
understand their purpose at a high level before diving into the details.

.. image:: imgs/concept_diagram.png
  

Environments and Endpoints
--------------------------

TbLink RPC exists to allow simulation-centric environments to 
communicate. Each pair of communicating environments has a 
pair of connected endpoints. An environment may communicate
with multiple other environments, but each pair of connected
environments may only be connected by a single pair of
TbLink RPC endpoints.

One result of TbLink RPC being simulation-centric is the 
requirement to  synchronize and control time. For example, when 
one environment is a simulator and the other is a testbench, 
it is critical to ensure that the simulation advances only
once the testbench has responded to all pending simulation
events. If this requirement isn't met, our ability to properly
interact with the design under test (DUT) will be impaired.

TbLink RPC is not a simulator co-simulation framework, with 
support for synchronizing the operation of multiple simulators
each with their own notion of time. Consequently, one 
environment is considered the *Timebase Provider*. The 
*Timebase Provider* environment maintains the current time 
for all environments, and provides support for time-based
callbacks. 

.. note::
  TbLink RPC doesn't enforce the restriction on having only
  a single Timebase Provider. This restriction is simply
  a pragmatic one, given the implementation of capabilities
  of most simultors today.

Methods, Interfaces, and Interface Types
----------------------------------------

.. image:: imgs/iftype_ifinst_mirror.png

TbLink RPC environments communicate via method calls. Method
calls are made with respect to *interface instances*. Each
*interface instance* has an *interface type*, which captures
which methods are available.

An interface type specifies type and usage information about 
methods. Specifically, it captures:

- The return type of the method
- Method parameter names and types
- Whether the method is time-consuming
- Whether the method is an *export* or an *import*.

This last bit -- export vs import -- is of critical importance.
An imported method is called by the environment, while an 
exported method is implemented by the environment and called
by TbLink RPC in response to a call from the peer environment.

Both connected interface instances have the same interface type.
However, one is designated a *mirror* interface. A *mirror* 
interface implements the "mirror" of methods, so an export
method is implemented as an import on a *mirror* interface, and
an import method is implemented as an export.

.. note::
  The terminology of import, export, and mirror comes from the
  vocabulary of Transaction-Level Modeling and IP-XACT IP
  encapsulation.
  
When defining an interface type, whether a method itself is an
import or an export is entirely irrelevant. For example, the 
interface type above could have been defined with *Req* being 
an import and *Rsp* being an export. The practical impact of 
this decision would be that the right-hand interface instance
would need to be specified as a mirror and the left-hand 
interface instance would need to be specified as a non-mirror 
in order to preserve the caller/called relationship.

Methods may be denoted as either time-consuming or non-time-consuming.
This is a critical distinction precisely because TbLink RPC is targeted
at enabling communication with simulation environments. When 
non-time-consuming methods are called, TbLink RPC understands that 
time in the simulation environment must not advance. When time-consuming
methods are called, TbLink RPC understands that it may be necessary for
time in the simulation environment to advance before the method call 
is complete.



Implementation Model
====================

Implementation of TbLink RPC is split into three major components:

- User Facades
- Core Implementation
- Environment Integration

As the name suggests, the user facade is the primary aspect of 
interest to end users. 

The implementation core is primarily of interest to developers
wishing to extend TbLink RPC to support another front-end 
language and/or simulator integration. Core Implementation must
support all user facades and environment integrations.

Environment integration is responsible for handling 
environment-specific details. For example, propagating events
properly in Verilog via the VPI API. Generally, environment 
integration is the smallest body of code in TbLink RPC.

User Facade
-----------
Every language and language methodology used for functional
verification and with simulation models time and events 
in some form. In standard fashion, different languages and
methodologies represent these same concepts in different ways. 
For example, SystemVerilog represents time-consuming methods
as *tasks* and language constructs for modeling events, while 
Python represents the same concept using *async* methods and
classes in the standard library. 

The purpose of language- and methodology-specific facades is 
to adapt TbLink RPC to the appropriate language- and 
methodology-specific constructs. 

The adaptation can go far beyond just adapting TbLink RPC to
threading and event constructs supported by the target
environment. For example, Python provides rich introspection
and annotation capabilities that enable the user to 
capture meta-data for TbLink RPC directly in Python instead
of in a separate side file. 

.. code:: python3

  import tblink_rpc
  import ctypes

  @tblink_rpc.iftype("rv_bfms.initiator")
  class RvInitiatorBfm(object):

      @tblink_rpc.exptask
      async def req(self, data : ctypes.c_uint64):
          pass

      @tblink_rpc.impfunc
      def rsp(self):
          pass


The code snippet above shows interface-type information 
captured as annotations on the Python class that implements
an interface instance. Other environments may have similar
environment- or language-specific mechanisms that provide
enhanced capabilities when TbLink RPC is used with that
environment.

Core Implementation
-------------------

The User Facade layer is characterized by differences. It's goal is 
to provide the best user experience possible based on the target
environment. In contrast, the Core Implementation layer is 
characterized by similarity. In nearly all cases, the 
Core Implementation layer for different languages and environments
have identical APIs, or very nearly identical APIs.

In many cases, this similarity is very important because of 
cross-language reuse of the Core Implementation layer. For example,
when a SystemVerilog is connected via a socket to an executable 
running as a separate process, the SystemVerilog Core Implementation
layer uses the C++ Core Implementation layer to implement 
process management and socket communication.

With that, let's dive into the key objects in the Core Implementation
layer.

Environment Integration
-----------------------

Nearly every environment requires some amount of integration
code to be able to access TbLink functionality. In many cases, this
code exists to access the C++ implementation of TbLink. In the
case of most simulation environments, some amount of code exists
to trigger events in the simulation environment. The goal is for 
this environment-specific code to be as light-weight as possible.

Current environment integrations include:

- SystemVerilog simulation (DPI)
- Verilog simuilation (VPI)
- Python (Cython/C++ binding)
- Gateware for Silicon targets (byte-oriented interface)

Automation
----------

A key aspect of the TbLink-RPC approach is automation to generate
boilerplate implementation code from 

Use-Cases / Application Examples
================================

Here are a few examples of TbLink RPC applications.

Python-Driven UVM Sequence Execution
------------------------------------

.. image:: imgs/usecase_python_uvm_sequence.png

It is often attractive to use Python for capturing tests
because of the flexibility and familiarity of the language, 
and because of access to Python libraries for algorithmic
stimulus generation. However, an existing SystemVerilog/UVM 
testbench typically contains extensive infrastructure, such
as bus functional models (BFMs) and/or verification IP (VIP),
a register model, and utility sequences for performing
standard operations on the design under test. 

Leveraging all of this existing infrastructure is highly
desirable. In order to do so, we effectively need some 
Python code to run in the context of the UVM 
virtual sequence running in the SystemVerilog environment.

The two key TbLink RPC capabilities exercised in this 
application example are:

- Support for dynamically creating interface instances
  and passing them between environments.
- Making multiple blocking calls between environments.

The key steps in this example are as follows:

- The Python environment creates a TbLink RPC 
  *interface instance* that corresponds to the UVM 
  virtual sequence. 
- The Python environment passes this *interface instance*
  to a method in the SystemVerilog testbench environment, 
  where handles to agents and register model are populated, 
  and that starts the UVM sequence.
- When the UVM testbench calls the sequence *body* task,
  the body task is invoked in the Python environment. 
- The Python *body* method can now drive behavior in the
  UVM testbench by calling utility methods in the virtual
  sequence.

UVM Sequence Implemented in Python
----------------------------------

.. image:: imgs/usecase_sv_seq_python_impl.png

This usecase is somewhat the inverse of the previous usecase.
In the previous example, the Python testbench created a sequence
and executed it in the UVM testbench. In this example, the
UVM testbench creates a sequence that is implemented in Python.

The key steps in this example are:
- The UVM testbench creates a SystemVerilog sequence class
that extends from a tblink-rpc implementation class
- When the sequence is run, it starts an embedded Python
interpreter and runs the specified 


SystemVerilog Co-Simulation with C/C++ Software Behavior
--------------------------------------------------------

.. image:: imgs/usecase_zephyr_integration.png

Bringing some aspects of software behavior into an IP-level
environment enables firmware to be developed during the IP
design and verification effort. One way of doing this is
to native-compile the `Zephyr RTOS <https://www.zephyrproject.org>`_ 
real-time operating system and co-simulate its software
behavior with the testbench and design. The 
`Zephyr-Cosim <https://github.com/zephyr-dv/zephyr-cosim>`_ project
provides integration code and uses TbLink-RPC to connect
a compiled Zephyr application to a simulation environment.

Python Driving a Silicon Platform
---------------------------------

.. image:: imgs/usecase_silicon_platform.png

Validation efforts continue past simulation onto silicon 
platforms. It is highly beneficial to be able to leverage
some aspects of the pre-silicon verification environment
in the post-silicon world. A combination of TbLink-RPC,
interface code generation, and BFMs/transactors enable
a carefully-selected subset of the verification environment
to be reused from verification to validation.


