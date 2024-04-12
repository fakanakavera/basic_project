def c(a, b, c):
    if a > 0 and b > 0 and c > 0:
        return (a/(b+c))+(b/(a+c))+(c/(a+b))
    return None

for x in range(1000):
    for y in range(1000):
        for z in range(1000):
            i = c(x, y, z)
            if i:
                if i == 4:
                    print('x: ',x)
                    print('y: ',y)
                    print('z: ',z)
                    print('----------------')