`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   16:47:45 01/20/2016
// Design Name:   CarryLook4b
// Module Name:   C:/XilinxProjectsLocal/CarryLookahead/TestCarryAdder.v
// Project Name:  CarryLookahead
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: CarryLook4b
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

module TestCarryAdder;

	// Inputs
	reg [3:0] a;
	reg [3:0] b;
	reg c;
	reg sub;

	// Outputs
	wire [3:0] r;
	wire co;

	// Instantiate the Unit Under Test (UUT)
	CarryLook4b uut (
		.a(a), 
		.b(b), 
		.c(c), 
		.sub(sub),
		.r(r), 
		.co(co)
	);

	initial begin
		// Initialize Inputs
		a = 0;
		b = 0;
		c = 0;
		sub = 0;

		// Wait 100 ns for global reset to finish
		#100; 
        
		// Add stimulus here
		a = 4'b0010;
		b = 4'b0111;
		c = 0;
		#10;
		$display("%d + %d = %d", a, b, r);
		a = 4'b0100;
		b = 4'b0011;
		sub = 1;
		c = 1;
		#10;
		$write("%d - %d = %d", a, b, r);
		
		$finish;
	end
      
endmodule

