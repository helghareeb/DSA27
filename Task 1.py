"""Lab 01"""


def seconds_to_hms(seconds):
    h = seconds // 3600
    rest = seconds % 3600
    m = rest // 60
    s = rest % 60
    return f'{h}:{m:02d}:{s:02d}'


def celsius_to_fahrenheit(celsius):
    # ASSUMPTION: rounded to 1 decimal place. Check the docstring.
    return round(celsius * 9 / 5 + 32, 1)


def split_evenly(total, people):
    return total // people, total % people


def initials(full_name):
    words = full_name.split()
    result = ''
    i = 0
    while i < len(words):
        result += words[i][0].upper() + '.'
        i += 1
    return result


def is_palindrome_word(word):
    cleaned = word.strip().lower()
    return cleaned == cleaned[::-1]


def mask_email(email):
    # ASSUMPTION: keep first letter of the name, replace the rest with '*'.
    at = email.index('@')
    name = email[:at]
    domain = email[at:]
    if len(name) <= 1:
        return email
    return name[0] + '*' * (len(name) - 1) + domain


def middle(values):
    # Returns the middle element (odd length) or the two middle elements (even length).
    n = len(values)
    return values[(n - 1) // 2: n // 2 + 1]


def rotate_left(values, k):
    if len(values) == 0:
        return []
    k = k % len(values)
    return values[k:] + values[:k]


def fib_list(n):
    result = []
    a, b = 0, 1
    while len(result) < n:
        result.append(a)
        a, b = b, a + b
    return result


def collatz_steps(n):
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps