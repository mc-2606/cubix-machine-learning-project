MAX_TERM = 2
FIRST_TERM = 0
SECOND_TERM = 1

def fib(first_term, second_term, max_term):
    # n time complexity

    if max_term == 0:
        return first_term
    else:
        return fib(second_term, first_term+second_term, max_term-1)

def fib_it(first_term, second_term, max_term):
    # n time complexity

    for _ in range(max_term):
        temp = second_term
        second_term = first_term+second_term

        first_term = temp
    
    return first_term

print(fib_it(0, 1, MAX_TERM))
print(fib(0, 1, MAX_TERM))

def factorial(term):
    # n time complexity

    if term == 1:
        return term
    else:
        return factorial(term-1) * term


def factorial_it(term):
    # n time complexity

    out = 1

    for new_term in range(term, 1, -1):
        out *= new_term

    return out
    
print(factorial(MAX_TERM))
print(factorial_it(MAX_TERM))