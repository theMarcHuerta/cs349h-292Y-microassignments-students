### Part A: Hyperdimensional Computing [8 pts total, 2 pts / question]

**Task 1:** Implement the hypervector generation, binding, bundling, Hamming distance, and permutation operations in the scaffold code, and then implement an HD encoding procedure that encodes strings. Also, implement the `add` and `get` functions in the item memory memory class; these functions will be used to manage the atomic hypervectors. 

For example "fox" would be translated to sequence ["f","o", "x"]. For simplicity, use a hypervector size of 10,000 to answer these questions unless otherwise stated.

**Q1.** Construct a HDC-based string for the word "fox". How did you encode the "fox" string? How similar is the hypervector for "fox" to the hypervector for "box" in your encoding? How similar is the hypervector for "xfo"? How similar is the hypervector for "car"? Please remark on the relative similarities, not the absolute distances.

**Q2.** Change your encoding so the order of the letters doesn't matter. What changes did you make? Please remark on the relative similarities, not the absolute distances.

-------

**Task 2**: Implement the bit flip error helper function (`apply_bit_flips`). Then apply bit flip errors to hypervectors before they are stored in item memory, where the bit flip probability is 0.01. Use the `monte_carlo`, `study_distributions`, and `plot_hist_distributions` helper functions to study the distribution of distances between `fox` and `box`, compared to the distance between `fox` and `car` with and without hardware error.

**Q3.** Try modifying the hardware error rate (`perr`). How high can you make the hardware error until the two distributions begin to become visibly indistinguishable? What does it mean conceptually when the two distance distributions have a lot of overlap?

**Q4.** Try modifying the hypervector size (`SIZE`). How small can you make the word hypervectors before the two distributions begin to become visibly indistinguishable?

-----

**Task 3**: Next, fill out the stubs in the item memory class -- there are stubs for threshold-based and winner-take-all queries, and for computing the Hamming distances between item memory rows and the query hypervector. The item memory class will be used in later exercises to build a database data structure and an ML model. 

### Part B: Item Memories [`hdc-db.py`, 10 points total, 2 pts / question]

Next, we will use this item memory to implement a database data structure; we will be performing queries against an HDC-based database populated with the digimon dataset (`digimon.csv`). The HDDatabase class implements the hyperdimensional computing-based version of this data structure, and contains stubs of convenience functions for encoding / decoding strings and database rows, as well as stubs for populating and querying the database. We will implement this class and then invoke `build_database` to build a database using the HDDatabase class. For simplicity, use a hypervector size of 10,000 to answer these questions unless otherwise stated.

_Tip_: For this exercise, map every string to an atomic hypervector. This will keep retrieval tasks relatively simple. For decoding operations, you will likely need to use the self-inverse property of binding and perform additional lookups to recover information.

---------

__Task 0__: The database data structure contains multiple rows, where each row is uniquely identified with a primary key and contains a collection of fields that are assigned to values. In the HD implmentation, the database rows are maintained in item memories, and row data is encoded as a hypervector. Decide how you want to map the database information to item memories. Implement the database row addition `add_row` function, which should invoke the `encode_row` helper function and update the appropriate item memories.

---------

__Task 1__: Implement the string and row encoding functions (`encode_string`, `encode_row`). These encoding functions accept a string and a database row (field-value map) respectively, and translate these inputs into hypervectors by applying HD operators to atomic basis vectors. Then, implement the string and row decoding functions (`decode_string`, `decode_row`) which take the hypervector representations of a string or database row respectively and reconstructs the original data. The decoding routines will likely need to perform multiple codebook / item memory lookups and use HD operator properties (e.g., unbinding) to recover the input data. Execute `digimon_test_encoding` function to test your string and row encoding routines and verify that you're able to recover information from the hypervector embedding with acceptable reliability.

**Q1.** Describe how you encoded strings / database rows as hypervectors. Write out the HD expression you used to encode each piece of information, and describe any atomic hypervectors you introduced.

**Q2.** Describe how you decoded the strings / database rows from hypervectors. Describe any HD operations you used to isolate the desired piece of information, and describe what item memory lookups you performed to recover information. If you're taking advantage of any HD operator properties to isolate information, describe how they do so.

--------

__Task 2__: Next, we'll implement routines for querying the data structure. Implement the `get_value` and `get_matches` stubs -- the `get_value` query retrieves the value assigned to a user-provided field within a record. The `get_matches` stub retrieves the rows that contain a subset of field-value pairs. Implement both these querying routines and then execute `digimon_basic_queries` and `digimon_value_queries` to test your implementations.

**Q3.** How did you implement the `get_value` query? Describe any HD operators and lookups you performed to implement this query.

**Q4.** How did you implement the `get_matches` query? Describe any HD operators and lookups you performed to implement this query. Try using lower threshold values. How low of a distance threshold can you set before you start seeing false positives in the returned results? 

-----

__Task 3__: Implement the `get_analogy` query, which given two records and a value in one of the records, identifies the value that shares the same field in the other record as the input value. For example, if you perform an `analogy` query on the `US` and `Mexico` records, and ask for the value in the `Mexico` record that relates to the `Dollar` value in the `US` record, this query would return `Peso`. This query completes the analogy  _Dollar is to USA as <result> is to Mexico_.

_Tip_: If you want more information on this type of query, you can look up "What We Mean When We Say 'What's the Dollar of Mexico?'"

**Q5.** How did you implement the `get_analogy` query? Describe how this is implemented using HD operators and item memory lookups. Why does your implementation work? You may want to walk through and HD operator properties you leveraged to complete this query.

### Part C: Implementing an HDC Classifier [10 pts total, 2 pts/question, hdc-ml.py]

Next, we will use an item memory to implement an MNIST image classifier. A naive implementation of this classifier should easily be able to get ~75% accuracy. In literature, HDC-based MNIST classifiers have been shown to achieve ~98% classification accuracy while being much more lightweight and error resilient than neural networks. In this exercise, you will implement the necessary encoding/decoding routines, and you will implement both the training and inference algorithms for the classifier. 

__Tips__: Try a simple pixel/image encoding first. For decoding operations, you will likely need to use the self-inverse property of binding to recover information.

-------------

**Task 1**: Fill in the `encode_pixel`, `decode_pixel`, `encode_image`, and `decode_image` stubs in the MNIST classifier. These functions should translate pixels/images to/from their hypervector representation. Then use the `test_encoding` function to evaluate the quality of your encoding. This function will save the original image to `sample0.png`, and the encoded then decoded image to `sample0_rec.png`.

**Q1.** How did you encode pixels as a hypervector? Write out the HD expressions, and describe what atomic/basis hypervectors you used for the encodings. 

**Q2.** How did you encode images as a hypervector? Write out the HD expressions, and describe any atomic/basis hypervectors in the expression. 

-----------------------

**Task 2**: Fill in the `train` and the `classify` stubs in the MNIST classifier. Test your classifier out by invoking the `test_classifier` function. What classification accuracy did you attain? 

**Q3.** What happens to the classification accuracy when you reduce the hypervector size; how small of a size can you select before you see > 5% loss in accuracy? 

**Q4.** What happens to the classification accuracy when you introduce bit flips into the item memory's distance calculation? How much error can you introduce before you see a > 5% loss in accuracy?

------------------------

**Task 3**: You can also implement a generative model using hyperdimensional computing. In this following exercise, we will use HDC to generate images of handwritten digits from the classifier label. Naive HD generative models are very similar to HD classifiers, and are constructed in two simple steps:

- _Constructing a Generative Model._ For each classifier label, group training data by label, and translate each datum to a hypervector. Next, generate a probability vector for each label. The probability value at position i of the probability vector is the probability that the hypervector bit in position i is a "1" bit value. The probability vector can easily be computed by summing up the M hypervectors that share the same label, and then normalizing by 1/M.

- _Generating Random Images._ To generate a random image for some label, you sample a binary hypervector from the probability hypervector for that label. You then translate the hypervector to an image using the hypervector decoding routine (`decode_image`). You can sample and bundle multiple hypervectors to average the result.

**Q5.** Include a few pictures outputted by your generative model in your submission.
