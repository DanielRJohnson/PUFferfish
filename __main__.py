from os import environ
environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from attacker import Attacker
from CRPTransform import NoTransform, XorKeyTransform, TFFWithResetTransform, ElipticCurveTransform

def main():
    notf_attacker = Attacker(NoTransform, N=500000, n=64, k=5)
    notf_attacker.fit_attack()
    print("no transform attack similarity:", notf_attacker.attack_similarity())
    print("no transform attack accuracy:", notf_attacker.attack_accuracy())
    print("no transform attack entropy:", notf_attacker.transform_entropy())

    xor_key_attacker = Attacker(XorKeyTransform, key=0x9284758302857311, N=500000, n=64, k=5)
    xor_key_attacker.fit_attack()
    print("xor key transform attack similarity:", xor_key_attacker.attack_similarity())
    print("xor key transform attack accuracy:", xor_key_attacker.attack_accuracy())
    print("xor key transform attack entropy:", xor_key_attacker.transform_entropy())

    tff_attacker = Attacker(TFFWithResetTransform, key=[0] * 64, N=500000, n=64, k=5)
    tff_attacker.fit_attack()
    print("tff with reset transform attack similarity:", tff_attacker.attack_similarity())
    print("tff with reset transform attack accuracy:", tff_attacker.attack_accuracy())
    print("tff with reset transform attack entropy:", tff_attacker.transform_entropy())

    print("TODO: ELIPTIC CURVE ATTACKS")


if __name__ == "__main__":
    main()