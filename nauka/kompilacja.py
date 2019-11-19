import time
import math

formulas_list = [
     "abs(x**3 - x**0.5)",
     "abs(math.sin(x) * x**2)"
     ]
result=0
argument_list = []
for i in range (100000):
    argument_list.append(i/10)
    i += 1
start=time.time()
for a in range(len(formulas_list)):
    results_list = []
    print("pracuje nad pętlą nr. {}".format(a+1))
    for b in argument_list:
        x=b
        result=eval(formulas_list[a])
        results_list.append(result)
print(results_list)
stop=time.time()
print(min(results_list), max(results_list))
print(stop-start)

start=time.time()
for a in range(len(formulas_list)):
    results_list = []
    skompilowany = compile(formulas_list[a], "wewnetrzny", "eval")
    print("pracuje nad pętlą nr. {}".format(a+1))
    for b in argument_list:
        x=b
        result=eval(skompilowany)
        results_list.append(result)
print(results_list)
stop=time.time()
print(min(results_list), max(results_list))
print(stop-start)
