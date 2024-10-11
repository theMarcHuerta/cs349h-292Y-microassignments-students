import numpy as np
import matplotlib.pyplot as plt
import math
from fractions import Fraction
import cv2

class PosStochasticComputing:
    APPLY_FLIPS = False
    APPLY_SHIFTS = False

    @classmethod
    def apply_bitshift(cls, bitstream):
        if not PosStochasticComputing.APPLY_SHIFTS:
            return bitstream
        n = len(bitstream)
        shifted_bitstream = np.copy(bitstream)
        for i in range(n):
            if np.random.rand() < 0.1:
                for j in range (i,n-1):
                    # Shift right just like the slides and example (unsure if we should account for a shift left)
                    shifted_bitstream[j+1] = bitstream[j]
        return shifted_bitstream
        # raise Exception("apply the bitshift error to the bitstream with probability 0.0001")

    @classmethod
    def apply_bitflip(self, bitstream):
        if not PosStochasticComputing.APPLY_FLIPS:
            return bitstream
        n = len(bitstream)
        flipped_bitstream = np.copy(bitstream)
        for i in range(n):
            if np.random.rand() < 0.0001:
                flipped_bitstream[i] = np.random.rand()
        return flipped_bitstream
        # raise Exception("apply the to the bitstream with probability 0.0001")

    @classmethod
    def to_stoch(cls, prob, nbits):
        assert(prob <= 1.0 and prob >= 0.0)
        bitstream = np.random.rand(nbits) < prob
        return bitstream.astype(int)
        # raise Exception("convert a decimal value in [0,1] to an <nbit> length bitstream.")

    @classmethod
    def stoch_add(cls, bitstream, bitstream2):
        assert(len(bitstream) == len(bitstream2))
        n = len(bitstream)
        # randomly choose
        result = [bitstream[i] if np.random.rand() < 0.5 else bitstream2[i] for i in range(n)]
        return result
        # raise Exception("add two stochastic bitstreams together")

    @classmethod
    def stoch_mul(cls, bitstream, bitstream2):
        assert(len(bitstream) == len(bitstream2))
        # & op
        result = np.logical_and(bitstream, bitstream2).astype(int)
        return result
        # raise Exception("multiply two stochastic bitstreams together")

    @classmethod
    def from_stoch(cls, result):
        return np.mean(result)
        # raise Exception("convert a stochastic bitstream to a numerical value")

class StochasticComputingStaticAnalysis:

    def __init__(self):
        self.current_precision = None
        pass

    def req_length(self, smallest_value):
        return int(math.ceil(1 / smallest_value))
        # raise Exception("figure out the smallest bitstream length necessary represent the input decimal value. This is also called the precision.")

    def stoch_var(self, prec):
        # raise Exception("update static analysis -- the expression contains a variable with precision <prec>.")
        if self.current_precision is None:
            self.current_precision = prec
        else:
            self.current_precision = min(self.current_precision, prec)
        return prec

    def stoch_add(self, prec1, prec2):
        # raise Exception("update static analysis -- the expression adds together two bitstreams with precisions <prec1> and <prec2> respectively.")
        result_prec = (prec1 + prec2) / 2.0
        # convert to a fraction with the smallest possible denominator
        fraction = Fraction(result_prec).limit_denominator()
        # get the denominator as a number
        denom = fraction.denominator
        prec_tmp = 1.0 / denom
        print(result_prec)
        self.current_precision = min(prec_tmp, result_prec)
        return result_prec

    def stoch_mul(self, prec1, prec2):
        # raise Exception("update static analysis -- the expression multiplies together two bitstreams with precisions <prec1> and <prec2> respectively.")
        result_prec = prec1 * prec2
        self.current_precision = result_prec
        return result_prec

    def get_size(self):
        # raise Exception("get minimum bitstream length required by computation.")
        return self.req_length(self.current_precision)



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
    # expression: 1/2*(0.8 * 0.4 + 0.6)
    reference_value = 1/2*(0.8 * 0.4 + 0.6)
    w = PosStochasticComputing.to_stoch(0.8, bitstream_len)
    x = PosStochasticComputing.to_stoch(0.4, bitstream_len)
    y = PosStochasticComputing.to_stoch(0.6, bitstream_len)
    tmp = PosStochasticComputing.stoch_mul(x, w)
    result = PosStochasticComputing.stoch_add(tmp, y)
    return reference_value, PosStochasticComputing.from_stoch(result)


