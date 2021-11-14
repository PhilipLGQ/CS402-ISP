import hashlib
import itertools
import multiprocessing

# List of all hashes to crack
hash_list = {'2e41f7133fd134335f566736c03cc02621a03a4d21954c3bec6a1f2807e87b8a',
             '7987d2f5f930524a31e0716314c2710c89ae849b4e51a563be67c82344bcc8da',
             '076f8c265a856303ac6ae57539140e88a3cbce2a2197b872ba6894132ccf92fb',
             'b1ea522fd21e8fe242136488428b8604b83acea430d6fcd36159973f48b1102e',
             '3992b888e772681224099302a5eeb6f8cf27530f7510f0cce1f26e79fdf8ea21',
             '326e90c0d2e7073d578976d120a4071f83ce6b7bc89c16ecb215d99b3d51a29b',
             '269398301262810bdf542150a2c1b81ffe0e1282856058a0e26bda91512cfdc4',
             '4fbee71939b9a46db36a3b0feb3d04668692fa020d30909c12b6e00c2d902c31',
             '55c5a78379afce32da9d633ffe6a7a58fa06f9bbe66ba82af61838be400d624e',
             '5106610b8ac6bc9da787a89bf577e888bce9c07e09e6caaf780d2288c3ec1f0c',}


# List of all dictionaries and their encoding method
dict_list = [("500-worst-passwords.txt", "utf-8"),
             ("alypaa.txt", "utf-8"),
             ("cain.txt", "utf-8"),
             ("carders.cc.txt", "latin-1"),
             ("conficker.txt", "utf-8"),
             ("english.txt", "utf-8"),
             ("elitehacker.txt", "utf-8"),
             ("facebook-pastebay.txt", "utf-8"),
             ("facebook-phished.txt", "latin-1"),
             ("faithwriters.txt", "utf-8"),
             ("file-locations.txt", "utf-8"),
             ("fuzzing-strings.txt", "utf-8"),
             ("german.txt", "latin-1"),
             ("hak5.txt", "utf-8"),
             ("honeynet.txt", "latin-1"),
             ("hotmail.txt", "utf-8"),
             ("john.txt", "utf-8"),
             ("phpbb.txt", "latin-1"),
             ("phpmyadmin-locations.txt", "latin-1"),
             ("singles.org.txt", "utf-8"),
             ("tuscl.txt", "latin-1"),
             ("twitter-banned.txt", "utf-8"),
             ("us_cities.txt", "utf-8"),
             ("web-extensions.txt", "utf-8"),
             ("web-mutations.txt", "utf-8"),
             ("rockyou.txt", "latin-1"),
             ("crackstation.txt", "latin-1")]


# Define all common modifications
# Capitalize the first letter comes after a digit
def capitalize(pswd: str):
    return pswd.title()


# Change 'e' to '3'
def r_e_3(pswd: str):
    return pswd.replace('e', '3')


# Change 'o' to '0':
def r_o_0(pswd: str):
    return pswd.replace('o', '0')


# Change 'i' to '1':
def r_i_1(pswd: str):
    return pswd.replace('i', '1')


# Define all possible modified combinations
modif_list = [capitalize, r_e_3, r_o_0, r_i_1]
modif_combination = set()

for idx in range(1, len(modif_list)+1):
    # return and collect all possible modified combinations
    # with idx length permutations of elements in the modif_list
    for modif_comb in itertools.permutations(modif_list, idx):
        modif_combination.add(modif_comb)


# Multiprocessing block function
# For one base password combination, try all possible modifications and their hashes to crack
def modif_crack(base_pswd):
    # directly return if no hash to crack
    if len(hash_list) == 0:
        return

    # ensure no \n at the end of string
    base_pswd = base_pswd.replace('\n', '')

    # collect all possible modified combinations of base_pswd
    all_pswd = {base_pswd}
    # loop through all set of modifications
    for comb in modif_combination:
        base_pswd_temp = base_pswd

        # apply the modifications to the baseline password iteratively
        for modif in comb:
            base_pswd_temp = modif(base_pswd_temp)

        # collect all possibilities to a set to prevent duplications
        all_pswd.add(base_pswd_temp)

    # hash all possible combinations and see if there's a match
    # return base password and its hash
    for pswd in all_pswd:
        h = hashlib.sha256(pswd.encode()).hexdigest()
        if h in hash_list:
            print('Found match: {} -> {} (from base password: {})'.format(h, pswd, base_pswd))
            hash_list.remove(h)
            return base_pswd, h

# Collect all cracking result by a list
result = []

# Cracking through iterating through all dictionaries
for dict_name, dict_encoding in dict_list:
    print('File opening: {}'.format(dict_name))
    dict_file = open('Dicts/{}'.format(dict_name), encoding=dict_encoding)

    # define 16 processes to crack
    pool = multiprocessing.Pool(processes=16)

    # read the dictionary file by a chucksize 1000
    # feed one dict row at a time to each worker
    for crack_return in pool.imap_unordered(modif_crack, dict_file, chunksize=1000):
        if crack_return is not None:
            result.append(crack_return)

    dict_file.close()
