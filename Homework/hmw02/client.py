import hashlib

import websockets
import asyncio
import os
from hashlib import sha256


async def PAKE():
    # Provided constants
    EMAIL = "guanqun.liu@epfl.ch"
    PASSWORD = "correct horse battery staple"
    NUM_LENGTH = 32
    H = sha256
    N = int('EEAF0AB9ADB38DD69C33F80AFA8FC5E86072618775FF3C0B9EA2314C9C256576D674DF7496EA81D3383B4813D692C6E0E0D5'
            'D8E250B98BE48E495C1D6089DAD15DC7D7B46154D6B6CE8EF4AD69B15D4982559B297BCF1885C529F566660E57EC68EDBC3C'
            '05726CC02FD4CBF4976EAA9AFD5138FE8376435B9FC61D2FC0EB06E3', 16)
    g = 2

    # set uri of websocket
    uri = 'ws://127.0.0.1:5000/'

    async with websockets.connect(uri) as websocket:
        # send email to server
        await websocket.send(EMAIL)

        # wait to receive the salt in hex form, convert it to binary
        salt_hex = await websocket.recv()
        salt_int = int(salt_hex, 16)
        salt_bin = format(salt_int, 'x').encode()

        # generate a random a and send A = (g ^ a & N)
        a = int.from_bytes(os.urandom(NUM_LENGTH), 'big')
        A = pow(g, a, N)
        A_hex = format(A, 'x').encode()
        await websocket.send(A_hex)

        # wait B
        B_hex = await websocket.recv()
        B = int(B_hex, 16)

        # create U = hash(A||B)
        hash = hashlib.sha256()
        hash.update(format(A, 'x').encode())
        hash.update(format(B, 'x').encode())
        U_hex = hash.hexdigest()
        U = int(U_hex, 16)

        # compute the inner hash = H(U || ":" || PASSWORD)
        inner_hash = hashlib.sha256()
        inner_hash.update(EMAIL.encode())
        inner_hash.update(b':')
        inner_hash.update(PASSWORD.encode())
        inner_hex = inner_hash.hexdigest()

        # compute the outer hash by inner hash, get x = H(salt || inner_hash)
        outer_hash = hashlib.sha256()
        outer_hash.update(salt_bin)
        outer_hash.update(inner_hex.encode())
        x = int(outer_hash.hexdigest(), 16)

        # compute secret S
        S = pow(B - pow(g, x), (a + U * x), N)

        # finally we verify client has the same secret as the server
        # by sending H(A || B || S) to the server and receive response from the server
        secret_hash = hashlib.sha256()
        secret_hash.update(format(A, 'x').encode())
        secret_hash.update(format(B, 'x').encode())
        secret_hash.update(format(S, 'x').encode())
        await websocket.send(secret_hash.hexdigest().encode())

        resp = await websocket.recv()
        print('The response is: {}'.format(resp))

asyncio.get_event_loop().run_until_complete(PAKE())