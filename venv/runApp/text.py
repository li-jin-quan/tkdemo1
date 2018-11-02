import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Executor
def sayHello(a):
    print("say hello:"+a)
start = time.time()
with ProcessPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(sayHello, "1"))
print
'results: %s' % results
end = time.time()
print
'Took %.3f seconds.' % (end - start)
