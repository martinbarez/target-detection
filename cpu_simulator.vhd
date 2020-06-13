library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.textio.all;
use ieee.std_logic_textio.all;

library work;
use work.rx.all;

-----------------------------------------------------------

entity cpu_simulator is

end entity cpu_simulator;

-----------------------------------------------------------

architecture testbench of cpu_simulator is

    -- Testbench DUT generics


    -- Testbench DUT ports
    signal clk   : std_logic;
    signal rst   : std_logic;
    signal n_rst : std_logic;
    signal start : std_logic;
    signal ready : std_logic;

    --covariance fifo
    signal cov_fifo_rd_en : std_logic;
    signal cov_fifo_dout  : std_logic_vector(precision*n_bands-1 downto 0);
    signal cov_fifo_empty : std_logic;

    signal cov_fifo_wr_en : std_logic;
    signal cov_fifo_din   : std_logic_vector(precision*n_bands-1 downto 0);
    signal cov_fifo_full  : std_logic;

    --mean fifo
    signal mean_fifo_rd_en : std_logic;
    signal mean_fifo_dout  : std_logic_vector(precision-1 downto 0);
    signal mean_fifo_empty : std_logic;

    signal mean_fifo_wr_en : std_logic;
    signal mean_fifo_din   : std_logic_vector(precision-1 downto 0);
    signal mean_fifo_full  : std_logic;

    --res_fifo
    signal res_fifo_rd_en : std_logic;
    signal res_fifo_dout  : std_logic_vector(log_pixels-1 downto 0);
    signal res_fifo_empty : std_logic;

    signal res_fifo_wr_en : std_logic;
    signal res_fifo_din   : std_logic_vector(log_pixels-1 downto 0);
    signal res_fifo_full  : std_logic;

    -- Other constants
    constant C_CLK_PERIOD : real := 10.0e-9; -- NS

begin
    -----------------------------------------------------------
    -- Clocks and Reset
    -----------------------------------------------------------
    CLK_GEN : process
    begin
        clk <= '1';
        wait for C_CLK_PERIOD / 2.0 * (1 SEC);
        clk <= '0';
        wait for C_CLK_PERIOD / 2.0 * (1 SEC);
    end process CLK_GEN;

    RESET_GEN : process
    begin
        rst <= '1',
            '0' after 20.0*C_CLK_PERIOD * (1 SEC);
        wait;
    end process RESET_GEN;

    fifo_reset : process (rst)
    begin
        n_rst <= not(rst);
    end process fifo_reset;

    -----------------------------------------------------------
    -- Testbench Stimulus
    -----------------------------------------------------------
    stimulus : process
    begin

        start          <= '0';
        cov_fifo_wr_en <= '0';
        res_fifo_rd_en <= '0';
        wait until rst = '0';
        wait until ready ='1';

        if(cov_fifo_full = '1') then
            wait until cov_fifo_full = '0'; --a day in my life i wont ever get back
        end if;

        --GEN_TESTS

        --GEN_TESTS

        report "finish" severity FAILURE;

    end process stimulus;
    -----------------------------------------------------------
    -- Entity Under Test
    -----------------------------------------------------------

    DUT : entity work.control
        port map (
            clk   => clk,
            rst   => rst,
            start => start,
            ready => ready,

            cov_fifo_rd_en => cov_fifo_rd_en,
            cov_fifo_dout  => cov_fifo_dout,
            cov_fifo_empty => cov_fifo_empty,

            mean_fifo_rd_en => mean_fifo_rd_en,
            mean_fifo_dout  => mean_fifo_dout,
            mean_fifo_empty => mean_fifo_empty,

            res_fifo_din   => res_fifo_din,
            res_fifo_wr_en => res_fifo_wr_en
        );

    covariance : covariance_fifo
        PORT MAP (
            clk   => clk,
            rst   => rst,
            din   => cov_fifo_din,
            wr_en => cov_fifo_wr_en,
            rd_en => cov_fifo_rd_en,
            dout  => cov_fifo_dout,
            full  => cov_fifo_full,
            empty => cov_fifo_empty
        );


    mean_fifo : element_fifo
        PORT MAP (
            clk   => clk,
            rst   => rst,
            din   => mean_fifo_din,
            wr_en => mean_fifo_wr_en,
            rd_en => mean_fifo_rd_en,
            dout  => mean_fifo_dout,
            full  => mean_fifo_full,
            empty => mean_fifo_empty
        );

    res_fifo : result_fifo
        PORT MAP(
            clk   => clk,
            din   => res_fifo_din,
            wr_en => res_fifo_wr_en,
            rd_en => res_fifo_rd_en,
            dout  => res_fifo_dout,
            full  => res_fifo_full,
            empty => res_fifo_empty
        );


end architecture testbench;