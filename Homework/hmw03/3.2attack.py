import hashlib
import string
import multiprocessing
import pickle as pkl


# Define constants
BASE36_PSWDLEN = 36
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


def crack_hash(target_hash):
    with open('rainbow.txt', 'rb') as f:
        end_to_start_matching = pkl.load(f)

    for i in range(NUM_REDUCTIONS - 1, -1, -1):
        # try from all starting columns, starting from the end
        # (so i = N-1, N-2, N-3,...,0)
        h = target_hash

        for j in range(i, NUM_REDUCTIONS):
            # range j between i, i+1, i+2,...,N
            plaintext = reduction_func(h, j)
            h = hashing_func(plaintext)

            if plaintext in end_to_start_matching:
                # you found a match: go to phase 2, recompute the whole row
                # may be a false alarm.
                preimage = find_preimage(target_hash,
                                         end_to_start_matching[plaintext])
                if preimage is not None:
                    # if not a false alarm, return it.
                    return target_hash, preimage


def find_preimage(target_hash: str, start_text: str):
    # phase 2: recompute the whole row until you find your target hash
    # (or the end of the row, false alarm)
    plaintext = start_text

    for i in range(NUM_REDUCTIONS):
        h = hashing_func(plaintext)
        if h == target_hash:
            return plaintext

        plaintext = reduction_func(h, i)

    # if hash not found in chain, return
    return None


def cracking_main():
    pool = multiprocessing.Pool(processes=16)

    # Here decide the set to crack or read files of hash list
    hash_list = []

    for crack_return in pool.imap_unordered(crack_hash, hash_list, chucksize=1000):
        if crack_return is not None:
            result.append(crack_return)


if __name__ == '__main__':
    result = []
    cracking_main()
