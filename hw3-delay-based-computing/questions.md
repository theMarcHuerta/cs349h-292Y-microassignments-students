# Assignment: Delay-Based Computing

In this assignment, we will implement numerous delay-based computing gates in `delay_gates.py`. To implement each gate, you need to fill in the `reset` and the `execute` functions:

 - The `reset` function should reset the state of the gate before execution. Recall delay-based computing gates are stateful and "remember" pulse information, and pulses are stored during a loading stage then released during execution. The reset function should define and reset whatever flags are necessary to correctly implement the operation of the gate.
 - The `execute` function should determine if the gate produces a pulse at a given timestep. The execute function takes as input the current time step (in nanoseconds), and a dictionary of input-value pairs. In this implementation, each port may have two values: PULSE (1) or NO_PULSE (0).

A `delay_circuit.py` Python file is provided to simulate a delay-based computing circuit and render the results, and a `delay_tester.py` Python file is provided to construct some simple single-gate circuits and simulate them for you. Each test function in the `delay_tester.py` produces a visualization of each simulation and a visualization of the circuit architecture. The measured time window is shaded.

## Part X: Understanding Delay-Based Encodings [8 points]

Execute the `delay_tester.py` file as is to investigate the behavior of delay-based input over time. The `test_input` function simulates the propagation of three constant delay-based values with labels ('X', 'Y', 'Z') through an empty circuit and outputs a pulse trace (`test_input.png`) and a summary of all the pulse arrivals/departures to console.

1. What does each numbered segment in the input image represent? What does it mean when a pulse (vertical line) is contained within a numbered segment?

2. What kind of value does an earlier pulse encode, what kind of value does a later pulse encode?

3. Run the simulation multiple times. Do you observe any variations in the plots from execution to execution?

4. Look at the pulse summary printed to console. How is a gate's numerical values computed from the relative delay and segment time? How is the relative delay computed from the absolute delay and the gate's settling time? The settling time for a given port is the time required for the pulse to reach a particular port.

# Part Y: Implementing the Delay Gates [8 pts]

Next, we will implement the simulations of first arrival, last arrival, delay, and inhibition gates associated with delay-based computing. Each delay gate is reset before execution, and then "executed" at each time step. The reset and execute functions may instantiate and change the gate's internal state, feel free to instantiate any internal variables needed.

1. Implement the reset and execute functions for the first arrival (`FirstArrival`) gate. Describe any internal state maintained by the gate, and what the reset operation and execution functions do for this gate. Uncomment the `test_first_arrival_gate` function in `delay_tester.py` to test the operation of the first arrival gate.


2. Implement the reset and execute functions for the last arrival (`LastArrival`) gate. Describe any internal state maintained by the gate, and what the reset operation and execution functions do for this gate. Uncomment the `test_last_arrival_gate` function in `delay_tester.py` to test the operation of the last arrival gate.


3. Implement the reset and execute functions for the delay (`Delay`) gate. Describe any internal state maintained by the gate, and what the reset operation and execution functions do for this gate. Uncomment the `test_delay_gate` function in `delay_tester.py` to test the operation of the delay gate. What does the circuit described in the `test_delay_gate` function do to the input value? 


4. Implement the reset and execute functions for the inhibition (`Inhibition`) gate. If two pulses arrive at the same time (which is unlikely in practice), you can assume that the gate emits a pulse with 50% probability. Describe any internal state maintained by the gate, and what the reset operation and execution functions do for this gate. Uncomment the `test_inh_gate` function in `delay_tester.py` to test the operation of the inhibition gate.

# Part Z: Using Delay-Based Computing [6 pts + 6 extra credit]

Implement a circuit that computes the numerical function.

    if max(X,Y) < 5:
        return max(X,Y)
    else:
        <no pulse>

You can use the `add_wire(src_gate,dst_gate,port)` function to add wires between gates, and the `add_gate(gate)` function to add a gate to the circuit. Feel free to use the `render_circuit("filename")` function to visualize the circuit that you built. As a reminder, in the simulation, the wire does not incur any delay but the gate introduces delay, and you need to make sure the inputs to the same gate have aligned delays. Reference the functions in `delay_tester.py` for examples of how to build and render a circuit. You do not need to worry about the `max(X,Y)=5` case. Test your circuit on a few values to verify that it computes the function correctly.

1. What is the structure of the circuit you implemented? Include a diagram of the circuit in your writeup. [4 pts]

2. What if the `<` operation is replaced with `>`? What is the structure of the circuit you implemented? Include a diagram of the circuit in your writeup. [4 extra credit]

Researchers have recently explored using delay-based computing in the log domain. With this method, instead of computing directly over numeric values, a value `x` is encoded into `x'=-ln(x)` as a delay (you need not worry about encoding of negative values in this question), delay-based computing is used to implement the computation, and then you raise the delay-based value `x=e^{-x'}` to recover the original value. This method can encode a broader value range using the same delay range, and obtain results faster compared to naive encoding, especially when dealing with large values.

2. The log domain encoding also enables operations that are difficult to implement in the original value domain. Describe how you can implement multiplication and constant value scaling in log domain. [2 pts]

3. One downside of computing in log domain though is that addition and substraction become more difficult. However, there are effective appraoches to approximate them. For example, substraction of two values `z=x-y` is `z'=-ln(e^{-x'}-e^{-y'})` in the log domain, but it can be approximated using delay logic as `z'=min(inhibit(x'+E0,y'+F0), ...,inhibit(x'+En,y'+Fn))`, where `Ei`'s and `Fi`'s are specially picked constants. Refer to `nLDE_approximation.png` in the folder for a visualization where `x'+y'=0`. Could you devise a similar approximation approach for addition? You may also focus on the case where `x'+y'=0`. Write the expression you use for the approximation, using only `min`, `max`, `inhibit` operations. Include a figure to show how good the approximation is in your writeup. [2 extra credit]

# Part W: Digital Logic with Delay-Based Computing [14 pts]

Move to the `delay_digital.py` file. The file uses race-based computing to execute `(X | not Y) and (Z | X) and (Z | Y)`. I have already implemented the scaffold for this part of the project which builds the logic circuit, and convenience functions for performing the dual-rail encoding. The delay-signal visualization in this part may be too dense to read due to many number of gates, but you may read the text output for debugging.

1. Implement the `and` gate using delay logic. How did you implement this gate?

2. Implement the `or` gate using delay logic. How did you implement this gate?

3. Implement the `not` gate using delay logic. How did you implement this gate?

4. Implement the digital readout gate in `delay_gates.py` (see class `DigitalReadOutGate`). This gate should remember if it saw a pulse or not.

5. Execute the completed implementation on a few digital values. What delay-based encoding does a digital "1" output correspond to? What delay-based encoding does the digital "0" output correspond to? What states are invalid in the current digital value encoding?
 
6. Currently, the implementation creates a fresh input signal for every usage of every variable instead of re-using the input signal. Why is this necessary? What would happen if you build the same circuit, but then reuse the same input for multiple gates?

7. What would happen if you don't reset the circuit between executions? Why is a circuit reset operation necessary for delay-based digital logic, but not necessary for conventional digital logic?