def PART_A_example_computation_q3(bitstream_len):
    reference_value = 0.1 * 0.1 * 0.1 * 0.9 * 0.9 * 0.9
    w = PosStochasticComputing.to_stoch(0.1, bitstream_len)
    x = PosStochasticComputing.to_stoch(0.1, bitstream_len)
    z = PosStochasticComputing.to_stoch(0.1, bitstream_len)
    a = PosStochasticComputing.to_stoch(0.9, bitstream_len)
    b = PosStochasticComputing.to_stoch(0.9, bitstream_len)
    c = PosStochasticComputing.to_stoch(0.9, bitstream_len)
    final = PosStochasticComputing.stoch_mul(w, x)
    result = PosStochasticComputing.stoch_mul(final, z)
    final2 = PosStochasticComputing.stoch_mul(result, a)
    final3 = PosStochasticComputing.stoch_mul(final2, b)
    final4 = PosStochasticComputing.stoch_mul(final3, c)
    return reference_value, PosStochasticComputing.from_stoch(final4)

def PART_X_flip_computation(bitstream_len):
    # expression: 1/2*(0.8 * 0.4 + 0.6)
    reference_value = 1/2*(0.8 * 0.4 + 0.6)
    w = PosStochasticComputing.to_stoch(0.8, bitstream_len)
    w = PosStochasticComputing.apply_bitflip(w)
    x = PosStochasticComputing.to_stoch(0.4, bitstream_len)
    x = PosStochasticComputing.apply_bitflip(x)
    y = PosStochasticComputing.to_stoch(0.6, bitstream_len)
    y = PosStochasticComputing.apply_bitflip(y)
    tmp = PosStochasticComputing.stoch_mul(x, w)
    tmp = PosStochasticComputing.apply_bitflip(tmp)
    result = PosStochasticComputing.stoch_add(tmp, y)
    result = PosStochasticComputing.apply_bitflip(result)
    return reference_value, PosStochasticComputing.from_stoch(result)

def PART_X_shift_computation(bitstream_len):
    # expression: 1/2*(0.8 * 0.4 + 0.6)
    reference_value = 1/2*(0.8 * 0.4 + 0.6)
    w = PosStochasticComputing.to_stoch(0.8, bitstream_len)
    w = PosStochasticComputing.apply_bitshift(w)
    x = PosStochasticComputing.to_stoch(0.4, bitstream_len)
    x = PosStochasticComputing.apply_bitshift(x)
    y = PosStochasticComputing.to_stoch(0.6, bitstream_len)
    y = PosStochasticComputing.apply_bitshift(y)
    tmp = PosStochasticComputing.stoch_mul(x, w)
    tmp = PosStochasticComputing.apply_bitshift(tmp)
    result = PosStochasticComputing.stoch_add(tmp, y)
    result = PosStochasticComputing.apply_bitshift(result)
    return reference_value, PosStochasticComputing.from_stoch(result)

def PART_Y_analyze_wxb_function(precs):
    # 1/2*(w*x + b)
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
    # expression: 1/2*(w*x + b)
    w = values["w"]
    x = values["x"]
    b = values["b"]
    reference_value = 1/2*(w*x + b)
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
    N_optimal = PART_Y_analyze_wxb_function(precs)
    print("best size: %d" % N_optimal)

    variables = {}
    for _ in range(10):
        variables["x"] = round(np.random.uniform(),1)
        variables["w"] = round(np.random.uniform(),2)
        variables["b"] = round(np.random.uniform(),1)
        print(variables)
        run_stochastic_computation(lambda : PART_Y_execute_wxb_function(variables,N_optimal), ntrials=10000, visualize=True)
        print("")


def PART_Z_execute_rng_efficient_computation(value,N,save_rngs=True):
    # expression: 1/2*(x*x+x)
    xv = value
    reference_value = 1/2*(xv*xv + xv)
    if save_rngs:
        x = PosStochasticComputing.to_stoch(xv, N+50)
        x2 = x[25:N+25]
        x3 = x[50:N+50]
        x = x[0:N]
    else:
        x = PosStochasticComputing.to_stoch(xv, N)
        x2 = PosStochasticComputing.to_stoch(xv, N)
        x3 = PosStochasticComputing.to_stoch(xv, N)

    tmp = PosStochasticComputing.stoch_mul(x, x2)
    result = PosStochasticComputing.stoch_add(tmp,x3)
    return reference_value, PosStochasticComputing.from_stoch(result)



print("---- part a: effect of length on stochastic computation ---")
ntrials = 10000
# run_stochastic_computation(lambda : PART_A_example_computation(bitstream_len=10), ntrials)
# run_stochastic_computation(lambda : PART_A_example_computation(bitstream_len=100), ntrials)
# run_stochastic_computation(lambda : PART_A_example_computation(bitstream_len=1000), ntrials)
######## Q3 of Part A
# run_stochastic_computation(lambda : PART_A_example_computation_q3(bitstream_len=1000), ntrials)

