import ctypes

def gen_testbench(mean, covariance, matrix, result):
    assert (mean.shape[0] == matrix.shape[0])
    (mean.shape[0] == covariance.shape[0] == covariance.shape[1])
    assert (matrix.shape[1] >= len(result))

    with open("cpu_simulator.vhd", 'r') as file:
        line_col = file.readlines()
    with open("cpu_simulator.vhd", 'w') as file:
        first = False
        second = False
        written = False
        for line in line_col:
            if "--GEN_TESTS" not in line:
                if first == second:
                    file.write(line)
                elif not written:
                    write_testbench(file, mean,
                                    covariance, matrix, result)
                    written = True
            else:
                file.write(line)
                if first:
                    second = True
                else:
                    first = True


def write_testbench(file, mean, covariance, matrix, result):
    write_cov(file, covariance)
    write_mean(file, mean)
    write_all_pixel(file, matrix)

    file.write("start <= '1';\n")
    file.write("wait until CLK = '1';\n")
    file.write("start <= '0';\n")
    file.write("wait until CLK = '1';\n")
    file.write("\n")
    file.write("wait until ready = '1';\n")

    write_assert(file, result, matrix.shape[1])


def write_cov(file, covariance):
    file.write("cov_fifo_wr_en <= '1';\n")
    file.write("\n")
    for col in covariance:
        s = 'cov_fifo_din <= x"'
        for e in col:
            s += hex(ctypes.c_uint.from_buffer(ctypes.c_float(e)).value)[2:].zfill(8)
        s += '";\n'
        file.write(s)
        file.write("wait until CLK = '1';\n")
    file.write("\n")
    file.write("cov_fifo_wr_en <= '0';\n")
    file.write("\n")
    file.write("\n")


def write_mean(file,mean):
    file.write("mean_fifo_wr_en <= '1';\n")
    file.write("\n")
    for e in mean:
        s = 'mean_fifo_din <= x"'
        s += hex(ctypes.c_uint.from_buffer(ctypes.c_float(e)).value)[2:].zfill(8)
        s += '";\n'
        file.write(s)
        file.write("wait until CLK = '1';\n")
    file.write("\n")
    file.write("mean_fifo_wr_en <= '0';\n")
    file.write("\n")
    file.write("\n")


def write_all_pixel(file, matrix):
    file.write("mean_fifo_wr_en <= '1';\n")
    file.write("\n")
    for row in matrix.transpose():
        for e in row:
            s = 'mean_fifo_din <= x"'
            s += hex(ctypes.c_uint.from_buffer(ctypes.c_float(e)).value)[2:].zfill(8)
            s += '";\n'
            file.write(s)
            file.write("wait until CLK = '1';\n")
    file.write("\n")
    file.write("mean_fifo_wr_en <= '0';\n")
    file.write("\n")
    file.write("\n")


def write_assert(file, result, size):
    file.write("res_fifo_rd_en <= '1';\n")
    file.write("\n")
    file.write("wait until CLK = '1';\n")
    file.write("wait until CLK = '1';\n")
    bin_size = len(bin(size - 1)) - 2
    hex_size = len(hex(size - 1)) - 2
    for e in result:
        s = 'assert (res_fifo_dout = "'
        s += bin(e)[2:].zfill(bin_size)
        s += '") report " coord: '+hex(e)[2:].zfill(hex_size)+'" severity FAILURE;\n'
        file.write(s)
        file.write("wait until CLK = '1';\n")
    file.write("\n")
    file.write("res_fifo_rd_en <= '0';\n")
    file.write("\n")
    file.write("\n")
