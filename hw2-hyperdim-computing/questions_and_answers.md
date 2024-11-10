### Part A: Hyperdimensional Computing [8 pts total, 2 pts / question]

**Task 1:** In `hdc.py`, implement the hypervector generation, binding, bundling, Hamming distance, and permutation operations in the scaffold code. Also, implement the `add` and `get` functions in the item memory `HDItemMem` class; these functions will be used to manage the atomic hypervectors. Based on them, implement an HD encoding procedure that encodes strings in `make_word` function. You should also implement the `make_letter_hvs` function. It should produce a codebook for the letters, which serves as the first argument for the `make_word` function. Refer to the main scripts for how these two functions are invoked in sequence.

For example "fox" would be translated to sequence ["f","o", "x"]. For simplicity, use a hypervector size of 10,000 to answer these questions unless otherwise stated.

**Q1.** Construct a HDC-based string encoding for the word "fox". How did you encode the "fox" string? How similar is the hypervector for "fox" to the hypervector for "box" in your encoding? How similar is the hypervector for "xfo"? How similar is the hypervector for "car"? Please remark on the relative similarities, not the absolute distances.

def test_make_word_unordered(letter_cb):
    hv1 = make_word_unordered(letter_cb, "fox")

All we have to do is given a codebook, we just pass it to our function to encode the word. It will fetch the hv for each letter at each positon and permute it by its positon then bind all the hvs at the end and return the result.

The similarity betwen car is non existent as it shares no letters and its reflected in the distance. The xfo one has the letters but all in differenet positions but since we bind everything and permute, it should be dissimilar from the main word. And it is. The one which should be most similar is box because it shares 2/3 letters in the same position and fox and it also is. 

**Q2.** Change your encoding so the order of the letters doesn't matter (apply the changes for this question only). What changes did you make? Please remark on the relative similarities, not the absolute distances.

I just didnt permute to make order not matter. Now the similarities should be and are all relative to the number of letters they share rather than the position with xfo being an exact match as fox. And box will be second in distance. Car is still the farthest.

-------

**Task 2:**: Implement the bit flip error helper function (`apply_bit_flips`). Then apply bit flip errors to hypervectors before the distance calculations, where the bit flip probability is 0.10. Specifically, before computing the distance between two hypervectors hv1 and hv2, you may apply the bit flip error to one of them, say hv1. Use the `monte_carlo`, `study_distributions`, and `plot_hist_distributions` helper functions to study the distribution of distances between `fox` and `box`, compared to the distance between `fox` and `car` with and without hardware error.

Fox and box were closer to being similar with no error and car and box were dissimilar. With error though, it seemed box started being less similar to fox.

**Q3.** Try modifying the hardware error rate (`perr`) with fixed hypervector size `10000`. How high can you make the hardware error until the two distributions begin to become visibly indistinguishable? What does it mean conceptually when the two distance distributions have a lot of overlap?

The became indistinguishable at 0.50. This makes sense because the error rate makes each of the vectors essentially random at 0.5 into a different vector at that point. When they have overlap it means they are just as dissimilar from the word fox but it has no correalation to each other neccesarily.

**Q4.** Try modifying the hypervector size (`SIZE`) with fixed hardware error rate `0.10`. How small can you make the word hypervectors before the two distributions begin to become visibly indistinguishable?

I pretty much had to get it down to the 5-10 range because as we shurnk the size, the distance betwen the 2 seemeed to close but then at sub 10 it basically was too random and just had a lot of overlap at the point but at 5 it was basically the same. 
-----

**Task 3:**: Next, fill out the stubs in the item memory class -- there are stubs for threshold-based (`matches`) and winner-take-all (`wta`) queries, and for computing the Hamming distances between item memory rows and the query hypervector. The item memory class will be used in later exercises to build a database data structure and an ML model.







### Part B: Item Memories [`hdc-db.py`, 10 points total, 2 pts / question]

Next, we will use this item memory to implement a database data structure; we will be performing queries against an HDC-based database populated with the digimon dataset (`digimon.csv`). The HDDatabase class implements the hyperdimensional computing-based version of this data structure, and contains stubs of convenience functions for encoding / decoding strings and database rows, as well as stubs for populating and querying the database. We will implement this class and then invoke `build_database` to build a database using the HDDatabase class. For simplicity, use a hypervector size of 10,000 to answer these questions unless otherwise stated.

