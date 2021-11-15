import string
import hashlib
import pickle as pkl

# Define the length for base36 passwords
BASE36_PSWDLEN = 8

# Define number of rows and to build the rainbow table
NUM_ROWS = 100000
NUM_REDUCTIONS = 100

# Define the hashing function for rainbow table, return hex form of string
def hashing_func(text: str):
    return hashlib.sha256(text.encode()).hexdigest()


# Apply reduction function: hex to base36(a-z & 0-9)
def reduction_func(hash: str, idx_col: int):
    # change hash to int, add number of columns to it
    hash_int_col = int(hash, 16) + idx_col

    # define the base36(a-z & 0-9) string
    base36_char = string.ascii_lowercase + string.digits

    # string to collect the base36 reduction result
    base36_pswd = ''

    # loop to calculate the base36 password of length 8
    while len(base36_pswd) < BASE36_PSWDLEN:
        base36_pswd = base36_pswd + base36_char[hash_int_col % len(base36_char)]
        hash_int_col = hash_int_col // len(base36_char)

    return base36_pswd


# build the rainbow table
def build():
    end_to_start_matching = dict()

    for row_num in range(NUM_ROWS):
        init_plaintext = reduction_func(hex(row_num), 0)
        plaintext = init_plaintext

        for i in range(NUM_REDUCTIONS):
            h = hashing_func(plaintext)
            plaintext = reduction_func(h, i)

        end_to_start_matching[plaintext] = init_plaintext

        print('Row {} reduction finished.'.format(row_num))

        with open('rainbow.txt', 'wb') as f:  # mode "wb" is important
            pkl.dump(end_to_start_matching, f)


if __name__ == '__main__':
    build()
