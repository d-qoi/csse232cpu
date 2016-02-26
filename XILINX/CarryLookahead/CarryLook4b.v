`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    16:21:07 01/20/2016 
// Design Name: 
// Module Name:    CarryLook4b 
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
module CarryLook4b(
		input[3:0] a,
		input[3:0] b,
		input c,
		input sub,
		output[3:0] r,
		output co
   );
	wire[3:0] g;
	wire[3:0] p;
	CLACell c1(a[0],b[0] ^ sub, c, g[0], p[0], r[0]);
	CLACell c2(a[1],b[1] ^ sub, (c & p[0]) + (g[0]), g[1], p[1], r[1]);
	CLACell c3(a[2],b[2] ^ sub, (c & p[0] & p[1]) + (g[0] & p[1]) + (g[1]), g[2], p[2], r[2]);
	CLACell c4(a[3],b[3] ^ sub, (c & p[0] & p[1] & p[2]) + (g[0] & p[1] & p[2]) + (g[1] & p[2]) + g[2], g[3], p[3], r[3]);
	assign co = (c & p[0] & p[1] & p[2] & p[3]) + (g[0] & p[1] & p[2] & p[3]) + (g[1] & p[2] & p[3]) + (g[2] & p[3]) + (g[3]);
endmodule