_Tip_: For this exercise, map every distinct string to an atomic random hypervector. This will keep retrieval tasks relatively simple. For decoding operations, you will likely need to use the self-inverse property of binding and perform additional lookups to recover information.

---------

__Task 0__: The database data structure contains multiple rows, where each row is uniquely identified with a primary key and contains a collection of fields that are assigned to values. In the HD implmentation, the database rows are maintained in item memories, and row data is encoded as a hypervector. Decide how you want to map the database information to item memories. Implement the database row addition `add_row` function, which should invoke the `encode_row` helper function and update the appropriate item memories.

---------

__Task 1__: Implement the string and row encoding functions (`encode_string`, `encode_row`). These encoding functions accept a string and a database row (field-value map) respectively, and translate these inputs into hypervectors by applying HD operators to atomic basis vectors. Then, implement the string and row decoding functions (`decode_string`, `decode_row`) which take the hypervector representations of a string or database row respectively and reconstructs the original data. The decoding routines will likely need to perform multiple codebook / item memory lookups and use HD operator properties (e.g., unbinding) to recover the input data. Execute `digimon_test_encoding` function to test your string and row encoding routines and verify that you're able to recover information from the hypervector embedding with acceptable reliability.

**Q1.** Describe how you encoded database rows as hypervectors. Write out the HD expression you used to encode each piece of information, and describe any atomic hypervectors you introduced.

Well as recommended every string is a hypervector in a codebook. So then after I have that established, I also put the fields into their own codebook so I can later iterate through them. So what function ends up being is I get the row hypervector by bindinng all the fields with their values and then bundle all those pairs together. Then I just add it to our databased with the primary key.

I just use (f1 * v1)+(f2 * v2)...(fn * vn) where f is the field and v is the value.

**Q2.** Describe how you decoded the strings / database rows from hypervectors. Describe any HD operations you used to isolate the desired piece of information, and describe what item memory lookups you performed to recover information. If you're taking advantage of any HD operator properties to isolate information, describe how they do so.

To decode, I just do the inverse of the encode. I get the field and i unbind it from the main row hypervector. Then I wta it to get the closest match while iterating through the string codebook and I just return that value.

I just use min ( all values(((f1 * v1)+(f2 * v2)...(fn * vn) * f1))) where f is the field and v is the value and f1 is the field for which value we want.

--------

__Task 2__: Next, we'll implement routines for querying the data structure. Implement the `get_value` and `get_matches` stubs -- the `get_value` query retrieves the value assigned to a user-provided field within a record. The `get_matches` stub retrieves the rows that contain a subset of field-value pairs. Implement both these querying routines and then execute `digimon_basic_queries` and `digimon_value_queries` to test your implementations.

**Q3.** How did you implement the `get_value` query? Describe any HD operators and lookups you performed to implement this query.

For get value i just get the row and decode the row and get the field from it! Most of the operators are just in the decoded row function since it's just a slight wrapper around it.


**Q4.** How did you implement the `get_matches` query? Describe any HD operators and lookups you performed to implement this query. Try using lower threshold values. How high of a distance threshold can you set before you start seeing false positives in the returned results?

So I encode the field values as its own row. Then i can just unbind it from each row and then wta it to get the closest match same as we did before. If its below the threshold then I just add it to the matches and boom. Nothing crazy, the hardest part was getting the previous parts working but then once I did it made sense and I was able to debug this one easier. 

As for false postives, it has to get pretty close to that .5 threshold for it to be a false positive because most of the tests we'll have will be uncorrelated with our hv we're testing against but with some variance, some will be lower than .5 like around .49 or so. This was the case for the champion query. For the virus plant one since we're querryign 2 fields at a time it was lower at around .44.

-----

__Task 3__: Implement the `get_analogy` query, which given two records and a value in one of the records, identifies the value that shares the same field in the other record as the input value. For example, if you perform an `analogy` query on the `US` and `Mexico` records, and ask for the value in the `Mexico` record that relates to the `Dollar` value in the `US` record, this query would return `Peso`. This query completes the analogy  _Dollar is to USA as <result> is to Mexico_. Execute `analogy_query` to test your implementation.

_Tip_: If you want more information on this type of query, you can look up "What We Mean When We Say 'What's the Dollar of Mexico?'"

