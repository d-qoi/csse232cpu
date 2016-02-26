`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    17:04:33 01/20/2016 
// Design Name: 
// Module Name:    CarryLook16b 
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
module CarryLook16b(
		input[15:0] a,
		input[15:0] b,
		input sub,
		output[15:0] r,
		output co
    );
	 wire c1, c2, c3;
	 
	 CarryLook4b a1 (a[3:0], b[3:0], sub, sub, r[3:0], c1);
	 CarryLook4b a2 (a[7:4], b[7:4], c1, sub, r[7:4], c2);
	 CarryLook4b a3 (a[11:8], b[11:8], c2, sub, r[11:8], c3);
	 CarryLook4b a4 (a[15:12], b[15:12], c3, sub, r[15:12], co);
endmodule
