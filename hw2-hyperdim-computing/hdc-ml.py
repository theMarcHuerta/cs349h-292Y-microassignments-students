from torchvision.datasets import MNIST
from torch.utils.data import Subset
import tqdm
import torch.utils
from hdc import *
import itertools
import PIL
import numpy as np

MAX = 26


class MNISTClassifier:

    def __init__(self):
        self.classifier = HDItemMem()
        self.black_hv = HDC.rand_vec()  # black
        self.white_hv = HDC.rand_vec()  # white

    def encode_coord(self, i, j):
        raise Exception("encode a coordinate in the image as a hypervector")

    def encode_pixel(self, i, j, v):
        pixel_num= i * MAX + j
        # hv based on the pixel val --0 black, 255 white
        color_hv = self.white_hv if v > 127 else self.black_hv
        return HDC.permute(color_hv, pixel_num) # permute the color hv by the pixel number

    def encode_image(self, image):
        encoded_pixels = []
        for i, j in itertools.product(range(MAX), range(MAX)):
            v = image.getpixel((i, j))
            pixel_hv = self.encode_pixel(i, j, v)
            encoded_pixels.append(pixel_hv)
        return HDC.bundle(encoded_pixels)

    def decode_pixel(self, image_hypervec, i, j):
        pixel_number = i * MAX + j
        # unpermute? the image hv by the pixel number
        unpermuted_hv = HDC.permute(image_hypervec, -pixel_number)
        black_dist = HDC.dist(unpermuted_hv, self.black_hv)
        white_dist = HDC.dist(unpermuted_hv, self.white_hv)
        return 0 if black_dist < white_dist else 255

    def decode_image(self, image_hypervec):
        im = PIL.Image.new(mode="1", size=(MAX, MAX))
        for i, j in itertools.product(range(MAX), range(MAX)):
            v = self.decode_pixel(image_hypervec, i, j)
            im.putpixel((i-1, j-1), v)
        return im

    def train(self, train_data):
        label_hvs = {label: [] for label in range(10)}

        for image, label in tqdm.tqdm(list(train_data)):
            image_hv = self.encode_image(image)
            label_hvs[label].append(image_hv)

        # Bundle all hvs for 0-9
        for label in label_hvs:
            if label_hvs[label]:
                label_hvs[label] = HDC.bundle(label_hvs[label])

        self.classifier.item_mem = label_hvs

    def classify(self, image):
        image_hv = self.encode_image(image)
        distances = self.classifier.distance(image_hv)
        label = min(distances, key=distances.get)
        dist = distances[label]
        return label, dist

    def build_gen_model(self, train_data):
        label_hvs = {label: [] for label in range(10)}

        for image, label in tqdm.tqdm(list(train_data)):
            image_hv = self.encode_image(image)
            label_hvs[label].append(image_hv)

        # for each label we bundle 
        self.gen_model = {}
        for label, hvs in label_hvs.items():
            if hvs:
                sum_hv = np.sum(hvs, axis=0)
                prob_vector = sum_hv / len(hvs)
                self.gen_model[label] = prob_vector

    def generate(self, cat, trials=10, threshold=0.35):
        trained_model = self.gen_model[cat]
        sampled_hvs = []

        for _ in range(trials):
            # Sample a binary hypervector based on the p vector
            # here we create a random hv and compare it to the trained hv
            sampled_hv = (np.random.rand(len(trained_model)) < trained_model).astype(int)
            sampled_hvs.append(sampled_hv)

        # Average the sampled hv
        avg_hv = np.mean(sampled_hvs, axis=0)
        # Convert the averaged hypervector to binary with a lower threshold
        # I found 0.35 to be pretty good for generation 
        avg_hv = (avg_hv > threshold).astype(int)
        return self.decode_image(avg_hv)


def initialize(N=1000):
    alldata = MNIST(root='data', train=True, download=True)
    dataset = list(map(lambda datum: (datum[0].convert("1"), datum[1]),  \
                Subset(alldata, range(N))))

    train_data, test_data = torch.utils.data.random_split(dataset, [0.6, 0.4])
    HDC.SIZE = 10000
    classifier = MNISTClassifier()
    return train_data, test_data, classifier


def test_encoding():
    train_data, test_data, classifier = initialize()
    image0, _ = train_data[0]
    hv_image0 = classifier.encode_image(image0)
    result = classifier.decode_image(hv_image0)
    image0.save("sample0.png")
    result.save("sample0_rec.png")


def test_classifier():
    train_data, test_data, classifier = initialize(2000)

    print("======= training classifier =====")
    classifier.train(train_data)

    print("======= testing classifier =====")
    correct, count = 0, 0
    for image, category in (pbar := tqdm.tqdm(test_data)):
        cat, dist = classifier.classify(image)
        if cat == category:
            correct += 1
        count += 1

        pbar.set_description("accuracy=%f" % (float(correct)/count))

    print("ACCURACY: %f" % (float(correct)/count))

def test_generative_model():
    train_data, test_data, classifier = initialize(1000)
    print("======= building generative model =====")
    classifier.build_gen_model(train_data)

    print("======= generate images =====")
    while True:
        cat = random.randint(0, 9)
        img = classifier.generate(cat)
        print("generated image for class %d" % cat)
        img.save("generated.png")
        input("press any key to generate new image..")


if __name__ == '__main__':
    # test_encoding()
    # test_classifier()
    test_generative_model()
