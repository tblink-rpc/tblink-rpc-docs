********************
Interaction Protocol
********************

Ideally, understanding the way in which different parts of the TbLink-RPC
system interact is only necessary for developers and integrators. As a 
user, having a deeper understanding of "what goes on under the hood" 
is primarily useful when debugging an issue. That said, the more you know...

In some cases, the interaction protocol is literally implemented by sending
RPC messages over sockets or through FIFOs. In other cases, the interaction
protocol is implemented by a series of method calls. If you're interested
in the details of one of the transport protocols, please see:
- TBD (1)
- TBD (2)

Initialization Protocol
=======================

The initialization protocol comes into play when a connection between
two endpoints is initiated. At each step in the protocol, different
information is assumed to be available and/or consistent at each
of the two endpoints.

.. seqdiag::

  diagram {
    TimebaseProvider  -> TimebaseClient [label = "Init: precision, args"];
    TimebaseProvider  <- TimebaseClient [label = "Init"];
    TimebaseProvider  -> TimebaseClient [label = "Build-Complete: Types/Insts"];
    TimebaseProvider  <- TimebaseClient [label = "Build-Complete: Types/Insts"];
    TimebaseProvider  -> TimebaseClient [label = "Connect-Complete: Types/Insts"];
    TimebaseProvider  <- TimebaseClient [label = "Connect-Complete: Types/Insts"];
  }

During initialization, the two endpoints exchange and compare information 
to ensure that the two have a consistent view of interface types and instances.
Endpoints have a peer relationship. One outcome is that the order in which
each message type is exchanged is not significant. For example, the
TimebaseClient could have been first to send the Init message.

An endpoint provides methods both to signal that a phase is complete 
(eg build-complete) and to confirm that the peer endpoint has also 
signaled phase completion. A phase is complete from the perspective
of an endpoint once it has signaled its completion of the phase and
has confirmed that its peer has also completed the phase.

At the conclusion of each initialization phase, endpoints have
access to specific information. A description of each phase and 
the information available at its completion is below.

Init
----

On completion of the initialization phase, the TimebaseConsumer
endpoint has access to the time-precision of the TimebaseProducer
and has access to any arguments provided by the TimebaseProducer.

Build
-----



Connect
-------