## Part X
# run_stochastic_computation(lambda : PART_X_flip_computation(bitstream_len=10), ntrials)
# run_stochastic_computation(lambda : PART_X_flip_computation(bitstream_len=100), ntrials)
# run_stochastic_computation(lambda : PART_X_flip_computation(bitstream_len=1000), ntrials)

# run_stochastic_computation(lambda : PART_X_shift_computation(bitstream_len=10), ntrials)
# run_stochastic_computation(lambda : PART_X_shift_computation(bitstream_len=100), ntrials)
# run_stochastic_computation(lambda : PART_X_shift_computation(bitstream_len=1000), ntrials)

# Part X, introduce non-idealities
# PosStochasticComputing.APPLY_FLIPS = True
# PosStochasticComputing.APPLY_SHIFTS =False
# print("---- part x: effect of bit flips ---")
# # run_stochastic_computation(lambda : PART_A_example_computation(bitstream_len=1000), ntrials)
# PosStochasticComputing.APPLY_FLIPS = False
# PosStochasticComputing.APPLY_SHIFTS = True
# print("---- part x: effect of bit shifts ---")
# # run_stochastic_computation(lambda : PART_A_example_computation(bitstream_len=1000), ntrials)
# PosStochasticComputing.APPLY_FLIPS = False
# PosStochasticComputing.APPLY_SHIFTS =False


# Part Y, apply static analysis
# print("---- part y: apply static analysis ---")
# PART_Y_test_analysis()

# Part Z, resource efficent rng generation
# print("---- part z: one-rng optimization ---")
# for _ in range(5):
#     v = round(np.random.uniform(),1)
#     print(f"x = {v}")
#     print("running with save_rngs disabled")
#     run_stochastic_computation(lambda : PART_Z_execute_rng_efficient_computation(value=v, N=1000, save_rngs=False), ntrials)
#     print("running with save_rngs enabled")
#     run_stochastic_computation(lambda : PART_Z_execute_rng_efficient_computation(value=v, N=1000, save_rngs=True), ntrials)




##########################################################
##########################################################
################## EXTENSION/PART W ######################
##########################################################
##########################################################

def generate_checkerboard_image(size=256, num_squares=8):
    image = np.zeros((size, size), dtype=np.uint8) # square all black image (0s)
    square_size = size // num_squares
    for i in range(num_squares):
        for j in range(num_squares):
            if (i + j) % 2 == 0:
                image[i * square_size:(i + 1) * square_size, j * square_size:(j + 1) * square_size] = 255
    cv2.imwrite("checkerboard.png", image)
    print("saved as 'checkerboard.png'")

def apply_stochastic_filter(pixel_block, N):
    bitstreams = [PosStochasticComputing.to_stoch(pixel, N) for pixel in pixel_block]
    sum_bitstream = bitstreams[0]
    for i in range(1, len(bitstreams)):
        sum_bitstream = PosStochasticComputing.stoch_add(sum_bitstream, bitstreams[i])
    avg_bitstream = PosStochasticComputing.stoch_mul(sum_bitstream, PosStochasticComputing.to_stoch(1/9, N))
    return PosStochasticComputing.from_stoch(avg_bitstream)

def PART_W_image_filter(image_path, N=1000):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # normalize [0, 1]
    image_normalized = image / 255.0
    filtered_image = np.zeros_like(image_normalized)

    for i in range(1, image_normalized.shape[0] - 1):
        for j in range(1, image_normalized.shape[1] - 1):
            # Get the 3x3 neighborhood
            pixel_block = [image_normalized[i - 1, j - 1], image_normalized[i - 1, j], image_normalized[i - 1, j + 1],
                image_normalized[i, j - 1], image_normalized[i, j], image_normalized[i, j + 1],
                image_normalized[i + 1, j - 1], image_normalized[i + 1, j], image_normalized[i + 1, j + 1]]
            filtered_value = apply_stochastic_filter(pixel_block, N)
            filtered_image[i, j] = filtered_value

    # Convert the filtered image back to the [0, 255] range
    filtered_image = (filtered_image * 255).astype(np.uint8)
    cv2.imwrite("filtered_image.png", filtered_image)
    print("Filtered image saved as 'filtered_image.png'.")

generate_checkerboard_image()
# Part W, applying stochastic computing for image filtering
print("---_____ part w: stochastic image filter _____---")
PART_W_image_filter("checkerboard.png", N=256)