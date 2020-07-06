cov_up = 20
inv_up = 29

forw = 24
back = 17
diag_up = 48
diag_dw = 27

st_mult = 0
st_accum = 0
nd_mult = 0

precision        = 24
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
mean_sub_s_precision = 24

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