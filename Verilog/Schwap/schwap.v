`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    23:36:46 01/27/2016 
// Design Name: 
// Module Name:    schwap 
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
module schwap (
	input clk,
	input write,
	input [1:0] readAddrA,
	input [1:0] readAddrB,
	input [1:0] writeAddr,
	input [15:0] writeData,
	output reg [15:0] readDataA,
	output reg [15:0] readDataB,
	input [3:0] schwapReg,
	input schwapClk
	);
	 
	reg [15:0] reg0[0:15];
	reg [15:0] reg1[0:15];
	reg [15:0] reg2[0:15];
	reg [15:0] reg3[0:15];
	reg [3:0] sReg;
	
	always @(posedge schwapClk) begin
		sReg = schwapReg;
	end
	
	always @(posedge clk) begin
		case (readAddrA)
			0: readDataA = reg0[sReg];
			1: readDataA = reg1[sReg];
			2: readDataA = reg2[sReg];
			3: readDataA = reg3[sReg];
			default: readDataA = 16'hXXXX;
		endcase
		case (readAddrB)
			0: readDataB = reg0[sReg];
			1: readDataB = reg1[sReg];
			2: readDataB = reg2[sReg];
			3: readDataB = reg3[sReg];
			default: readDataB = 16'hXXXX;
		endcase
	end
	
	always @(posedge clk) begin
		if (write)
			case(writeAddr)
				0: reg0[sReg] <= writeData;
				1: reg1[sReg] <= writeData;
				2: reg2[sReg] <= writeData;
				3: reg3[sReg] <= writeData;
			endcase
	end
	
endmodule
