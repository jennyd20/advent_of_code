def fib(n, cache):
    if n in cache:
        return cache[n]
    if n == 0:
        return 1
    elif n == 1:
        return 1
    else:
        value = fib(n-1, cache) + fib(n-2, cache)
        cache[n] = value
        return value

def foo(cache=None):
    if not cache:
        cache = {}
    print(f"{cache=}")
    cache["a"] = 666
    
if __name__ == "__main__":
    # print(fib(50, {}))
    foo()
    print("====")
    foo()