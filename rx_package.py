read_cov = 20
read_inv = 28 #28 hidyce, 30 wtc

forw = 20
back = 18
diag = 20

write_up = 31 #31 hydice, 30 wtc
write_dw = 0

st_mult = -14 #-14 hydice, -18 wtc
st_accum = 0 #0 hydice, -3 wtc
nd_mult = -18 #-18 hydice, -19 wtc

precision        = 48
ram_precision    = 42
sorter_precision = 48

dividend_precision    = ram_precision
divisor_precision     = ram_precision
quotient_precision    = 35
gauss_mul_a_precision = ram_precision
gauss_mul_b_precision = quotient_precision
gauss_mul_p_precision = 48
gauss_sub_a_precision = ram_precision
gauss_sub_b_precision = gauss_mul_p_precision
gauss_sub_s_precision = ram_precision

mean_sub_a_precision = precision
mean_sub_b_precision = precision
mean_sub_s_precision = 48

mult_st_mul_a_precision = mean_sub_s_precision
mult_st_mul_b_precision = ram_precision
mult_st_mul_p_precision = 48
mult_st_accum_in_precision  = mult_st_mul_p_precision
mult_st_accum_out_precision = 48

mult_nd_mul_a_precision = mean_sub_s_precision
mult_nd_mul_b_precision = mult_st_accum_out_precision
mult_nd_mul_p_precision = 48
mult_nd_accum_in_precision  = mult_nd_mul_p_precision
mult_nd_accum_out_precision = sorter_precision