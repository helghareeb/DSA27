"""Lab 02"""


def classify_triangle(a, b, c):
    # Validate first, classify second.
    if a <= 0 or b <= 0 or c <= 0:
        raise ValueError('sides must be positive')
    if a + b <= c or a + c <= b or b + c <= a:
        raise ValueError('triangle inequality violated')
    # ASSUMPTION: the returned strings. Check the docstring.
    if a == b == c:
        return 'equilateral'
    if a == b or b == c or a == c:
        return 'isosceles'
    return 'scalene'


def course_result(coursework, final, attendance):
    # Rules from the course guide:
    #   attendance >= 75, final >= 30% of the final, overall >= 60%.
    # ASSUMPTION: coursework and final are both percentages (0-100) and
    # overall = 40% coursework + 60% final. Adjust to the docstring.
    if not (0 <= coursework <= 100 and 0 <= final <= 100 and 0 <= attendance <= 100):
        return 'fail'
    overall = coursework * 0.4 + final * 0.6
    if attendance < 75:
        return 'fail'
    if final < 30:
        return 'fail'
    if overall < 60:
        return 'fail'
    return 'pass'


def fizzbuzz(n):
    result = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            result.append('FizzBuzz')
        elif i % 3 == 0:
            result.append('Fizz')
        elif i % 5 == 0:
            result.append('Buzz')
        else:
            result.append(str(i))
    return result


def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def primes_below(n):
    result = []
    for k in range(2, n):
        if is_prime(k):
            result.append(k)
    return result


def first_repeated(values):
    for i in range(len(values)):
        for j in range(i):
            if values[j] == values[i]:
                return values[i]
    return None


def count_pairs(n):
    # Nested-loop version gives the same answer:
    #   count = 0
    #   for i in range(n):
    #       for j in range(i + 1, n):
    #           count += 1
    return n * (n - 1) // 2


def calculator(command):
    # Commands are 'add a b', 'sub a b', 'mul a b', or 'div a b'.
    parts = command.split()
    if len(parts) == 3:
        operation, a, b = parts
        if operation == 'add':
            return int(a) + int(b)
        if operation == 'sub':
            return int(a) - int(b)
        if operation == 'mul':
            return int(a) * int(b)
        if operation == 'div':
            return int(a) / int(b)
    raise ValueError(f'unknown command: {command!r}')


def parse_int(text, default=None):
    try:
        return int(text)
    except ValueError:
        return default


def stats(*numbers):
    # ASSUMPTION: returns (smallest, largest); empty input raises ValueError.
    if len(numbers) == 0:
        raise ValueError('stats needs at least one number')
    smallest = numbers[0]
    largest = numbers[0]
    for x in numbers:
        if x < smallest:
            smallest = x
        if x > largest:
            largest = x
    return smallest, largest


def append_to(item, target=None):
    if target is None:
        target = []
    target.append(item)
    return target


def make_multiplier(k):
    def multiply(x):
        return x * k
    return multiply


def apply_n(f, x, n):
    for _ in range(n):
        x = f(x)
    return x