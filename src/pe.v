

module PE #(
    parameter width = 8;
)(
    input wire clk,
    input wire rst,
    input wire clear,
    input wire signed [width-1:0] a_in;
    input wire signed [width-1:0] b_in;

    output reg signed [width-1:0] a_out;
    output reg signed [width-1:0] b_out;

    output reg signed [width*2-1:0] c_out;
);

    always @(posedge clk) begin
        a_out <= a_in;
        b_out <= b_in;
        
        if(rst) begin
            c_out <= 0;
            a_out <= 0;
            b_out <= 0;
        end else if(clear) begin
            c_out <= a_in * b_in;
        end else begin
            c_out <= c_out + (a_in * b_in);
        end
    end

endmodule