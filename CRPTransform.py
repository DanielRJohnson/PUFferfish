from numpy import array

def NoTransform(challenges, key):
    return challenges, key

def XorKeyTransform(challenges, key):
    arrayed_key = [bit for bit in bin(key)[2:]] # num to binary string to list with 0b cut off
    arrayed_key = [-1 if bit == '0' else 1 for bit in arrayed_key] # '0' -> -1, '1' -> 1
    return array([[ 1 if challenge[i] != arrayed_key[i] else -1 
        for i in range(len(arrayed_key))] for challenge in challenges]), key # return the xor

def TFFWithResetTransform(challenges, key):
    new_challenges = []
    for challenge in challenges:
        new_challenges.append(key)
        key = [bit if challenge[i] == -1 else _flip_bit(bit) for i, bit in enumerate(key)]
    return array(new_challenges), key

def _flip_bit(bit):
    return -1 if bit == 1 else 1

def ElipticCurveTransform(challenges, key):
    raise NotImplementedError