```bash
                             ███╗   ███╗ ██████╗ ███╗   ██╗ █████╗ ███╗   ███╗██╗
                             ████╗ ████║██╔═══██╗████╗  ██║██╔══██╗████╗ ████║██║
                             ██╔████╔██║██║   ██║██╔██╗ ██║███████║██╔████╔██║██║
                             ██║╚██╔╝██║██║   ██║██║╚██╗██║██╔══██║██║╚██╔╝██║██║
                             ██║ ╚═╝ ██║╚██████╔╝██║ ╚████║██║  ██║██║ ╚═╝ ██║██║
                             ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝
                                  
                                  Monitoring First-Order Interval Logic
                                       Version 1.0, May 31 - 2021            
```

# Overview
MonAmI is a Python library for monitoring the foATL (First-Order Allen Temporal Logic), which is an extension of [Allen's temporal logic](https://en.wikipedia.org/wiki/Allen%27s_interval_algebra). 

MonAmI processes a sequence of events and checks them against a FoATL property. 
An example of a FoATL property is the following, expressing that there is no
fail of a downlink of data from a spacecraft (a `DL_FAIL` interval) during a downlink of mobility parameters (a `DL_MOBPRM` interval) or downlink of robotic arm parameters (a `DL_ARMPRM` interval):


```
!exist D, F . (D('DL_MOBPRM') | D('DL_ARMPRM')) & F('DL_FAIL') & D i F
```

The property states that there do not exist intervals `D` and `F` (`!exist D, F`) such that (`.`) D with data `DL_MOBPRM` (`D('DL_MOBPRM'`) or (`|`) D with data `DL_ARMPRM` includes (`i`) interval F with `DL_FAIL` data. 

The implementation uses [BDDs (Binary Decision Diagrams)](https://en.wikipedia.org/wiki/Binary_decision_diagram) for representing assignments to quantified variables with their data (such as `D('DL_MOBPRM')`) and for the Allen's intervals (such as `D i F`).

# Installing MonAmI

The directory out contains files and directories useful for installing and running MonAmI:

* __examples__: An example directory containing properties, traces and other files.
* __guides__: A directory containing other guides such as using the trace_generator.py.
* __papers__: A directory containing papers written about MonAmI.
  
MonAmI is implemented in Python.

1. Install Python 3.7 and above (We used Python 3.9).
2. Download MonAmI project.
3. Run the command `python3 -m pip install -r requierments.txt` (from CMD in windows or Terminal in Unix/Mac). Make sure that `python3` points to your Python > 3.7 version.
4. To use dd.cudd (Cython binding to the CUDD C library) interface, follow the instruction at https://github.com/tulip-control/dd#installation 
(__Note: For good performance on large traces, dd.cudd is necessary__)
   
# Running MonAmI
1. cd to MonAmI root directory.
2. Type ``` export PYTHONPATH=$PYTHONPATH:`pwd` ``` and press enter (only for the first execution).   
3. Running MonAmI is made by executing the command `python3 monami.py`. Make sure that `python3` points to your Python > 3.7 version.
4. Before running, you must change the `configuration` file according to your environment and needs.

### Configuration File: 

The `configuration` file defines parameters that controls the execution of MonAmI. Two parameters (`INTERVAL_SIZE` and `DATA_SIZE`)
require a brief upfront explanation. MonAmi stores interval identifiers and data as BDDs (as mentioned above). The BDDs are essentially encoding
of binary numbers used to represent the intervals and data. The `SIZE` refers to the number of bits used for this representation. E.g. if we know we will only observe 6 different data, we only need 3 bits to represen these, hence `DATA_SIZE` can be 3.

    1. `DEBUG` - If true, the program will print to the console messages that describe the BDDs for each event.
    2. `INTERVAL_SIZE` - Initial length of the enumeration of intervals.
       1. `int` - Set the initial size to be as the specified value.
       2. `AUTO` - Set the initial value to match the size of the trace (expansion will not happen).
    3. `DATA_SIZE` - Initial length of the enumeration of data.
       1. `int` - Set the initial size to be as the specified value.
       2. `AUTO` - Set the initial value to match the size of the trace (expansion will not happen).
    4. `EXPANSION_LENGTH` - The expansion length when an enumeration needs to grow.
    5. `MODE` - Define the mode of operation of MonAmI, controlling when monitoring stops.
       1. `VIOLATION` - MonAmI will stop when the property evaluates to False.
       2. `SATISFACTION` - MonAmI will stop when the property evaluates to True.
       3. `CONTINUE-SMALL` - MonAmI evaluates the property after every event until the end of the trace.
       4. `CONTINUE-BIG` - MonAmi evaluates the property once at the end of the trace.
    6. `TRACE` - Path to the `trace` file.
    7. `PROPERTY` - Path to the `property` file.

The parameters and their possible values are tabulated below.
    
Parameter         | Details
----------------- | -------------
`DEBUG`           | `true` or `false`
`INTERVAL_SIZE`   | `int` or `AUTO`
`DATA_SIZE`       | `int` or `AUTO`
`EXPANSION_LENGTH`| `int`
`MODE`            | `VIOLATION`, `SATISFACTION`, `CONTINUE-SMALL` or `CONTINUE-BIG`
`TRACE`           | `str`
`PROPERTY`        | `str`

###Example of 'configuration` file:

```json
{
    "DEBUG": false,
    "INTERVAL_SIZE": "AUTO",
    "DATA_SIZE": "AUTO",
    "EXPANSION_LENGTH": 2,
    "MODE": "CONTINUE-SMALL",
    "TRACE": "/home/john/project/MonAmI/input/trace",
    "PROPERTY": "/home/john/project/MonAmI/input/property"
}
```
# The MonAmI Specification Logic
### Grammar ###
The grammar for the MonAmI First-Order Interval Logic is as follows:

```
<formula> ::=
    | <formula> '|' <formula>
    | <formula> '->' <formula>
    | <formula> '&' <formula>
    | '!' <formula>
    | <name> '<' <name>
    | <name> 'o' <name>
    | <name> 'i' <name>
    | <name> '(' <data> ')'
    | 'same' '(' <name> ',' <name> ')'
    | 'exist' <names> '.' <formula>
    | 'forall' <names> '.' <formula>
    | '(' <formula> ')'
    
 <name> ::= r'[a-zA-Z_][a-zA-Z0-9_\.]*'
 <names> ::= <name> | <names> ',' <name>
 <data> ::= <number> | <string>
 <number> ::= r'\d+'
 <string> ::= r'\"([^\\\n]|(\\.))*?\"'
```
The Boolean binary operators have precedence as follows: 
`|` and `->` have the same precedence, which is weaker than
the precedence of `&`, which is weaker than the precedence of 
`!`. 

For example:

```
A < B & C < D | ! E < F & G < H
```

Has the same meaning as this formula:

```
(A < B & C < D) | ((! E < F) & G < H)
```

### Formulas ###
The different formulas <formula> have the following intuitive meaning:

Operator                            | Meaning
----------------------------------- | -------------
<code> p &#124; q </code>           | `p OR q`
`p & q`                             | `p AND q`
`p -> q`                            | `p IMPLIES q`
`!p`                                | `NOT p`
`A < B`                             | A before B : A ends before B starts
`A o B`                             | A overlaps B : B starts after A starts and before A ends, and B ends after A ends
`A i B`                             | A includes B : B starts after A starts and ends before A ends
`A(d)`                              | Denotes that the data of the interval assigned to the variable `A` is the constant `d`
`same(A, B)`                        | Denotes that the two intervals A and B carry the same value
`exist A1,...,An . p(A1,...An)`     | There exist intervals A1,...,An such that p(A1,...,An)
`forall A1,...,An . p(A1,...,An)`   | For all intervals A1,...,An it holds that p(A1,...,An)  
`(p)`                               | Same meaning as p 

### Example Properties

#### Double Boot ####

During a spacecraft operation, a particular concern is whether there is a downlink operation of an image (`DL_IMAGE`)
during an interval where the flight computer reboots (`BOOT`) twice. This scenario could cause a potential loss of downlink information.

```
!exist B1, B2, D . 
  B1('BOOT') & B2('BOOT') & D('DL_IMAGE') & 
  B1 < B2 & 
  (B1 i D | B2 i D) | (B1 < D & D < B2) | (B1 o D & !D i B2) | (D o B2 & !D i B1))
```

#### Power-on Failure

We here want to detect whether an instrument power-on command (`INS_ON`) fails (`INS_FAIL`) and then recovers (`INS_RECOVER`).

```
!exist O, F, R . 
  O('INS_ON') & F('INS_FAIL') & R('INS_RECOVER') & 
  O < F & F < R & 
  !exist X . (X('INS_ON') | X('INS_RECOVER')) & O < X & X < R
```

#### Task Starvation

We here want to detect whether there is task starvation (`STARVE`) during an interval where
an activity reading data from the camera
(`GET_CAMDATA`) overlaps with an Earth image communication activity (`DL_IMAGE`).

```
!exist D, G, S . 
  D('DL_IMAGE') & G('GET_CAMDATA') & S('STARVE') & 
  D i S & 
  G i S
```


# The MonAmI Trace Language

The format of traces is as follows.

* A trace in a sequence of events.
* An interval is created internally in MonaAmi from a `begin` event followed by a corresponding `end` event with the same interval ID.
  
Each event is from the type `["begin", Interval ID, Data]` for a `begin` event, and `["end", Interval ID]` for an `end` event.

Parameter     | Details
------------- | -------------
Event Type    | `"begin"` or `"end"` only
Interval ID   | `int`, `str`
Data          | `null`, `int`, or `str` for begin events only

# MonAmI Execution Example (in debug mode): 

Both property and trace are assumed stored in JSON files, with particular
  formats, as illustrated below.
  
Assume the property:

```json
{
    "property": 
      "!exist B1, B2, D . 
        B1('BOOT') & B2('BOOT') & D('DL_IMAGE') & 
        B1 < B2 & 
        (B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & !D i B2) | (D o B2 & !D i B1))"
}
```

Assume furthermore the trace:

```json
{
    "execution": 
       [
         ["begin", 1, "BOOT"], 
         ["begin", 2, "DL_IMAGE"], 
         ["end", 1], 
         ["end", 2], 
         ["begin", 3, "BOOT"], 
         ["end", 3]
       ]
}
```

and assume the configuration file:

```json
{
    "DEBUG": true,
    "INTERVAL_SIZE": "AUTO",
    "DATA_SIZE": 1,
    "EXPANSION_LENGTH": 2,
    "MODE": "VIOLATION",
    "TRACE": "/home/john/project/MonAmI/input/trace",
    "PROPERTY": "/home/john/project/MonAmI/input/property"
}
```

We choose `"MODE": "VIOLATION"` since we want to check whether a violation occurs as soon as it is encountered.
In the example, the property will be violated at the last event. 

`"INTERVAL_SIZE": "AUTO"` will set the interval bitstring size into 2, since with 2 bits, we can represent four different intervals (00, 01, 10, 11). 
        
`"DATA_SIZE": 1` is good enough since 1 bit can represent two distinct data values, and in our example, we have only two.

In debug mode, after each event, the program will print to console the updated BDDs.
It also prints other information, like bitstring expansion if it happens, and the mapping between intervals and data to bitstrings.
The final state will be printed at the end of the execution.

The output generated from running MonAmi on the above trace, property, and configuration file is as follows.
          
          
```python
          

                         ███╗   ███╗ ██████╗ ███╗   ██╗ █████╗ ███╗   ███╗██╗
                         ████╗ ████║██╔═══██╗████╗  ██║██╔══██╗████╗ ████║██║
                         ██╔████╔██║██║   ██║██╔██╗ ██║███████║██╔████╔██║██║
                         ██║╚██╔╝██║██║   ██║██║╚██╗██║██╔══██║██║╚██╔╝██║██║
                         ██║ ╚═╝ ██║╚██████╔╝██║ ╚████║██║  ██║██║ ╚═╝ ██║██║
                         ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝
                                                    

############################################################################## (START) ##############################################################################
[EXECUTION]: [['begin', 1, 'BOOT'], ['begin', 2, 'DL_IMAGE'], ['end', 1], ['end', 2], ['begin', 3, 'BOOT'], ['end', 3]]

[PROPERTY]: ! exist ['B1', 'B2', 'D'] . B1(BOOT) & B2(BOOT) & D(DL_IMAGE) & B1 < B2 & (B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2) | (D o B2 & ! D i B1))

|-- [ENUMERATION]: 1 -> "00" ([False, False])
|-- [ENUMERATION]: BOOT -> "0" ([False])
|-- [EVENT]: begin(1, BOOT)
    |-- [X]: [{'_X0': False, '_X1': False}]
    |-- [XX]: []
    |-- [XY]: []
    |-- [XYY]: []
    |-- [XYYX]: []
    |-- [XYX]: []
    |-- [XYXY]: []
    |-- [XXY]: []
    |-- [XXYY]: []
    |-- [XD]: []
    |-- [AST]:
        |-- [B1(BOOT)]: []
        |-- [B2(BOOT)]: []
        |-- [(B1(BOOT)) & (B2(BOOT)))]: []
        |-- [D(DL_IMAGE)]: []
        |-- [(B1(BOOT) & B2(BOOT)) & (D(DL_IMAGE)))]: []
        |-- [B1 < B2]: []
        |-- [(B1(BOOT) & B2(BOOT) & D(DL_IMAGE)) & (B1 < B2))]: []
        |-- [B1 i D]: []
        |-- [B2 i D]: []
        |-- [(B1 i D) | (B2 i D))]: []
        |-- [B1 < D]: []
        |-- [D < B2]: []
        |-- [(B1 < D) & (D < B2))]: []
        |-- [(B1 < D & D < B2)]: []
        |-- [(B1 i D | B2 i D) | ((B1 < D & D < B2)))]: []
        |-- [B1 o D]: []
        |-- [D i B2]: []
        |-- [~(D i B2))]: [{}]
        |-- [(B1 o D) & (! D i B2))]: []
        |-- [(B1 o D & ! D i B2)]: []
        |-- [(B1 i D | B2 i D | (B1 < D & D < B2)) | ((B1 o D & ! D i B2)))]: []
        |-- [D o B2]: []
        |-- [D i B1]: []
        |-- [~(D i B1))]: [{}]
        |-- [(D o B2) & (! D i B1))]: []
        |-- [(D o B2 & ! D i B1)]: []
        |-- [(B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2)) | ((D o B2 & ! D i B1)))]: []
        |-- [(B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2) | (D o B2 & ! D i B1))]: []
        |-- [(B1(BOOT) & B2(BOOT) & D(DL_IMAGE) & B1 < B2) & ((B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2) | (D o B2 & ! D i B1))))]: []
        |-- [exist ['B1', 'B2', 'D'] . B1(BOOT) & B2(BOOT) & D(DL_IMAGE) & B1 < B2 & (B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2) | (D o B2 & ! D i B1))]: []
        |-- [~(exist ['B1', 'B2', 'D'] . B1(BOOT) & B2(BOOT) & D(DL_IMAGE) & B1 < B2 & (B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2) | (D o B2 & ! D i B1))))]: [{}]

[INFO]: Specification result is True

|-- [ENUMERATION]: 2 -> "01" ([False, True])
|-- [ENUMERATION]: DL_IMAGE -> "1" ([True])
|-- [EVENT]: begin(2, DL_IMAGE)
    |-- [X]: [{'_X0': False}]
    |-- [XX]: []
    |-- [XY]: [{'_X0': False, '_X1': False, '_Y0': False, '_Y1': True}]
    |-- [XYY]: []
    |-- [XYYX]: []
    |-- [XYX]: []
    |-- [XYXY]: []
    |-- [XXY]: []
    |-- [XXYY]: []
    |-- [XD]: []
    |-- [AST]:
        |-- [B1(BOOT)]: []
        |-- [B2(BOOT)]: []
        |-- [(B1(BOOT)) & (B2(BOOT)))]: []
        |-- [D(DL_IMAGE)]: []
        |-- [(B1(BOOT) & B2(BOOT)) & (D(DL_IMAGE)))]: []
        |-- [B1 < B2]: []
        |-- [(B1(BOOT) & B2(BOOT) & D(DL_IMAGE)) & (B1 < B2))]: []
        |-- [B1 i D]: []
        |-- [B2 i D]: []
        |-- [(B1 i D) | (B2 i D))]: []
        |-- [B1 < D]: []
        |-- [D < B2]: []
        |-- [(B1 < D) & (D < B2))]: []
        |-- [(B1 < D & D < B2)]: []
        |-- [(B1 i D | B2 i D) | ((B1 < D & D < B2)))]: []
        |-- [B1 o D]: []
        |-- [D i B2]: []
        |-- [~(D i B2))]: [{}]
        |-- [(B1 o D) & (! D i B2))]: []
        |-- [(B1 o D & ! D i B2)]: []
        |-- [(B1 i D | B2 i D | (B1 < D & D < B2)) | ((B1 o D & ! D i B2)))]: []
        |-- [D o B2]: []
        |-- [D i B1]: []
        |-- [~(D i B1))]: [{}]
        |-- [(D o B2) & (! D i B1))]: []
        |-- [(D o B2 & ! D i B1)]: []
        |-- [(B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2)) | ((D o B2 & ! D i B1)))]: []
        |-- [(B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2) | (D o B2 & ! D i B1))]: []
        |-- [(B1(BOOT) & B2(BOOT) & D(DL_IMAGE) & B1 < B2) & ((B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2) | (D o B2 & ! D i B1))))]: []
        |-- [exist ['B1', 'B2', 'D'] . B1(BOOT) & B2(BOOT) & D(DL_IMAGE) & B1 < B2 & (B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2) | (D o B2 & ! D i B1))]: []
        |-- [~(exist ['B1', 'B2', 'D'] . B1(BOOT) & B2(BOOT) & D(DL_IMAGE) & B1 < B2 & (B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2) | (D o B2 & ! D i B1))))]: [{}]

[INFO]: Specification result is True

|-- [ENUMERATION]: 1 -> "00" ([False, False])
|-- [EVENT]: end(1, BOOT)
    |-- [X]: [{'_X0': False, '_X1': True}]
    |-- [XX]: [{'_X0': False, '_X1': False}]
    |-- [XY]: []
    |-- [XYY]: []
    |-- [XYYX]: []
    |-- [XYX]: [{'_X0': False, '_X1': False, '_Y0': False, '_Y1': True}]
    |-- [XYXY]: []
    |-- [XXY]: []
    |-- [XXYY]: []
    |-- [XD]: [{'_X0': False, '_X1': False, '_D0': False}]
    |-- [AST]:
        |-- [B1(BOOT)]: [{'B10': False, 'B11': False}]
        |-- [B2(BOOT)]: [{'B20': False, 'B21': False}]
        |-- [(B1(BOOT)) & (B2(BOOT)))]: [{'B10': False, 'B11': False, 'B20': False, 'B21': False}]
        |-- [D(DL_IMAGE)]: []
        |-- [(B1(BOOT) & B2(BOOT)) & (D(DL_IMAGE)))]: []
        |-- [B1 < B2]: []
        |-- [(B1(BOOT) & B2(BOOT) & D(DL_IMAGE)) & (B1 < B2))]: []
        |-- [B1 i D]: []
        |-- [B2 i D]: []
        |-- [(B1 i D) | (B2 i D))]: []
        |-- [B1 < D]: []
        |-- [D < B2]: []
        |-- [(B1 < D) & (D < B2))]: []
        |-- [(B1 < D & D < B2)]: []
        |-- [(B1 i D | B2 i D) | ((B1 < D & D < B2)))]: []
        |-- [B1 o D]: []
        |-- [D i B2]: []
        |-- [~(D i B2))]: [{}]
        |-- [(B1 o D) & (! D i B2))]: []
        |-- [(B1 o D & ! D i B2)]: []
        |-- [(B1 i D | B2 i D | (B1 < D & D < B2)) | ((B1 o D & ! D i B2)))]: []
        |-- [D o B2]: []
        |-- [D i B1]: []
        |-- [~(D i B1))]: [{}]
        |-- [(D o B2) & (! D i B1))]: []
        |-- [(D o B2 & ! D i B1)]: []
        |-- [(B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2)) | ((D o B2 & ! D i B1)))]: []
        |-- [(B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2) | (D o B2 & ! D i B1))]: []
        |-- [(B1(BOOT) & B2(BOOT) & D(DL_IMAGE) & B1 < B2) & ((B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2) | (D o B2 & ! D i B1))))]: []
        |-- [exist ['B1', 'B2', 'D'] . B1(BOOT) & B2(BOOT) & D(DL_IMAGE) & B1 < B2 & (B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2) | (D o B2 & ! D i B1))]: []
        |-- [~(exist ['B1', 'B2', 'D'] . B1(BOOT) & B2(BOOT) & D(DL_IMAGE) & B1 < B2 & (B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2) | (D o B2 & ! D i B1))))]: [{}]

[INFO]: Specification result is True

|-- [ENUMERATION]: 2 -> "01" ([False, True])
|-- [EVENT]: end(2, DL_IMAGE)
    |-- [X]: []
    |-- [XX]: [{'_X0': False}]
    |-- [XY]: []
    |-- [XYY]: []
    |-- [XYYX]: []
    |-- [XYX]: []
    |-- [XYXY]: [{'_X0': False, '_X1': False, '_Y0': False, '_Y1': True}]
    |-- [XXY]: []
    |-- [XXYY]: []
    |-- [XD]: [{'_X0': False, '_X1': False, '_D0': False}, {'_X0': False, '_X1': True, '_D0': True}]
    |-- [AST]:
        |-- [B1(BOOT)]: [{'B10': False, 'B11': False}]
        |-- [B2(BOOT)]: [{'B20': False, 'B21': False}]
        |-- [(B1(BOOT)) & (B2(BOOT)))]: [{'B10': False, 'B11': False, 'B20': False, 'B21': False}]
        |-- [D(DL_IMAGE)]: [{'D0': False, 'D1': True}]
        |-- [(B1(BOOT) & B2(BOOT)) & (D(DL_IMAGE)))]: [{'B10': False, 'B11': False, 'B20': False, 'B21': False, 'D0': False, 'D1': True}]
        |-- [B1 < B2]: []
        |-- [(B1(BOOT) & B2(BOOT) & D(DL_IMAGE)) & (B1 < B2))]: []
        |-- [B1 i D]: []
        |-- [B2 i D]: []
        |-- [(B1 i D) | (B2 i D))]: []
        |-- [B1 < D]: []
        |-- [D < B2]: []
        |-- [(B1 < D) & (D < B2))]: []
        |-- [(B1 < D & D < B2)]: []
        |-- [(B1 i D | B2 i D) | ((B1 < D & D < B2)))]: []
        |-- [B1 o D]: [{'B10': False, 'B11': False, 'D0': False, 'D1': True}]
        |-- [D i B2]: []
        |-- [~(D i B2))]: [{}]
        |-- [(B1 o D) & (! D i B2))]: [{'B10': False, 'B11': False, 'D0': False, 'D1': True}]
        |-- [(B1 o D & ! D i B2)]: [{'B10': False, 'B11': False, 'D0': False, 'D1': True}]
        |-- [(B1 i D | B2 i D | (B1 < D & D < B2)) | ((B1 o D & ! D i B2)))]: [{'B10': False, 'B11': False, 'D0': False, 'D1': True}]
        |-- [D o B2]: [{'B20': False, 'B21': True, 'D0': False, 'D1': False}]
        |-- [D i B1]: []
        |-- [~(D i B1))]: [{}]
        |-- [(D o B2) & (! D i B1))]: [{'B20': False, 'B21': True, 'D0': False, 'D1': False}]
        |-- [(D o B2 & ! D i B1)]: [{'B20': False, 'B21': True, 'D0': False, 'D1': False}]
        |-- [(B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2)) | ((D o B2 & ! D i B1)))]: [{'B10': False, 'B11': False, 'B20': False, 'B21': False, 'D0': False, 'D1': True}, {'D1': False, 'B10': False, 'B11': False, 'B20': False, 'B21': True, 'D0': False}, {'D1': True, 'B10': False, 'B11': False, 'B20': False, 'B21': True, 'D0': False}, {'B21': False, 'B10': False, 'B11': False, 'B20': True, 'D0': False, 'D1': True}, {'B21': True, 'B10': False, 'B11': False, 'B20': True, 'D0': False, 'D1': True}, {'B10': False, 'B11': True, 'B20': False, 'B21': True, 'D0': False, 'D1': False}, {'B11': False, 'B10': True, 'B20': False, 'B21': True, 'D0': False, 'D1': False}, {'B11': True, 'B10': True, 'B20': False, 'B21': True, 'D0': False, 'D1': False}]
        |-- [(B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2) | (D o B2 & ! D i B1))]: [{'B10': False, 'B11': False, 'B20': False, 'B21': False, 'D0': False, 'D1': True}, {'D1': False, 'B10': False, 'B11': False, 'B20': False, 'B21': True, 'D0': False}, {'D1': True, 'B10': False, 'B11': False, 'B20': False, 'B21': True, 'D0': False}, {'B21': False, 'B10': False, 'B11': False, 'B20': True, 'D0': False, 'D1': True}, {'B21': True, 'B10': False, 'B11': False, 'B20': True, 'D0': False, 'D1': True}, {'B10': False, 'B11': True, 'B20': False, 'B21': True, 'D0': False, 'D1': False}, {'B11': False, 'B10': True, 'B20': False, 'B21': True, 'D0': False, 'D1': False}, {'B11': True, 'B10': True, 'B20': False, 'B21': True, 'D0': False, 'D1': False}]
        |-- [(B1(BOOT) & B2(BOOT) & D(DL_IMAGE) & B1 < B2) & ((B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2) | (D o B2 & ! D i B1))))]: []
        |-- [exist ['B1', 'B2', 'D'] . B1(BOOT) & B2(BOOT) & D(DL_IMAGE) & B1 < B2 & (B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2) | (D o B2 & ! D i B1))]: []
        |-- [~(exist ['B1', 'B2', 'D'] . B1(BOOT) & B2(BOOT) & D(DL_IMAGE) & B1 < B2 & (B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2) | (D o B2 & ! D i B1))))]: [{}]

[INFO]: Specification result is True

|-- [ENUMERATION]: 3 -> "10" ([True, False])
|-- [ENUMERATION]: BOOT -> "0" ([False])
|-- [EVENT]: begin(3, BOOT)
    |-- [X]: [{'_X0': True, '_X1': False}]
    |-- [XX]: [{'_X0': False}]
    |-- [XY]: []
    |-- [XYY]: []
    |-- [XYYX]: []
    |-- [XYX]: []
    |-- [XYXY]: [{'_X0': False, '_X1': False, '_Y0': False, '_Y1': True}]
    |-- [XXY]: [{'_X0': False, '_Y0': True, '_Y1': False}]
    |-- [XXYY]: []
    |-- [XD]: [{'_X0': False, '_X1': False, '_D0': False}, {'_X0': False, '_X1': True, '_D0': True}]
    |-- [AST]:
        |-- [B1(BOOT)]: [{'B10': False, 'B11': False}]
        |-- [B2(BOOT)]: [{'B20': False, 'B21': False}]
        |-- [(B1(BOOT)) & (B2(BOOT)))]: [{'B10': False, 'B11': False, 'B20': False, 'B21': False}]
        |-- [D(DL_IMAGE)]: [{'D0': False, 'D1': True}]
        |-- [(B1(BOOT) & B2(BOOT)) & (D(DL_IMAGE)))]: [{'B10': False, 'B11': False, 'B20': False, 'B21': False, 'D0': False, 'D1': True}]
        |-- [B1 < B2]: []
        |-- [(B1(BOOT) & B2(BOOT) & D(DL_IMAGE)) & (B1 < B2))]: []
        |-- [B1 i D]: []
        |-- [B2 i D]: []
        |-- [(B1 i D) | (B2 i D))]: []
        |-- [B1 < D]: []
        |-- [D < B2]: []
        |-- [(B1 < D) & (D < B2))]: []
        |-- [(B1 < D & D < B2)]: []
        |-- [(B1 i D | B2 i D) | ((B1 < D & D < B2)))]: []
        |-- [B1 o D]: [{'B10': False, 'B11': False, 'D0': False, 'D1': True}]
        |-- [D i B2]: []
        |-- [~(D i B2))]: [{}]
        |-- [(B1 o D) & (! D i B2))]: [{'B10': False, 'B11': False, 'D0': False, 'D1': True}]
        |-- [(B1 o D & ! D i B2)]: [{'B10': False, 'B11': False, 'D0': False, 'D1': True}]
        |-- [(B1 i D | B2 i D | (B1 < D & D < B2)) | ((B1 o D & ! D i B2)))]: [{'B10': False, 'B11': False, 'D0': False, 'D1': True}]
        |-- [D o B2]: [{'B20': False, 'B21': True, 'D0': False, 'D1': False}]
        |-- [D i B1]: []
        |-- [~(D i B1))]: [{}]
        |-- [(D o B2) & (! D i B1))]: [{'B20': False, 'B21': True, 'D0': False, 'D1': False}]
        |-- [(D o B2 & ! D i B1)]: [{'B20': False, 'B21': True, 'D0': False, 'D1': False}]
        |-- [(B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2)) | ((D o B2 & ! D i B1)))]: [{'B10': False, 'B11': False, 'B20': False, 'B21': False, 'D0': False, 'D1': True}, {'D1': False, 'B10': False, 'B11': False, 'B20': False, 'B21': True, 'D0': False}, {'D1': True, 'B10': False, 'B11': False, 'B20': False, 'B21': True, 'D0': False}, {'B21': False, 'B10': False, 'B11': False, 'B20': True, 'D0': False, 'D1': True}, {'B21': True, 'B10': False, 'B11': False, 'B20': True, 'D0': False, 'D1': True}, {'B10': False, 'B11': True, 'B20': False, 'B21': True, 'D0': False, 'D1': False}, {'B11': False, 'B10': True, 'B20': False, 'B21': True, 'D0': False, 'D1': False}, {'B11': True, 'B10': True, 'B20': False, 'B21': True, 'D0': False, 'D1': False}]
        |-- [(B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2) | (D o B2 & ! D i B1))]: [{'B10': False, 'B11': False, 'B20': False, 'B21': False, 'D0': False, 'D1': True}, {'D1': False, 'B10': False, 'B11': False, 'B20': False, 'B21': True, 'D0': False}, {'D1': True, 'B10': False, 'B11': False, 'B20': False, 'B21': True, 'D0': False}, {'B21': False, 'B10': False, 'B11': False, 'B20': True, 'D0': False, 'D1': True}, {'B21': True, 'B10': False, 'B11': False, 'B20': True, 'D0': False, 'D1': True}, {'B10': False, 'B11': True, 'B20': False, 'B21': True, 'D0': False, 'D1': False}, {'B11': False, 'B10': True, 'B20': False, 'B21': True, 'D0': False, 'D1': False}, {'B11': True, 'B10': True, 'B20': False, 'B21': True, 'D0': False, 'D1': False}]
        |-- [(B1(BOOT) & B2(BOOT) & D(DL_IMAGE) & B1 < B2) & ((B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2) | (D o B2 & ! D i B1))))]: []
        |-- [exist ['B1', 'B2', 'D'] . B1(BOOT) & B2(BOOT) & D(DL_IMAGE) & B1 < B2 & (B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2) | (D o B2 & ! D i B1))]: []
        |-- [~(exist ['B1', 'B2', 'D'] . B1(BOOT) & B2(BOOT) & D(DL_IMAGE) & B1 < B2 & (B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2) | (D o B2 & ! D i B1))))]: [{}]

[INFO]: Specification result is True

|-- [ENUMERATION]: 3 -> "10" ([True, False])
|-- [EVENT]: end(3, BOOT)
    |-- [X]: []
    |-- [XX]: [{'_X1': False, '_X0': False}, {'_X1': True, '_X0': False}, {'_X0': True, '_X1': False}]
    |-- [XY]: []
    |-- [XYY]: []
    |-- [XYYX]: []
    |-- [XYX]: []
    |-- [XYXY]: [{'_X0': False, '_X1': False, '_Y0': False, '_Y1': True}]
    |-- [XXY]: []
    |-- [XXYY]: [{'_X0': False, '_Y0': True, '_Y1': False}]
    |-- [XD]: [{'_X0': False, '_X1': False, '_D0': False}, {'_X0': False, '_X1': True, '_D0': True}, {'_X0': True, '_X1': False, '_D0': False}]
    |-- [AST]:
        |-- [B1(BOOT)]: [{'B11': False}]
        |-- [B2(BOOT)]: [{'B21': False}]
        |-- [(B1(BOOT)) & (B2(BOOT)))]: [{'B11': False, 'B21': False}]
        |-- [D(DL_IMAGE)]: [{'D0': False, 'D1': True}]
        |-- [(B1(BOOT) & B2(BOOT)) & (D(DL_IMAGE)))]: [{'B11': False, 'B21': False, 'D0': False, 'D1': True}]
        |-- [B1 < B2]: [{'B10': False, 'B20': True, 'B21': False}]
        |-- [(B1(BOOT) & B2(BOOT) & D(DL_IMAGE)) & (B1 < B2))]: [{'B10': False, 'B11': False, 'B20': True, 'B21': False, 'D0': False, 'D1': True}]
        |-- [B1 i D]: []
        |-- [B2 i D]: []
        |-- [(B1 i D) | (B2 i D))]: []
        |-- [B1 < D]: [{'B10': False, 'D0': True, 'D1': False}]
        |-- [D < B2]: [{'B20': True, 'B21': False, 'D0': False}]
        |-- [(B1 < D) & (D < B2))]: []
        |-- [(B1 < D & D < B2)]: []
        |-- [(B1 i D | B2 i D) | ((B1 < D & D < B2)))]: []
        |-- [B1 o D]: [{'B10': False, 'B11': False, 'D0': False, 'D1': True}]
        |-- [D i B2]: []
        |-- [~(D i B2))]: [{}]
        |-- [(B1 o D) & (! D i B2))]: [{'B10': False, 'B11': False, 'D0': False, 'D1': True}]
        |-- [(B1 o D & ! D i B2)]: [{'B10': False, 'B11': False, 'D0': False, 'D1': True}]
        |-- [(B1 i D | B2 i D | (B1 < D & D < B2)) | ((B1 o D & ! D i B2)))]: [{'B10': False, 'B11': False, 'D0': False, 'D1': True}]
        |-- [D o B2]: [{'B20': False, 'B21': True, 'D0': False, 'D1': False}]
        |-- [D i B1]: []
        |-- [~(D i B1))]: [{}]
        |-- [(D o B2) & (! D i B1))]: [{'B20': False, 'B21': True, 'D0': False, 'D1': False}]
        |-- [(D o B2 & ! D i B1)]: [{'B20': False, 'B21': True, 'D0': False, 'D1': False}]
        |-- [(B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2)) | ((D o B2 & ! D i B1)))]: [{'B10': False, 'B11': False, 'B20': False, 'B21': False, 'D0': False, 'D1': True}, {'D1': False, 'B10': False, 'B11': False, 'B20': False, 'B21': True, 'D0': False}, {'D1': True, 'B10': False, 'B11': False, 'B20': False, 'B21': True, 'D0': False}, {'B21': False, 'B10': False, 'B11': False, 'B20': True, 'D0': False, 'D1': True}, {'B21': True, 'B10': False, 'B11': False, 'B20': True, 'D0': False, 'D1': True}, {'B10': False, 'B11': True, 'B20': False, 'B21': True, 'D0': False, 'D1': False}, {'B11': False, 'B10': True, 'B20': False, 'B21': True, 'D0': False, 'D1': False}, {'B11': True, 'B10': True, 'B20': False, 'B21': True, 'D0': False, 'D1': False}]
        |-- [(B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2) | (D o B2 & ! D i B1))]: [{'B10': False, 'B11': False, 'B20': False, 'B21': False, 'D0': False, 'D1': True}, {'D1': False, 'B10': False, 'B11': False, 'B20': False, 'B21': True, 'D0': False}, {'D1': True, 'B10': False, 'B11': False, 'B20': False, 'B21': True, 'D0': False}, {'B21': False, 'B10': False, 'B11': False, 'B20': True, 'D0': False, 'D1': True}, {'B21': True, 'B10': False, 'B11': False, 'B20': True, 'D0': False, 'D1': True}, {'B10': False, 'B11': True, 'B20': False, 'B21': True, 'D0': False, 'D1': False}, {'B11': False, 'B10': True, 'B20': False, 'B21': True, 'D0': False, 'D1': False}, {'B11': True, 'B10': True, 'B20': False, 'B21': True, 'D0': False, 'D1': False}]
        |-- [(B1(BOOT) & B2(BOOT) & D(DL_IMAGE) & B1 < B2) & ((B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2) | (D o B2 & ! D i B1))))]: [{'B10': False, 'B11': False, 'B20': True, 'B21': False, 'D0': False, 'D1': True}]
        |-- [exist ['B1', 'B2', 'D'] . B1(BOOT) & B2(BOOT) & D(DL_IMAGE) & B1 < B2 & (B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2) | (D o B2 & ! D i B1))]: [{}]
        |-- [~(exist ['B1', 'B2', 'D'] . B1(BOOT) & B2(BOOT) & D(DL_IMAGE) & B1 < B2 & (B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2) | (D o B2 & ! D i B1))))]: []

[INFO]: Specification result is False

########################################################################### (FINAL STATE) ###########################################################################
[EXECUTION]: [['begin', 1, 'BOOT'], ['begin', 2, 'DL_IMAGE'], ['end', 1], ['end', 2], ['begin', 3, 'BOOT'], ['end', 3]]

[PROPERTY]: ! exist ['B1', 'B2', 'D'] . B1(BOOT) & B2(BOOT) & D(DL_IMAGE) & B1 < B2 & (B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & ! D i B2) | (D o B2 & ! D i B1))

    |-- [X]: []
    |-- [XX]: [{'_X1': False, '_X0': False}, {'_X1': True, '_X0': False}, {'_X0': True, '_X1': False}]
    |-- [XY]: []
    |-- [XYY]: []
    |-- [XYYX]: []
    |-- [XYX]: []
    |-- [XYXY]: [{'_X0': False, '_X1': False, '_Y0': False, '_Y1': True}]
    |-- [XXY]: []
    |-- [XXYY]: [{'_X0': False, '_Y0': True, '_Y1': False}]
    |-- [XD]: [{'_X0': False, '_X1': False, '_D0': False}, {'_X0': False, '_X1': True, '_D0': True}, {'_X0': True, '_X1': False, '_D0': False}]
############################################################################# (THE END) #############################################################################

[INFO]: Specification result is False

```

# Contributors:
* [Klaus Havelund](http://www.havelund.com/), Jet Propulsion Laboratory/NASA, USA
* [Doron Peled](https://u.cs.biu.ac.il/~doronp/), Bar Ilan University, Israel
* Moran Omer, Bar Ilan University, Israel
