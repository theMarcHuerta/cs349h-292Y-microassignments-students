#### Part A: Stochastic Computing [2 pt/question, 8 points]

The provided scaffold code runs 10,000 trials of the `1/2*(0.8*0.4 + 0.6)` stochastic computation and plots the distribution of results. The `PART_A_example_computation` function executes the above numeric expression, and the `run_stochastic_computation` runs a stochastic computation for <ntrials> trials and plots the distribution + reports the mean and standard deviation of the stochastic executions. The vertical red line shows the expected result. Currently, the stochastic computing operations and value-to-bitstream / bitstream-to-value conversion routines are not implemented. 

Implement the stochastic computing paradigm by filling in the function stubs in the PosStochComputing class. Don't worry about supporting negative numbers just yet.

<!-- - `to_stoch` : convert a value in [0,1] to a stochastic bitstream. -->
<!-- - `from_stoch`: convert a stochastic bitstream to a numerical value -->
<!-- - `stoch_add`: perform scaled addition over two stochastic bitstreams. -->
<!-- - `stoch_mul`: perform multiplication over two stochastic bitstreams. -->

Execute the stochastic computation for bitstream lengths 10, 100, and 1000 with `stochastic.py`, and answer the following questions.

Q1. How does the mean change with increasing bitstream length? How does the variance change?

The mean actually stay surprisingly accurate! The variance just gets vastly smaller as bitstream length increases.

Q2. What is the smallest representable numeric value in 1000-bit stochastic bitstream? What happens when you try to generate a bitstream for this value -- do the bitstream values converge to the desired value?

1/1000 is the smallest. Yea they'll still form a good distrubution except since there's no space for variance below 0/1000, it will also have a bunch of results be 0 almost as much as it is 1/1000.

Q3. Using what you leaned from the analysis in (Q2), design a stochastic computation that produces an incorrect result for bitstreams with a length n=1000. You must accomplish this with stochastic operations, all values must be >= 0.1 and every constant must be a uniquely generated bitstream. What is the smallest bitstream length for the stochastic computation you come up with to produce the correct result?

Ok so if I try to represent 1/1000, about half the time it will be 0. So if I multiply 0.1 * 0.1 * 0.1 I get 1/1000. So that's pretty inaccurate. Having a bitstream of length 2000 would produce a more accurate result. Any value between 0 and 1/1000 that I try to get out will give me just 0 a lot of the time.

Q4. What stochastic bitstream length L do we need to represent a value V, assuming V is in [0,1] and V != 0? Write the equation.

It'd just be the precison of the lowest decimal place number and use that to divide 1. So .00453 would be 1/0.00003.

#### Part X: Non-Idealities Stochastic Computing [2 pt/question, 4 points]

Next, we'll experiment with introducing non-idealities into the stochastic computation `1/2*(0.8*0.4 + 0.6)`. We will introduce two kinds of non-idealities:

- bit-shift errors: this class of errors result from timing issues in circuits. This non-ideality causes one bitstream to lag behind the other during computation. For example, a bit shift error at index 1 of a bit stream would transform some stream 00101 to 00010 (the 0 at index 1 is replicated). We do not consider the case where more than one bit shift occurs at the same index, as it is unlikely to happen in practice.

- bit-flip errors: this class of errors result from bit flips in storage elements, or in the computational circuit. This non-ideality introduces bit flips in bitstreams. For example, a bit flip error at index 1 of a bit stream would transform some stream 00101 to 01101.

Fill in the `apply_bitshift` and `apply_bitflip` functions in the stochastic computing class and apply these non-idealities at the appropriate points in the stochastic computing model. Make sure these non-idealities are only enabled for this section of the homework.

Q1. What happens to the computational results when you introduce a per-bit bit-flip error probability of 0.0001? What happens when the per-bit bit flip error probability is 0.1?

Literally nothing almost-- it is super immune to these errors espcially with such a low probability. If it was 0.1 then it would highly more affect the computation and create high variance and shift the computational mean up or down 0.1.

Q2. What happens to the computational results when you introduce a per-bit bit-shift error probability of 0.0001? What happens when the per-bit bit shift error probability is 0.1?

For both situations nothing happened-- it is much more resilient to this as it still keeps a lot of its own data, it just shfits down 1 number and copies one one at a index which randomly further samples the own distrubtion of the vector so it stays the same because of that too.

Q3. In summary, is the computation affected by these non-idealities? Do you see any changes in behavior as the bitstream grows?

Not really that much, especially not as much as classical computing. The bitflip one is more affected but still not that much relatively. As the bitstream grows it won't make a difference for any error, the expected value and error would remain the same.

