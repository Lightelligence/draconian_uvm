What is draconian_uvm?
----------------------

SystemVerilog's and UVM's effectiveness has been argued ad
nauseam. Nevertheless, it is the current state of the art in constrained-random verification
methodology. Unfortunately, it contains many footguns that may prevent easy
vertical reintegration (into subsystem and fullchip simulations).

draconian_uvm (duvm) is linter for an additional set of guidelines imposed on
top of UVM that aims to make vertical reintegration easier.

It checks for:
1. Coding style
   A uniform coding styles makes reading code easier
2. Common UVM "gotchas"


Details
-------
For the purpose of this tool, there are three main categories of files in UVM:

1. Testbench Top
   This is the file that instantiates the DUT. Generally, there is only one per
   testbench. While some guidelines may apply to this type of file, it is not
   the focus of this tool as it is not generally used for reintegration.
2. Tests
   Tests are the top level instantiation of UVM components. These files are
   also generally not reused across testbenches.
3. UVC
   A universal verification component is a piece intended to be reused either
   horizontally or vertically. This where the majority of rules will be
   applied.
   