**Q5.** How did you implement the `get_analogy` query? Describe how this is implemented using HD operators and item memory lookups. Why does your implementation work? You may want to walk through and HD operator properties you leveraged to complete this query.


Well for this, at this point i have a lot of helper functions so I just make use of them. I get all the encoded dict for the target key and then loop through it til i find a match with the value and field and then I'll know thats the field I'm looking for. At which point I can just use get_value. So I really just end up making use of my helper functions to make it easy.







### Part C: Implementing an HDC Classifier [10 pts total, 2 pts/question, hdc-ml.py]

Next, we will use an item memory to implement an MNIST image classifier. A naive implementation of this classifier should easily be able to get ~75% accuracy. In literature, HDC-based MNIST classifiers have been shown to achieve ~98% classification accuracy with model size of only a few bytes while being error resilient. In this exercise, you will implement the necessary encoding/decoding routines, and you will implement both the training and inference algorithms for the classifier.

__Tips__: Try a simple pixel/image encoding first. For decoding operations, you will likely need to use the self-inverse property of binding to recover information.

-------------

**Task 1**: Fill in the `encode_pixel`, `decode_pixel`, `encode_image`, and `decode_image` stubs in the MNIST classifier. These functions should translate pixels/images to/from their hypervector representation. Then use the `test_encoding` function to evaluate the quality of your encoding. This function will save the original image to `sample0.png`, and the encoded then decoded image to `sample0_rec.png`.

**Q1.** How did you encode pixels as a hypervector? Write out the HD expressions, and describe what atomic/basis hypervectors you used for the encodings. 

I justed used black and white as the 2 atomics and then permuated based on the pixel positons. 
image = p^0*n+0(white) + ... + p^m*n+n(black)

**Q2.** How did you encode images as a hypervector? Write out the HD expressions, and describe any atomic/basis hypervectors in the expression. 

After getting each pixel encoding based on its position, i just needed to bundle them together.
(pix0) + .... + (pixN).

-----------------------

**Task 2**: Fill in the `train` and the `classify` stubs in the MNIST classifier. Test your classifier out by invoking the `test_classifier` function. What classification accuracy did you attain? 

I got 75% like right on the dot almost: accuracy=0.756250: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 800/800 [00:13<00:00, 58.02it/s]
ACCURACY: 0.756250


**Q3.** What happens to the classification accuracy when you reduce the hypervector size; how small of a size can you select before you see > 5% loss in accuracy? 

I never saw a loss of accuracy. I thought i did something wrong but i couldnt find it so maybe I'm figuring that since it just binds and essentially averages all the pixels on the image, the training data will be slightly biased still and when we find the distance over the entire image, that acts as a hyper vector in a sort itself and we can find the distance between the numbers still because of when i set the size to 1 we'd still get 28*28 hyper vector and you could think of the numbers as atomics now in a sort of way and we're just finding the distance between the hyper vectors.


**Q4.** What happens to the classification accuracy when you introduce bit flips into the item memory's distance calculation? Note that you shold only apply bit flips during inference. How much error can you introduce before you see a > 5% loss in accuracy?

When I go into the .30s range i start to see loss of less than 5% accuracy and by .4 i see 13% loss. This makes sense because the error is random and the more error we have, the more random the vectors are and the more likely they are to be misclassified.

ACCURACY: 0.638750

------------------------

**Task 3**: You can also implement a simple generative model using hyperdimensional computing. In this following exercise, we will use HDC to generate images of handwritten digits from the classifier label. Naive HD generative models are very similar to HD classifiers, and are constructed in two simple steps:

- _Constructing a Generative Model._ For each classifier label, group training data by label, and translate each datum to a hypervector. Next, generate a probability vector for each label. The probability value at position i of the probability vector is the probability that the hypervector bit in position i is a "1" bit value. The probability vector can easily be computed by summing up the M hypervectors that share the same label, and then normalizing by 1/M.

- _Generating Random Images._ To generate a random image for some label, you sample a binary hypervector from the probability hypervector for that label. You then translate the hypervector to an image using the hypervector decoding routine (`decode_image`). You can sample and bundle multiple hypervectors to average the result.

You can find a sample of generated image `sample_generated.png` for number `7` in the folder.

**Q5.** Use `test_generative_model` function to test your generative model. Include a few pictures outputted by your generative model in your submission.

Included.