#### Part Y: Statically Analyzing Stochastic Computations [2 pt/question, 8 points]

Next, we'll build a simple static analysis for stochastic computations. A _static analysis_ is a type of analysis that is able to infer information about a program without ever running the computation. The analysis we will be building determines the minimum bitstream size necessary for a computation, given a set of precisions for each of the arguments. For example, to compute the bitstream length for the following expression:

    (x + y) + z

We will set up the static analyzer as follows:

    `analysis = StochasticComputingStaticAnalysis()`
    `analysis.stoch_add(analysis.stoch_add(prec_x, prec_y), prec_z)`
    `N = analysis.get_size()`

where `prec_x`, `prec_y`, and `prec_z` are the precisions of x, y, and z respectively. Precision of a variable is defined as the smallest value of the variable. If the precision of x is 0.01, the precision of y is 0.02 and the precision of z is 0.03, then the minimum bitstream length is 100. In this exercise, you will be populating the `StochasticComputingStaticAnalysis` class, which offers the following functions:

    - `stoch_var`, given a variable with a desired precision `prec`, update the static analyzer to incorporate this information.
    - `stoch_add`, given two stochastic bitstreams that can represent values with precision `prec1` and `prec2` respectively, figure out the precision required for the result stochastic bitstream given an addition operation is performed. Update the static analyzer to incorporate any new information.
    - `stoch_mul`, given two stochastic bitstreams that can represent values with precision `prec1` and `prec2` respectively, figure out the precision required for the result stochastic bitstream given a multiplication operation is performed. Update the static analyzer to incorporate any new information.
    - `get_size`, given all of the operations and variables analyzed so far, return the smallest possible bitstream size that accurately executes all operations, and can accurately represent all values.

We will use this static analysis to figure out what stochastic bistream length to use for the computation (w*x + b), where the precision of w is 0.01, the precision of x is 0.1, and the precision of b is 0.1. For convenience, the scaffold file provides helper functions `PART_Y_analyze_wxb_function` for analyzing the `1/2*(w*x+b)` function, given a dictionary of precisions for variables `w`, `x`, and `b`, a `PART_Y_execute_wxb_function` which executes the `1/2*(w*x+b)` function using stochastic computing given a dictionary of variable values for `w`, `x`, and `b`, and a `PART_Y_test_analysis` function which uses the static analysis to find the best bitstream size for the `1/2*(w*x+b)` expresison, and then uses the size returned by the static analyzer to execute the `1/2*(w*x+b)` for ten random variable values that have the promised precisions.

Q1. Describe how your precision analysis works. Specifically, how do you propagate the precisions through the entire computation? How do you determine the final size?

I keep a private variable keeping track of the state of precision and updating based on the operation.

Q2. What bitstream length did your analysis return?



Q3. How did the random executions perform when parametrized with the analyzer-selected bitstream length?

Q4. What if you execute the parametrized computation with values w=0.00012, x = 0.124, and b = 0.1? Would you expect the result to be accurate? Why or why not?
 
#### Part Z: Sources of Error in Stochastic Computing [2 points + 2 points extra credit]

Next, we will investigate the `PART_Z_execute_rng_efficient_computation` stochastic computaton. This computation implements `1/2*(x*x+x)`, and implements an optimization (`save_rngs=True`) that reuses the bitstream for x to reduce the number of random number generators.

Q1. Does the accuracy of the computation change when the `save_rngs` optimization is enabled? Why or why not?

Q2. Devise an alternate method for implementing `1/2*(x*x+x)` from a single stochastic bitstream. There is a way to do this with a single (N+k)-bit bitstream, where k is a small constant value.

 
#### Part W: Extend the Stochastic Computing Paradigm [15 points]

Come up with your own extension, application, or analysis tool for the stochastic computing paradigm. This is your chance to be creative. Describe what task you chose, how it was implemented, and describe any interesting results that were observed. There is no need to pursue great results, e.g., beating some state-of-the-art approaches. It is fine to obtain minimum results just to show that your idea works. Here are some ideas to get you started:

- Implement a variant of stochastic computing, such as deterministic stochastic computing or bipolar stochastic computing. You may also modify the existing stochastic computing paradigm to incorporate a new source of hardware error -- you will need to justify your hardware error model. 

- Build an stochastic computing analysis of your choosing. You may build up the existing bitstream size analysis to work with abstract syntax trees, or you may devise a new analysis that studies some other property of the computation, such as error propagation or correlation.

- Implement an application using the stochastic computing paradigm. Examples from literature include image processing, ML inference, and LDPC decoding.