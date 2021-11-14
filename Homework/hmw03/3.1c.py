import hashlib
import multiprocessing


# List of all hashes to crack
hash_list = {'962642e330bd50792f647c1bf71895c5990be4ebf6b3ca60332befd732aed56c',
             '8eef79d547f7a6d6a79329be3c7035f8e377f9e629cd9756936ec233969a45a3',
             'e71067887d50ce854545afdd75d10fa80b841b98bb13272cf4be7ef0619c7dab',
             '889a22781ef9b72b7689d9982bb3e22d31b6d7cc04db7571178a4496dc5ee128',
             '6a16f9c6d9542a55c1560c65f25540672db6b6e121a6ba91ee5745dabdc4f208',
             '2317603823a03507c8d7b2970229ee267d22192b8bb8760bb5fcef2cf4c09edf',
             'c6c51f8a7319a7d0985babe1b6e4f5c329403d082e05e83d7b9d0bf55876ecdc',
             'c01304fc36655dd37b5aa8ca96d34382ed9248b87650fffcd6ec70c9342bf451',
             'cff39d9be689f0fc7725a43c3bdc7f5be012c840b9db9b547e6e3c454a076fc8',
             '662ab7be194cee762494c6d725f29ef6321519035bfb15817e84342829728891'}

# List of all salts used in passwords
salt_list = ['b9', 'be', 'bc', '72', '9f', '17', '94', '7f', '2e', '24']

# List of dicts used for cracking
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


# Multiprocessing block processing
# For each base password (a row in the dict), create hashes by all salts and see if a match exists
def salt_crack(base_pswd):
    # ensure no \n at the end of string
    base_pswd = base_pswd.replace('\n', '')

    # generate salted passwords and hash them, to see if there's a match
    for salt in salt_list:
        salt_pswd = base_pswd + salt
        h = hashlib.sha256(salt_pswd.encode()).hexdigest()

        if h in hash_list:
            print('Found match: {} -> {} (salt: {})'.format(h, base_pswd, salt))
            hash_list.remove(h)
            return base_pswd, h


# Collect all results in a list
result = []

# Iterate through all dicts to get the cracking result
for dict_name, dict_encoding in dict_list:
    print('File opening: {}'.format(dict_name))
    dict_file = open('Dicts/{}'.format(dict_name), encoding=dict_encoding)

    # define 16 processes to crack
    pool = multiprocessing.Pool(processes=16)

    # read the dictionary file by a chucksize 1000
    # feed one dict row at a time to each worker
    for crack_return in pool.imap_unordered(salt_crack, dict_file, chunksize=1000):
        if crack_return is not None:
            result.append(crack_return)

    dict_file.close()
