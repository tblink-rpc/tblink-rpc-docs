********
Overview
********

Digital simulation has always relied on being able to integrate external 
models. In the days before SystemVerilog, the testbench environment
for a Verilog or VHDL design was nearly always external to the 
design. It might be implemented in C/C++, one of the purpose-built
verification languages, or maybe even Java. With a VHDL or Verilog
simulation, external models nearly always integrated at the signal level.

With the introduction of SystemVerilog, external models gained new
integration capabilities with the introduction of the SystemVerilog
Direct Procedural Interface (DPI). Interacting with the design 
at the signal level from an external model was still possible, but
increasingly unneeded and undesirable. The testbench portion of the
SystemVerilog language made it easier to specify signal-level 
interactions between the testbench and design directly in SystemVerilog.
New performance optimizations introduced by simulator vendors often
worked only for design regions that were inaccessible to the older
signal-level APIs. 

SystemVerilog enables the testbench to move directly into the simulator, 
but external models are still important. Reference models, used for 
checking, are often implemented in C++. External stimulus models,
such as virtual platform simulators (eg QEMU) are implemented as
standalone tools. Integrating these external models can certainly
be done using the SystemVerilog DPI, but require a significant 
amount of design, development, and maintenance effort 
for each integration.

Due to API differences across simulators (SystemVerilog vs Verilog 
vs SystemC vs silicon), a different integration must be constructed 
for each supported simulation environment.

TbLink RPC (Testbench Link Remote Procedure Call) is a set of 
libraries and automation scripts with the goal of simplifying
creating simulation extensions that interact with a HDL simulation
at the procedure-call level. There are three primary outcomes
that TbLink RPC targets:

- Simplify object-oriented RPC between object-oriented testbench 
  and simulation environments
- Separate simulator support from application integration 
  enabling, for example, integrating a new testbench language 
  without needing to add new simulator integrations
- Common procedural abstraction layer with support for commercial
  and open source simulation environments.




