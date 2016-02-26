`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 		Schwap
// Engineer: 		Alexander Hirschfeld
// 
// Create Date:    12:22:57 01/29/2016 
// Design Name: 	regFile with Schwap
// Module Name:    RegisterFile 
// Project Name: 		Schwappable MEmory
// Target Devices: Only in this class
// Tool versions: 
// Description: 	This is a register file that has the schwappable registers implemented and changable with Schlatch
//
// Dependencies: Schwap
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module RegisterFile(
	input clk,
	input write,
	input [3:0] readAddrA,
	input [3:0] readAddrB,
	input [3:0] writeAddr,
	input [15:0] writeData,
	output reg [15:0] readDataA,
	output reg [15:0] readDataB,
	input [3:0] schwapReg,
	input schwapClk
    );
	 
	reg [15:0] reg0[0:3]; //registers 0:3
	reg [15:0] reg1[0:3]; //registers 4:7
	reg [15:0] reg2[0:3]; //registers 8:11
	
	wire [1:0] readAddrA1; //testing things, splting address bus into 2 so things are easier.
	wire [1:0] readAddrA2;
	wire [1:0] readAddrB1;
	wire [1:0] readAddrB2;
	
	wire [1:0] writeAddr1;
	wire [1:0] writeAddr2;
	
	wire [15:0] schwapReadA;
	wire [15:0] schwapReadB;
	wire schwapWrite;

	schwap reg3 (
		.clk(clk),
		.write(schwapWrite),
		.readAddrA(readAddrA2),
		.readAddrB(readAddrB2),
		.writeAddr(writeAddr2),
		.writeData(writeData),
		.readDataA(schwapReadA),
		.readDataB(schwapReadB),
		.schwapReg(schwapReg),
		.schwapClk(schwapClk)
	);
	
	assign readAddrA1 = readAddrA[3:2];
	assign readAddrA2 = readAddrA[1:0];
	assign readAddrB1 = readAddrB[3:2];
	assign readAddrB2 = readAddrB[1:0];
	 
	assign writeAddr1 = writeAddr[3:2];
	assign writeAddr2 = writeAddr[1:0];
	
	assign schwapWrite = writeAddr1[0] & writeAddr1[1] & write;
	
	//readA
	always @(*) begin
		case (readAddrA1)
			0: readDataA = reg0[readAddrA2];
			1: readDataA = reg1[readAddrA2];
			2: readDataA = reg2[readAddrA2];
			3: readDataA = schwapReadA;
			default: readDataA = 16'hXXXX;
		endcase
		case (readAddrB1)
			0: readDataB = reg0[readAddrB2];
			1: readDataB = reg1[readAddrB2];
			2: readDataB = reg2[readAddrB2];
			3: readDataB = schwapReadB;
			default: readDataB = 16'hXXXX;
		endcase
	end
	
	always @(clk) begin
	if (write)
		case(writeAddr1)
			0: reg0[writeAddr2] <= writeData;
			1: reg1[writeAddr2] <= writeData;
			2: reg2[writeAddr2] <= writeData;
			//3: $display("schwap write");
		endcase
	end


endmodule
