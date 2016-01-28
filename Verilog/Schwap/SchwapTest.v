`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   00:14:56 01/28/2016
// Design Name:   schwap
// Module Name:   /home/hirschag/xilinxworking/csse232/SchwapTest.v
// Project Name:  csse232
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: schwap
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

module SchwapTest;

	// Inputs
	reg clk;
	reg write;
	reg [1:0] readAddrA;
	reg [1:0] readAddrB;
	reg [1:0] writeAddr;
	reg [15:0] writeData;
	reg [3:0] schwapReg;
	reg schwapClk;

	// Outputs
	wire [15:0] readDataA;
	wire [15:0] readDataB;
	
	//temps
	
	integer i;
	integer j;
	integer k;

	// Instantiate the Unit Under Test (UUT)
	schwap uut (
		.clk(clk), 
		.write(write), 
		.readAddrA(readAddrA), 
		.readAddrB(readAddrB), 
		.writeAddr(writeAddr), 
		.writeData(writeData), 
		.readDataA(readDataA), 
		.readDataB(readDataB), 
		.schwapReg(schwapReg), 
		.schwapClk(schwapClk)
	);

	initial begin
		// Initialize Inputs
		clk = 0;
		write = 0;
		readAddrA = 0;
		readAddrB = 0;
		writeAddr = 0;
		writeData = 0;
		schwapReg = 0;
		schwapClk = 0;

		// Wait 100 ns for global reset to finish
		#100;
        
		// Add stimulus here
		schwapReg = 0;
		#5;
		schwapClk = 1;
		#5;
		schwapClk = 0;
		write = 1;
		k = 0;
		for(i = 0; i<16; i = i + 1) begin
			schwapReg = i;
			#5;
			schwapClk = 1;
			#5;
			schwapClk = 0;
			#5;
			for(j = 0; j<4; j = j + 1) begin
				writeAddr = j;
				writeData = j;
				$display("writing %d to %d in schwap %d",j,j,i);
				#5;
				clk = 1;
				#5;
				clk = 0;
				#5;
				k = k + 1;
			end
		end
		write = 0;
		#50;
		k = 0;
		for(i = 0; i<16; i = i + 1) begin
			schwapReg = i;
			#5;
			schwapClk = 1;
			#5;
			schwapClk = 0;
			#5;
			for(j = 0; j<4; j = j + 1) begin
				readAddrA = j;
				readAddrB = j;
				clk = 1;
				#5;
				clk = 0;
				$display("%d & %d for schwap %d should be %d & %d and are %d & %d",j,j,i,j,j, readDataA, readDataB);
				#10;
				k = k + 1;
			end
		end
		$finish;

	end
      
endmodule

