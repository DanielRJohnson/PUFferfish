from os import environ
environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import matplotlib.pyplot as plt

from attacker import Attacker
from CRPTransform import NoTransform, XorKeyTransform, DoubleXorTransform, TFFWithResetTransform, ElipticCurveTransform

CRPNUMS = [100, 1000, 10000, 50000, 75000, 100000, 250000, 500000]

def main():
    notf_accuracies = []
    for N in CRPNUMS:
        notf_attacker = Attacker(NoTransform, N=N, n=64, k=5)
        notf_attacker.fit_attack()
        notf_accuracies.append(notf_attacker.attack_accuracy())
        
    xor_accuracies = []
    for N in CRPNUMS:
        xor_key_attacker = Attacker(XorKeyTransform, key=0xfedcba0987654321, N=N, n=64, k=5)
        xor_key_attacker.fit_attack()
        xor_accuracies.append(xor_key_attacker.attack_accuracy())

    double_xor_accuracies = []
    for N in CRPNUMS:
        double_xor_attacker = Attacker(DoubleXorTransform, key=0xfedcba0987654321, N=N, n=64, k=5)
        double_xor_attacker.fit_attack()
        double_xor_accuracies.append(double_xor_attacker.attack_accuracy())
    
    tf_accuracies = []
    for N in CRPNUMS:
        tff_attacker = Attacker(TFFWithResetTransform, key=[0] * 64, N=N, n=64, k=5)
        tff_attacker.fit_attack()
        tf_accuracies.append(tff_attacker.attack_accuracy())

    plot_accuracies(notf_accuracies, xor_accuracies, double_xor_accuracies, tf_accuracies)

    notf_entropy = notf_attacker.transform_entropy()
    xor_entropy = xor_key_attacker.transform_entropy()
    double_xor_entropy = double_xor_attacker.transform_entropy()
    tf_entropy = tff_attacker.transform_entropy()

    plot_entropies(notf_entropy, xor_entropy, double_xor_entropy, tf_entropy)

    print("TODO: ELIPTIC CURVE ATTACKS")

def plot_accuracies(notf_accuracies, xor_accuracies, double_xor_accuracies, tf_accuracies):
    print("accuracies:", notf_accuracies, xor_accuracies, double_xor_accuracies, tf_accuracies)
    plt.plot(notf_accuracies, label="No Transform")
    plt.plot(xor_accuracies, label="Xor Key")
    plt.plot(double_xor_accuracies, label="Double Xor")
    plt.plot(tf_accuracies, label="TFF With Reset")
    plt.xticks(list(range(len(CRPNUMS))), CRPNUMS)
    plt.xlabel("Number of CRPs")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.savefig("figs/accuracies.png")
    plt.clf()

def plot_entropies(notf_entropy, xor_entropy, double_xor_entropy, tf_entropy):
    print("entropies:", notf_entropy, xor_entropy, double_xor_entropy, tf_entropy)
    plt.bar(["No Transform", "Xor Key", "Double Xor", "TFF With Reset"], 
            [notf_entropy, xor_entropy, double_xor_entropy, tf_entropy])
    plt.ylabel("Entropy")
    plt.savefig("figs/entropies.png")
    plt.clf()

if __name__ == "__main__":
    main()