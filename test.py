import hmath as hm


def f(x):

    x_sqr = hm.mul(x, x)
    x_cub = hm.mul(x, x_sqr)
    x_pent = hm.mul(x_sqr, x_cub)
    return hm.add(hm.sub(x, hm.div(x_cub, (1, 6))), hm.div(x_pent, (1, 120)))


def f_prime(x):

    x_sqr = hm.mul(x, x)
    x_rect = hm.mul(x_sqr, x_sqr)
    return hm.add(hm.sub((1, 1), hm.div(x_sqr, (1, 2))), hm.div(x_rect, (1, 24)))

hm.printn(hm.mul(hm.nutmet(f, f_prime, (2, 1), (2, 1), 5), (1, 6)), 12)