import concurrent.futures
 
def worker():
    print("Hi")
 
pool = concurrent.futures.ThreadPoolExecutor(max_workers=4)
 
pool.submit(worker)
# pool.submit(worker)

pool.shutdown(wait=True)