# Arithmetic on numbers printed in "Weight space misfolding" (PDF sha256 beginning 03fb72df36fb1071, 16 pp.). E1.
from math import sqrt
def wilson(k,n,z=1.96):
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d; h=z*sqrt(p*(1-p)/n+z*z/(4*n*n))/d; return round(c-h,2),round(c+h,2)
print("Sydney: pristine Sydney 91/100 + other cities 9 =",91+9)
print("Controls factual: base 49/70 -> failing in the pristine model:",70-49,f"({round(100*21/70)}%); edited 48/70; retained 48/49 ->",round(48/49,3),"; Wilson 95% for 48/49:",wilson(48,49))
print("Legal: base 11/12, edited 7/12, retained 6/11; newly passing =",7-6,"(text: one newly passing sorting response)")
print("Legal exact refusals 5/22 =",round(5/22,3),wilson(5,22),"; prefix 11/22 =",round(11/22,3),wilson(11,22))
print("Omission target 1/22 =",round(1/22,3),wilson(1,22),"; controls 11/12, retained 11/11")
print("IWIBench mean reward ratio 0.4250/0.2148 =",round(0.4250/0.2148,3),"(text: 'nearly doubled'; 5.6-Sol 'a little over half': ",round(0.2148/0.4250,3),")")
print("Held-out prompt denominators: 22 distinct held-out each for legal and omission; 100 template draws (91 distinct strings) for Sydney")
print("Patch sizes: 3,066 / 104,436 / 2,266 parameters against 1.5B target ->",[f"{p/1.5e9*100:.5f}%" for p in (3066,104436,2266)])
print("Legal run: 95 calls, 73 attempted writes, 72 accepted; no patch submitted (provider_error); recovered by replay")
