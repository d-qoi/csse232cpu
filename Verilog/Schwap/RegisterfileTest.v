`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   20:44:19 01/29/2016
// Design Name:   RegisterFile
// Module Name:   /home/hirschag/xilinxworking/csse232/RegisterfileTest.v
// Project Name:  csse232
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: RegisterFile
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

module RegisterfileTest;

	// Inputs
	reg clk;
	reg write;
	reg [3:0] readAddrA;
	reg [3:0] readAddrB;
	reg [3:0] writeAddr;
	reg [15:0] writeData;
	reg [3:0] schwapReg;
	reg schwapClk;

	// Outputs
	wire [15:0] readDataA;
	wire [15:0] readDataB;
	
	integer temp1;
	integer temp2;
	integer pass; 

	// Instantiate the Unit Under Test (UUT)
	RegisterFile uut (
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
		
		temp2 = -1;
		write = 1;
		for (temp1 = 0; temp1 < 12; temp1 = temp1 + 1) begin
			
			temp2 = temp2 + 1;
			writeAddr= temp1;
			writeData = temp2;
			#5;
			clk = 1;
			#5;
			clk = 0;
			#5;
		end
		write = 0;
		
		pass = 1;
		temp2 = -1;
		for (temp1 = 0; temp1 < 12; temp1 = temp1 + 1) begin
			temp2 = temp2 + 1;
			readAddrA = temp1;
			readAddrB = temp1;
			#5;
			if (readDataA != temp2 && readDataB != temp2) begin
				$display("Register error, %d != %d, in %d", temp2, readAddrA, temp1);
				pass = 0;
			end
			#5;
		end
		if (pass == 1)
			$display("All normal registers pass");
			
		write = 1;
		for (temp1 = 12; temp1 < 16; temp1 = temp1 + 1) begin
			for(temp2 = 0; temp2 < 4; temp2 = temp2 + 1) begin
				writeAddr = temp1;
				writeData = temp1 + temp2;
				schwapReg = temp2;
				#2;
				schwapClk = 1;
				#3;
				schwapClk = 0;
				clk = 1;
				#5;
				clk = 0;
				#5;
			end
		end
		write = 0;
		
		pass = 1;
		for (temp1 = 12; temp1 < 16; temp1 = temp1 + 1) begin
			for(temp2 = 0; temp2 < 4; temp2 = temp2 + 1) begin
				readAddrA = temp1;
				readAddrB = temp1;
				schwapReg = temp2;
				#2;
				schwapClk = 1;
				#3;
				schwapClk = 0;
				#5;
				if (readDataA != (temp1 + temp2) && readDataB != (temp1 + temp2)) begin
					$display("Schwap Error %d != %d at %d:%d",temp1 + temp2, readDataA, temp2,temp1);
					pass = 0;
				end
			end
		end
		if (pass == 1)
			$display("All Schwap Registers Pass");
		$finish;
	end
      
endmodule

