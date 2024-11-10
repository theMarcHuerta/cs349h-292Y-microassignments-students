import string
import random
import operator
import numpy as np
import tqdm
import matplotlib.pyplot as plt
from functools import reduce


class HDC:
    SIZE = 10000

    @classmethod
    def rand_vec(cls):
        return np.random.randint(2, size=cls.SIZE) #gen either 0 or 1

    @classmethod
    def dist(cls, x1, x2):
        return np.sum(x1 != x2)/cls.SIZE #hammin dis

    @classmethod
    def bind(cls, x1, x2):
        # XOR 
        return np.logical_xor(x1, x2)

    @classmethod
    def bind_all(cls, xs):
        # reduce applies the xor to all of xs one at a time
        return reduce(cls.bind, xs).astype(int)

    @classmethod
    def bundle(cls, xs):
        # adding vectors together then threshold em
        tot_sum = np.sum(xs, axis=0) # sum 
        return (tot_sum > len(xs) / 2).astype(int)

    @classmethod
    def permute(cls, x, i):
        # shift the array
        return np.roll(x, i) # had to use roll bc it wraps it around

    @classmethod
    def apply_bit_flips(cls, x, p=0.0):
        flip_mask = (np.random.random(cls.SIZE) < p).astype(int) #ran vector of 1s 0s based on p
        return np.logical_xor(x, flip_mask)


class HDItemMem:

    def __init__(self, name=None) -> None:
        self.name = name
        self.item_mem = {}
        # perbit bit flip prob
        self.ber = 0.0

    def add(self, key, hv):
        assert (hv is not None)
        self.item_mem[key] = hv

    def get(self, key):
        return self.item_mem[key]

    def has(self, key):
        return key in self.item_mem

    def distance(self, query):
        distances = {}
        for key, hv in self.item_mem.items():
            if self.ber > 0:
                hv = HDC.apply_bit_flips(hv, self.ber)
            distances[key] = HDC.dist(query, hv)
        return distances

    def all_keys(self):
        return list(self.item_mem.keys())

    def all_hvs(self):
        return list(self.item_mem.values())

    def wta(self, query):
        # Winner-take-all querying
        distances = self.distance(query)
        return min(distances, key=distances.get)

    def matches(self, query, threshold=0.49):
        # Threshold-based querying
        distances = self.distance(query)
        return [key for key, dist in distances.items() if dist / HDC.SIZE <= threshold]


# a codebook is simply an item memory that always creates a random hypervector
# when a key is added.
class HDCodebook(HDItemMem):

    def __init__(self, name=None):
        HDItemMem.__init__(self, name)

    def add(self, key):
        self.item_mem[key] = HDC.rand_vec()


def make_letter_hvs():
    alphaltrs = HDCodebook("alpha")
    for ltr in string.ascii_lowercase:
        alphaltrs.add(ltr)
    return alphaltrs


def make_word(letter_codebook, word):
    letter_hvs = [letter_codebook.get(letter) for letter in word]
    permuted_hvs = [HDC.permute(hv, i) for i, hv in enumerate(letter_hvs)]
    return HDC.bundle(permuted_hvs)


def make_word_unordered(letter_codebook, word):
    # Encode a word using the letter codebook, ignoring letter order
    letter_hvs = [letter_codebook.get(letter) for letter in word]
    return HDC.bundle(letter_hvs)


def test_make_word(letter_cb):
    hv1 = make_word(letter_cb, "fox")
    hv2 = make_word(letter_cb, "box")
    hv3 = make_word(letter_cb, "xfo")
    hv4 = make_word(letter_cb, "car")
    print(HDC.dist(hv1, hv2))
    print(HDC.dist(hv1, hv3))
    print(HDC.dist(hv1, hv4))

def test_make_word_unordered(letter_cb):
    hv1 = make_word_unordered(letter_cb, "fox")
    hv2 = make_word_unordered(letter_cb, "box")
    hv3 = make_word_unordered(letter_cb, "xfo")
    hv4 = make_word_unordered(letter_cb, "car")
    print(HDC.dist(hv1, hv2))
    print(HDC.dist(hv1, hv3))
    print(HDC.dist(hv1, hv4))



def monte_carlo(fxn, trials):
    results = list(map(lambda i: fxn(), tqdm.tqdm(range(trials))))
    return results


def plot_dist_distributions(key1, dist1, key2, dist2):
    plt.hist(dist1,
            alpha=0.75,
            label=key1)

    plt.hist(dist2,
            alpha=0.75,
            label=key2)

    plt.legend(loc='upper right')
    plt.title('Distance distribution for Two Words')
    plt.show()
    plt.clf()


def study_distributions():
    def gen_codebook_and_words(w1, w2, prob_error=0.0):
        letter_cb = make_letter_hvs()
        hv1 = make_word(letter_cb, w1)
        hv2 = make_word(letter_cb, w2)
        
        if prob_error > 0:
            hv1 = HDC.apply_bit_flips(hv1, prob_error)
        
        return HDC.dist(hv1, hv2)

    trials = 1000
    # d1 = monte_carlo(lambda: gen_codebook_and_words("fox", "box"), trials)
    # d2 = monte_carlo(lambda: gen_codebook_and_words("fox", "car"), trials)
    # plot_dist_distributions("box", d1, "car", d2)

    perr = 0.10
    d1 = monte_carlo(lambda: gen_codebook_and_words("fox", "box", prob_error=perr), trials)
    d2 = monte_carlo(lambda: gen_codebook_and_words("fox", "car", prob_error=perr), trials)
    plot_dist_distributions("box", d1, "car", d2)
    


# if __name__ == '__main__':
#     HDC.SIZE = 10000

#     letter_cb = make_letter_hvs()
#     hv1 = make_word(letter_cb, "fox")
#     hv2 = make_word(letter_cb, "box")
#     hv3 = make_word(letter_cb, "xfo")
#     hv4 = make_word(letter_cb, "car")

#     print(HDC.dist(hv1, hv2))
#     print(HDC.dist(hv1, hv3))
#     print(HDC.dist(hv1, hv4))

#     test_make_word_unordered(letter_cb)

#     study_distributions()

# letter_cb = make_letter_hvs()
# # test_make_word(letter_cb)
# # test_make_word_unordered(letter_cb)
# study_distributions()