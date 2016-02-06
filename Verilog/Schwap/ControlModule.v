`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    19:09:02 02/02/2016 
// Design Name: 
// Module Name:    ControlModule 
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
module ControlModule(
    input [3:0] opcode,
	 input clk,
	 output wire PCSrc,
	 output wire PCWrite,
	 output wire Addr0Src,
	 output wire memRead,
	 output wire memWrite,
	 output wire nextInstWrite,
	 output wire [1:0] regStore,
	 output wire regWrite,
	 output wire imm,
	 output wire R0Write,
	 output wire R1Write,
	 output wire [1:0] ALUsrc0,
	 output wire ALUsrc1,
	 output wire ALUctrl,
	 output wire SchwapClk
	 );

	reg [3:0] state;
	
	always @(negedge clk) begin
		if (state < 4) begin
			state = state + 1;
		end
		else begin
			state = 0;
		end
	end
	
	always @(posedge clk) begin
		if (state == 0)begin
			PCSrc = 1'b1;
			PCWrite = 1'b1;
			Addr0Src = 1'b1;
			memRead = 1'b1;
			memWrite = 1'b0;
			IRwrite = 1'b1;
			nextInstWrite = 1'b1;
		end else if (state == 1) begin
			memWrite = 1'b0;
			IRwrite = 1'b0;
			nextInstWrite = 1'b0;
			regWrite = 1'b0;
			R0write = 1'b1;
			R1write = 1'b1;
			ALUsrc0 = 2'b00;
			ALUsrc1 = 1'b1;
			ALUctrl = 1'b0;
			SchwapClk = 1'b0;
			if (opcode == 1) begin
				PCwrite = 1'b1;
				regStore = 2'b01;
				imm = 1'b1;
			end else begin
				PCwrite = 1'b0;
				regStore = 2'b00;
				imm = 1'b0;
			end
		end else if (state == 2) begin
			memWrite = 1'b0;
			regWrite = 1'b0;
			R0write = 1'b0;
			R1write = 1'b0;
			PCsrc = 1'b0;
			IRwrite = 1'b0;
			nextInstWrite = 1'b0;
			if (opcode == 0 || opcode == 1) begin
				PCwrite = 1'b0;
				ALUsrc0 = 2'b01;
				ALUsrc1 = 1'b0;
				ALUctrl = 1'b1;
				SchwapClk = 1'b0;
			end else if (opcode == 2 || opcode == 3 || opcode == 4 || opcode == 5 || opcode == 7 || opcode == 8) begin
				PCwrite = 1'b1;
				ALUsrc0 = 2'b10;
				ALUsrc1 = 1'b0;
				ALUctrl = 1'b0;
				SchwapClk = 1'b0;
			end else if (opcode == 6) begin
				PCwrite = 1'b1;
				ALUsrc0 = 2'b01;
				ALUsrc1 = 1'b1;
				ALUctrl = 1'b0;
				SchwapClk = 1'b0;
			end else if (opcode == 14) begin
				PCwrite = 1'b0;
				ALUsrc0 = 2'b00;
				ALUsrc1 = 1'b0;
				ALUctrl = 1'b0;
				SchwapClk = 1'b1;
			end else if (opcode == 15) begin
				PCwrite = 1'b0;
				ALUsrc0 = 2'b00;
				ALUsrc1 = 1'b0;
				ALUctrl = 1'b0;
				SchwapClk = 1'b0;
			end
		end else if (state == 3) begin
			PCwrite = 1'b0;
			Addr0Src = 1'b0;
			IRwrite = 1'b0;
			regStore = 1'b0;
			if (opcode == 0 || opcode == 1) begin
				memRead = 1'b0;
				memWrite = 1'b0;
				regWrite = 1'b1;
			end else if (opcode == 7) begin
				memRead = 1'b1;
				memWrite = 1'b0;
				regWrite = 1'b0;
			end else if (opcode == 8) begin
				memRead = 1'b0;
				memWrite = 1'b1;
				regWrite = 1'b0;
			end
		end else if (state == 4) begin
			PCwrite = 1'b0;
			memRead = 1'b0;
			memWrite = 1'b0;
			IRwrite = 1'b0;
			regStore = 1'b0;
			regWrite = 1'b1;
		end
	end	

endmodule
