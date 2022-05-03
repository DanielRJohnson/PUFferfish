from pypuf.simulation import XORArbiterPUF
from pypuf.io import ChallengeResponseSet, random_inputs
from pypuf_local.attack.mlp2021 import MLPAttack2021
from pypuf.metrics import similarity, accuracy
from scipy.stats import entropy
from numpy import array

class Attacker:
    def __init__(self, transform, key=None, N: int = 500000, n: int = 64, k: int = 5):
        self.puf = XORArbiterPUF(n, k, seed=10)
        self.transform = transform
        self.key = key
        self.N = N
        self.model = None # gets set in fit_attack

    def fit_attack(self):
        challenges = random_inputs(self.puf.challenge_length, self.N, seed=21)
        tf_challenges, self.key = self._transform(challenges)
        responses = self.puf.r_eval(1, tf_challenges)
        attacker_crps = ChallengeResponseSet(challenges, responses)
        attack = MLPAttack2021(
            attacker_crps, seed=3, net=[2 ** 4, 2 ** 5, 2 ** 4],
            epochs=30, lr=.001, bs=1000, early_stop=0
        )
        attack.fit()
        self.model = attack.model

    def attack_similarity(self):
        assert self.model is not None, "model not fitted"
        return similarity(self.puf, self.model, seed=42)

    def attack_accuracy(self):
        assert self.model is not None, "model not fitted"
        new_challenges = random_inputs(self.puf.challenge_length, self.N, seed=84)
        new_tf_challenges, self.key = self._transform(new_challenges)
        new_responses = self.puf.r_eval(1, new_tf_challenges)
        new_crps = ChallengeResponseSet(new_challenges, new_responses)
        return accuracy(self.model, new_crps)

    def transform_entropy(self):
        new_challenges = random_inputs(self.puf.challenge_length, self.N, seed=168)
        new_challenges_bin = array([[1 if bit == 1 else 1e-20 for bit in challenge] for challenge in new_challenges])
        new_tf_challenges, self.key = self._transform(new_challenges)
        new_tf_bin = array([[1 if bit == 1 else 1e-20 for bit in challenge] for challenge in new_tf_challenges])
        return entropy(new_challenges_bin.flatten(), qk=new_tf_bin.flatten(), base=2)

    def _transform(self, challenges):
        return self.transform(challenges, self.key)
