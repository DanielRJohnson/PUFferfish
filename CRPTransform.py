from numpy import array

def NoTransform(challenges, key):
    return challenges, key

def XorKeyTransform(challenges, key):
    arrayed_key = [-1 if bit == '0' else 1 for bit in bin(key)[2:]] # '0' -> -1, '1' -> 1, 0b cut off
    return array([[ 1 if challenge[i] != arrayed_key[i] else -1 
        for i in range(len(arrayed_key))] for challenge in challenges]), key # return the xor

def DoubleXorTransform(challenges, key):
    arrayed_key = [-1 if bit == '0' else 1 for bit in bin(key)[2:]] # '0' -> -1, '1' -> 1, 0b cut off
    first = arrayed_key[:len(arrayed_key)//2] * 2
    second = arrayed_key[len(arrayed_key)//2:] * 2
    assert len(first) == len(second) == len(challenges[0])

    for k in [first, second]:
        challenges = array([[ 1 if challenge[i] != k[i] else -1 
                        for i in range(len(k))] for challenge in challenges])

    return challenges, key # return the xor

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