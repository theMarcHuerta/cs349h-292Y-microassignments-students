import numpy as np
import matplotlib.pyplot as plt
import math

class PosStochasticComputing:
    APPLY_FLIPS = False
    APPLY_SHIFTS = False

    @classmethod
    def apply_bitshift(cls, bitstream):
        if not PosStochasticComputing.APPLY_SHIFTS:
            return bitstream

        raise Exception("apply the bitshift error to the bitstream with probability 0.0001")

    @classmethod
    def apply_bitflip(self, bitstream):
        if not PosStochasticComputing.APPLY_FLIPS:
            return bitstream

        raise Exception("apply the to the bitstream with probability 0.0001")



    @classmethod
    def to_stoch(cls, prob, nbits):
        assert(prob <= 1.0 and prob >= 0.0)
        raise Exception("convert a decimal value in [0,1] to an <nbit> length bitstream.")

    @classmethod
    def stoch_add(cls, bitstream, bitstream2):
        assert(len(bitstream) == len(bitstream2))
        raise Exception("add two stochastic bitstreams together")

    @classmethod
    def stoch_mul(cls, bitstream, bitstream2):
        assert(len(bitstream) == len(bitstream2))
        raise Exception("multiply two stochastic bitstreams together")

    @classmethod
    def from_stoch(cls, result):
        raise Exception("convert a stochastic bitstream to a numerical value")

class StochasticComputingStaticAnalysis:

    def __init__(self):
        pass

    def req_length(self, smallest_value):
        raise Exception("figure out the smallest bitstream length necessary represent the input decimal value. This is also called the precision.")

    def stoch_var(self, prec):
        raise Exception("update static analysis -- the expression contains a variable with precision <prec>.")
        result_prec = None
        return result_prec


    def stoch_add(self, prec1, prec2):
        raise Exception("update static analysis -- the expression adds together two bitstreams with precisions <prec1> and <prec2> respectively.")
        result_prec = None
        return result_prec


    def stoch_mul(self, prec1, prec2):
        raise Exception("update static analysis -- the expression multiplies together two bitstreams with precisions <prec1> and <prec2> respectively.")
        result_prec = None
        return res_prec

    def get_size(self):
        raise Exception("get minimum bitstream length required by computation.")



# run a stochastic computation for ntrials trials
def run_stochastic_computation(lambd, ntrials, visualize=True, summary=True):
    results = []
    reference_value, _ = lambd()
    for i in range(ntrials):
        _,result = lambd()
        results.append(result)

    if visualize:
        nbins = math.floor(np.sqrt(ntrials))
        plt.hist(results,bins=nbins)
        plt.axvline(x=reference_value, color="red")
        plt.show()
    if summary:
        print("ref=%f" % (reference_value))
        print("mean=%f" % np.mean(results))
        print("std=%f" % np.std(results))




def PART_A_example_computation(bitstream_len):
    # expression: 0.8 * 0.4 + 0.6
    reference_value = 0.8 * 0.4 + 0.6
    w = PosStochasticComputing.to_stoch(0.8, bitstream_len)
    x = PosStochasticComputing.to_stoch(0.4, bitstream_len)
    y = PosStochasticComputing.to_stoch(0.6, bitstream_len)
    tmp = PosStochasticComputing.stoch_mul(x, w)
    result = PosStochasticComputing.stoch_add(tmp, y)
    return reference_value, PosStochasticComputing.from_stoch(result)


def PART_Y_analyze_wxb_function(precs):
    # w*x + b
    analysis = StochasticComputingStaticAnalysis()
    w_prec = analysis.stoch_var(precs["w"])
    x_prec = analysis.stoch_var(precs["x"])
    b_prec = analysis.stoch_var(precs["b"])
    res_prec = analysis.stoch_mul(w_prec, x_prec)
    analysis.stoch_add(res_prec, b_prec)
    N = analysis.get_size()
    print("best size: %d" % N)
    return N

def PART_Y_execute_wxb_function(values, N):
    # expression: w*x + b
    w = values["w"]
    x = values["x"]
    b = values["b"]
    reference_value = w*x + b
    w = PosStochasticComputing.to_stoch(w, N)
    x = PosStochasticComputing.to_stoch(x, N)
    b = PosStochasticComputing.to_stoch(b, N)
    tmp = PosStochasticComputing.stoch_mul(x, w)
    result = PosStochasticComputing.stoch_add(tmp, b)
    return reference_value, PosStochasticComputing.from_stoch(result)


def PART_Y_test_analysis():
    precs = {"x": 0.1, "b":0.1, "w":0.01}
    # apply the static analysis to the w*x+b expression, where the precision of x and b is 0.1 and
    # the precision of w is 0.01
    N_optimal = analyze_example_computation(precs)
    print("best size: %d" % N_optimal)

    variables = {}
    for _ in range(10):
        variables["x"] = round(np.random.uniform(),1)
        variables["w"] = round(np.random.uniform(),2)
        variables["b"] = round(np.random.uniform(),1)
        print(variables)
        run_stochastic_computation(lambda : execute_example_computation(variables,N_optimal), ntrials=10000, visualize=False)
        print("")


def PART_Z_execute_rng_efficient_computation(values,N,save_rngs=True):
    # expression: x*x+x
    xv = values["x"]
    reference_value = xv*xv + xv
    if save_rngs:
        x = PosStochasticComputing.to_stoch(xv, N)
        x2 = x
        x3 = x
    else:
        x = PosStochasticComputing.to_stoch(xv, N)
        x2 = PosStochasticComputing.to_stoch(xv, N)
        x3 = PosStochasticComputing.to_stoch(xv, N)

    tmp = PosStochasticComputing.stoch_mul(x, x2)
    result = PosStochasticComputing.stoch_add(tmp,x3)
    return reference_value, PosStochasticComputing.from_stoch(result)



print("---- part a: effect of length on stochastic computation ---")
ntrials = 10000
run_stochastic_computation(lambda : PART_A_example_computation(bitstream_len=10), ntrials)
run_stochastic_computation(lambda : PART_A_example_computation(bitstream_len=100), ntrials)
run_stochastic_computation(lambda : PART_A_example_computation(bitstream_len=1000), ntrials)


# Part X, introduce non-idealities
PosStochasticComputing.APPLY_FLIPS = True
PosStochasticComputing.APPLY_SHIFTS =False
print("---- part x: effect of bit flips ---")
run_stochastic_computation(lambda : PART_A_example_computation(bitstream_len=1000), ntrials)
PosStochasticComputing.APPLY_FLIPS = False
PosStochasticComputing.APPLY_SHIFTS = True
print("---- part x: effect of bit shifts ---")
run_stochastic_computation(lambda : PART_A_example_computation(bitstream_len=1000), ntrials)
PosStochasticComputing.APPLY_FLIPS = False
PosStochasticComputing.APPLY_SHIFTS =False


# Part Y, apply static analysis
print("---- part y: apply static analysis ---")
PART_Y_test_analysis()

# Part Z, resource efficent rng generation
print("---- part z: one-rng optimization ---")
run_stochastic_computation(lambda : PART_Z_execute_rng_efficient_computation(bitstream_len=1000, N=1000), ntrials)
