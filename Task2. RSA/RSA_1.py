from sympy import isprime, randprime
from math import gcd
import math

def phi(n, P, Q):
    return(P-1)*(Q-1)

def finding_e(phi):
    for e in range(2, phi):
        if gcd(e, phi) == 1:
            return e


P = int(input("Введите P:"))
Q = int(input("Введите Q:"))


if isprime(P) and isprime(Q):
    n = P * Q

phi_n = phi(n, P, Q)
e = finding_e(phi_n)

d = pow(e, -1, phi_n)


print("Публичный ключ:", (n, d))
print("Приватный ключ:", (n, e))

m = int(input("Введите сообщение m:"))
m = m % n
c = pow(m, e, n)
m_dec = pow(c, d, n)

print(c)
print(m_dec)
