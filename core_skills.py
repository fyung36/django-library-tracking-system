import random
rand_list = [random.randint(1, 50) for _ in range(20)]

list_comprehension_below_10 = [num for num in rand_list if num < 10]

list_comprehension_below_10_with_filter = list(filter(lambda X: X <10,rand_list))