`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    16:07:48 01/20/2016 
// Design Name: 
// Module Name:    FullAdd1b 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module FullAdd1b(
		input a,
		input b,
		input c,
		output r,
		output co
   );
	wire c1, c2, c3;
	assign r = a ^ b ^ c;
	assign c1 = a^c;
	assign c2 = a^b;
	assign c3 = b^c;
	assign co = c1 + c2 + c3;
endmodule
