import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer, ClockCycles


@cocotb.test()
async def test_systolic_array(dut):
    """Test basic  2x2 matrix multiplication"""

    cocotb.log.info("Starting systolic array test")

    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    dut.rst.value = 1
    dut.clear.value = 1
    dut.activation.value = 0
    dut.a_data0.value = 0
    dut.a_data1.value = 0
    dut.b_data0.value = 0
    dut.b_data1.value = 0

    await Timer(20, unit="ns")

    dut.rst.value = 0
    dut.clear.value = 1
    await RisingEdge(dut.clk)

    dut.clear.value = 0
    await RisingEdge(dut.clk)

    matrix_A = [[1, 4], [5, 9]]
    matrix_B = [[2, 5], [3, 9]]

    weights = [matrix_A[0][0], matrix_A[0][1], matrix_A[1][0], matrix_A[1][1]]
    inputs = [matrix_B[0][0], matrix_B[0][1], matrix_B[1][0], matrix_B[1][1]]

    # cycle 0
    dut.a_data0.value = weights[0]
    dut.a_data1.value = 0
    dut.b_data0.value = inputs[0]
    dut.b_data1.value = 0
    await RisingEdge(dut.clk)

    # cycle 1
    dut.a_data0.value = weights[1]
    dut.a_data1.value = weights[2]
    dut.b_data0.value = inputs[2]
    dut.b_data1.value = inputs[1]
    await RisingEdge(dut.clk)

    # cycle 2
    dut.a_data0.value = 0
    dut.a_data1.value = weights[3]
    dut.b_data0.value = 0
    dut.b_data1.value = inputs[3]
    await RisingEdge(dut.clk)

    # clear inputs
    dut.a_data0.value = 0
    dut.a_data1.value = 0
    dut.b_data0.value = 0
    dut.b_data1.value = 0

    await ClockCycles(dut.clk, 2)

    c00 = dut.c00.value.signed_integer
    c01 = dut.c01.value.signed_integer
    c10 = dut.c10.value.signed_integer
    c11 = dut.c11.value.signed_integer

    cocotb.log.info(f"Output matrix")
    cocotb.log.info(f"C00 = {c00}")
    cocotb.log.info(f"C01 = {c01}")
    cocotb.log.info(f"C10 = {c10}")
    cocotb.log.info(f"C11 = {c11}")

    assert c00 == 14, f"C00 expected to be 14"
    assert c01 == 41, f"C01 expected to be 39"
    assert c10 == 37, f"C10 expected to be 55"
    assert c11 == 106, f"c11 expected to be 106"

    cocotb.log.info("Systolic array multiplicated passed")
