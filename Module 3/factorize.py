import multiprocessing
import time

def find_divisors(number):
    divisors = []
    for divisor in range(1, number + 1):
        if number % divisor == 0:
            divisors.append(divisor)
    return divisors

def factorize_sequential(*numbers):
    results = []
    for number in numbers:
        results.append(find_divisors(number))
    return results


def factorize_parallel(*numbers):
    cpu_cores = multiprocessing.cpu_count()
    print(f"Aviable cores: {cpu_cores}")
    with multiprocessing.Pool(cpu_cores) as pool:
        results = pool.map(find_divisors,numbers)
    return results


if __name__ == "__main__":
    numbers = [10**4, 10**5, 10**6, 10**7, 10**8, 10**9]
    start_time = time.time()
    sequential_results = factorize_sequential(*numbers)
    sequential_time = time.time() - start_time
    print(f"Sequential time: {sequential_time}")
    
    start_time = time.time()
    parallel_results = factorize_parallel(*numbers)
    parallel_time = time.time() - start_time
    print(f"Paralell time: {parallel_time}")
    