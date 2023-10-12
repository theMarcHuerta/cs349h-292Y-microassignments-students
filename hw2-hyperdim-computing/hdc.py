import string
import random
import operator
import numpy as np
import tqdm
import matplotlib.pyplot as plt

class HDC:
    SIZE = 10000

    @classmethod
    def rand_vec(cls):
        raise Exception("generate atomic hypervector with size HDC.SIZE") 
    
    @classmethod
    def dist(cls,x1,x2):
        raise Exception("hamming distance between hypervectors") 
    
    @classmethod
    def bind(cls,x1,x2):
        raise Exception("bind two hypervectors together") 

    @classmethod
    def bind_all(cls, xs):
        raise Exception("convenience function. bind together a list of hypervectors") 

    @classmethod
    def bundle(cls,xs):
        raise Exception("bundle together xs, a list of hypervectors") 
          

    @classmethod
    def permute(cls,x,i):
        raise Exception("permute x by i, where i can be positive or negative") 
    
    
    @classmethod
    def apply_bit_flips(cls,x,p=0.0):
        raise Exception("return a corrupted hypervector, given a per-bit bit flip probability p") 
    


class HDItemMem:

    def __init__(self,name=None) -> None:
        self.name = name
        self.item_mem = {}
        # per-bit bit flip probabilities for the  hamming distance
        self.prob_bit_flips = 0.0

    def add(self,key,hv):
        assert(not hv is None)
        self.item_mem[key] = hv
    
    def get(self,key):
        return self.item_mem[key]

    def has(self,key):
        return key in self.item_mem

    def distance(self,query):
        raise Exception("compute hamming distance between query vector and each row in item memory. Introduce bit flips if the bit flip probability is nonzero") 

    def all_keys(self):
        return list(self.item_mem.keys())


    def all_hvs(self):
        return list(self.item_mem.values())

    def wta(self,query):
        raise Exception("winner-take-all querying") 
        
    
    def matches(self,query, threshold=0.49):
        raise Exception("threshold-based querying") 
        

# a codebook is simply an item memory that always creates a random hypervector
# when a key is added.
class HDCodebook(HDItemMem):

    def __init__(self,name=None):
        HDItemMem.__init__(self,name)

    def add(self,key):
        self.item_mem[key] = HDC.rand_vec()

    

def make_letter_hvs():
    raise Exception("return a codebook of letter hypervectors") 
    
def make_word(letter_codebook, word):
    raise Exception("make a word using the letter codebook") 
    
def monte_carlo(fxn,trials):
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
    def gen_codebook_and_words(w1,w2,prob_error=0.0):
        raise Exception("encode words and compute distance") 


    trials = 1000
    d1 = monte_carlo(lambda: gen_codebook_and_words("fox","box"), trials)
    d2 = monte_carlo(lambda: gen_codebook_and_words("fox","car"), trials)
    plot_dist_distributions("box",d1,"car",d2)

    perr = 0.10
    d1 = monte_carlo(lambda: gen_codebook_and_words("fox","box", prob_error=perr), trials)
    d2 = monte_carlo(lambda: gen_codebook_and_words("fox","car", prob_error=perr), trials)
    plot_dist_distributions("box",d1,"car",d2)


if __name__ == '__main__':
    HDC.SIZE = 10000

    letter_cb = make_letter_hvs()
    hv1 = make_word(letter_cb,"fox")
    hv2 = make_word(letter_cb,"box")
    hv3 = make_word(letter_cb,"xfo")
    hv4 = make_word(letter_cb,"care")

    print(HDC.dist(hv1, hv2))
    print(HDC.dist(hv1, hv3))
    print(HDC.dist(hv1, hv4))

    study_distributions()




