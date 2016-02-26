`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   17:09:19 01/20/2016
// Design Name:   CarryLook16b
// Module Name:   C:/XilinxProjectsLocal/CarryLookahead/TestCarry16b.v
// Project Name:  CarryLookahead
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: CarryLook16b
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

module TestCarry16b;

	// Inputs
	reg [15:0] a;
	reg [15:0] b;
	reg sub;

	// Outputs
	wire [15:0] r;
	wire co;

	// Instantiate the Unit Under Test (UUT)
	CarryLook16b uut (
		.a(a), 
		.b(b), 
		.sub(sub), 
		.r(r), 
		.co(co)
	);

	initial begin
		// Initialize Inputs
		a = 0;
		b = 0;
		sub = 0;

		// Wait 100 ns for global reset to finish
		#100;
        
		// Add stimulus here
		
		//TEST ZERO
		a = 0;
		b = 16'b1011011010110110;
		sub = 1;
		#10;
		$display("%x - %x = %x", a, b, r);
		
		a = 0;
		b = 16'b1011011010110110;
		sub = 0;
		#10;
		$display("%x + %x = %x", a, b, r);
		
		b = 0;
		a = 16'b1011011010110110;
		sub = 1;
		#10;
		$display("%x - %x = %x", a, b, r);
		
		
		//TEST OVFL
		
		
		a = 16'b0110000011100000;
		b = 16'b0011011010110110;
		sub = 0;
		#10;
		$display("%x + %x = %x", a, b, r);
		
		a = 16'b1110000011100000;
		b = 16'b1011011010110110;
		sub = 1;
		#10;
		$display("%x - %x = %x", a, b, r);
		
		// Test Normal
		
		a = 16'h0EB4;
		b = 16'hF2E1;
		sub = 0;
		#10;
		$display("%x + %x = %x", a, b, r);
		
		a = 16'h7F01;
		b = 16'h2552;
		sub = 0;		
		#10;
		$display("%x + %x = %x", a, b, r);
		$finish;
	end
endmodule

