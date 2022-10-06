def int_2_digits(n:int):
    mod = 2**30
    flag = 1 if n >= 0 else -1
    ob_size = 0
    digits = []

    n = abs(n)
    while n > 0:
        digits.append(n % mod)
        n = n // mod
        ob_size += 1

    ob_size = flag * ob_size

    return ob_size, digits


def digits_2_int(ob_size:int, digits:list):
    SHIFT = 30
    n = 0
    
    if ob_size == 0:
        return n

    for i in range(abs(ob_size)):
        n += digits[i] * (2 ** (SHIFT * i))

    return n if ob_size > 0 else -n




def print_digits(n:int):
    ob_size, digits = int_2_digits(n)
    new_n = digits_2_int(ob_size, digits)
    # digits = [hex(i) for i in digits]
    print("n:{} ob_size:{} digits:{} new_n:{}".format(n, ob_size, digits, new_n))
    assert n == new_n, "n:{} ob_size:{} digits:{} new_n:{}".format(n, ob_size, digits, new_n)


print_digits(2**10)
print_digits(-(2**51+1))
print_digits(10000000000000000000000)

# for n in range(-(2**40), 2**40, 2**20):
    # print(n)
    
        
