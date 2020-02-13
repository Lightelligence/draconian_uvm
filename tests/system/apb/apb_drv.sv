`ifndef __APB_DRV_SV__
 `define __APB_DRV_SV__

class helper_c extends base_cfg_c;
   boring;
endclass : helper_c

class apb_drv_c extends uvm_driver;

   `uvm_componenet_utils(apb_pkg::apb_drv_c)

   function new(string name="apb_drv",
                uvm_component parent);
      super.new(name, parent);
      // duvm: disable=DollarDisplay
      $display("made a bad");
   endfunction : new
endclass : apb_drv_c

`endif // guard
