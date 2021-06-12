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
MonAmI is a Python library for monitoring the foATL (First-Order Allen Temporal Logic), which is an extension of [Allen's temporal logic](https://en.wikipedia.org/wiki/Allen%27s_interval_algebra). \
MonAmI formed by events, by checking them against a FoATL property. \
An example of a FoATL property is the following (Benign Telemetry Transmission Error):
```json
{
    "property": "!exist D, F . (D('DL_MOBPRM') | D('DL_ARMPRM')) & F('DL_FAIL') & D i F"
}
```
The property states that there is not exist D and F intervals (`!exist D, F`) such that (`.`) D with data DL_MOBPRM (`D('DL_MOBPRM'`) or (`|`) D with DL_ARMPRM data includes (`i`) F interval with DL_FAIL data. \
Another way of seeing this is that there is no DL_FAIL interval during a DL_MOBPRM or DL_ARMPRM interval. \
The implementation uses [BDDs (Binary Decision Diagrams)](https://en.wikipedia.org/wiki/Binary_decision_diagram) for representing assignments to quantified variables with their data (such as D('DL_MOBPRM')) and for the Allen's intervals (such as D i F).

# Installing MonAmI
The directly out contains files and directories useful for installing and running MonAmI:
* ast: A directory containing python script which helps to understand the AST structure.
* examples: An example directory containing properties, traces and other files.
* guides: A directory containing other guides such as using the trace_generator.py.
* papers: A directory containing papers published about MonAmI.
  
MonAmI is implemented in Python.
1. Install Python 3.7 and above (We used Python 3.9).
2. Download MonAmI project to your PC.
3. Run the command `python3 -m pip install -r requierments.txt` (from CMD in windows or Terminal in Unix). Make sure that `python3` points to your Python > 3.7 version.
4. To use dd.cudd (Cython binding to the CUDD C library) interface, follow the instruction at https://github.com/tulip-control/dd#installation \
(__Note: For significant executions, dd.cudd is necessary__)
   
# Running MonAmI
1. CD to MonAmI root directory.
2. Type ``` export PYTHONPATH=$PYTHONPATH:`pwd` ``` and press enter (Only in the first execution).   
3. Running MonAmI is made by executes the command `python3 monami.py`. Make sure that `python3` points to your Python > 3.7 version.
4. Before running, you must change the `configuration` file according to your environment and needs.

### Configuration File: ###
1. The `configuration` file contains the arguments that are needed for MonAmI:
    1. `DEBUG` - If true, the program will print into console messages that describe the BDDs state for each event.
    2. `INTERVAL_SIZE` - Initial length of the enumeration of interval.
       1. `int` - Set the initial size to be as the specified value.
       2. `AUTO` - Set the initial value to match the size of the trace (expansion will not happen).
    3. `DATA_SIZE` - Initial length of the enumeration of data.
       1. `int` - Set the initial size to be as the specified value.
       2. `AUTO` - Set the initial value to match the size of the trace (expansion will not happen).
    4. `EXPANSION_LENGTH` - The expansion length when an enumeration needs to grow.
    5. `MODE` - Define the mode of operation of MonAmI, In which cases it will stop from running.
       1. `VIOLATION` - MonAmI will stop when the property eval result is False.
       2. `SATISFACTION` - MonAmI will stop when the property eval result is True.
       3. `CONTINUE-SMALL` - MonAmI evaluates the property after every event until the end of the trace.
       4. `CONTINUE-BIG` - MonAmi evaluates the property once at the end of the trace.
    6. `TRACE` - Path to the `trace` file you have.
    7. `PROPERTY` - Path to the `property` file you have.
    
Parameter         | Details
----------------- | -------------
`DEBUG`           | `true` or `false`
`INTERVAL_SIZE`   | `int` or `AUTO`
`DATA_SIZE`       | `int` or `AUTO`
`EXPANSION_LENGTH`| `int`
`MODE`            | `VIOLATION`, `SATISFACTION`, `CONTINUE-SMALL` or `CONTINUE-BIG`
`TRACE`           | `str`
`PROPERTY`        | `str`
2. Example of 'configuration` file:
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
`true`, `false`                     | A boolean value of `true` and `false` 
<code> p &#124; q </code>           | `p OR q`
`p & q`                             | `p AND q`
`p -> q`                            | `p IMPLIES q`
`!p`                                | `NOT p`
`A < B`                             | `A Before B` 
`A o B`                             | `A Overlaps B`
`A i B`                             | `A Includes B`
`A(d)`                              | Denote that the data of the interval assigned to the variable `A` has the constant value `d`
`same(A, B)`                        | Verify whether two intervals `A` and `B` carry the `same` value
`exist A . p(A)`                    | There exists an `A` such that `p(A)`
`forall A . p(A)`                   | For all `A`, `p(A)`  
`(<formula>)`                       | `<formula>`

### Example Properties ###
* #### Double Boot ####
    * ```!exist B1, B2, D . B1('BOOT') & B2('BOOT') & D('DL_IMAGE') & B1 < B2 & (B1 i D | B2 i D) | (B1 < D & D < B2) | (B1 o D & !D i B2) | (D o B2 & !D i B1))"```
    * One particular concern in this case is whether there is a downlink operation during an interval where the flight 
      computer reboots twice. This scenario could cause a potential loss of downlink information.

* #### Benign Instrument Power-on Failure
    * ```"!exist O, F, R . O('INS_ON') & F('INS_FAIL') & R('INS_RECOVER') & O < F & F < R & !exist X . (X('INS_ON') | X('INS_RECOVER')) & O < X & X < R"```
    * In this case, an instrument power-on command (`INS_ON`) fails (`INS_FAIL`) and then recovers (`INS_RECOVER`). 
      Since the behavior is predictable, and benign, the warning is labeled as being expected.
* #### Benign Task Starvation during Overlap of Commands
    * ```"!exist D, G, S . D('DL_IMAGE') & G('GET_CAMDATA') & S('STARVE') & D i S & G i S"```
    * This property labels a situation in which a warning about task starvation (`STARVE`) is expected whenever an 
      activity (`GET_CAMDATA`) which fetches data products from the cameras overlaps with an Earth image communication activity (`DL_IMAGE`).



# The MonAmI Trace Language
In order to execute MonAmI, it needs to get the trace in a valid language format.
* A trace in a sequence of events.
* An interval is a pair of events - `begin` and `end` events. 
  
Each event is from the type `[Event type, Interval ID, Data]` for `begin` event and `[Event type, Interval ID]` for an `end` event.

Parameter     | Details
------------- | -------------
Event Type    | `"begin"` or `"end"` only
Interval ID   | `int`, `str`
Data          | `null`, `int`, or `str`

4. Example of short `trace` file:
```json
{
    "execution": [["begin", 1, "BOOT"], ["begin", 2, "DL_IMAGE"], ["end", 1], ["end", 2], ["begin", 3, "BOOT"], ["end", 3]]
}
```

# MonAmI Execution Output Example (in debug mode): 
Debug mode is good for short traces.
* Assume the property:
```json
{
    "property": "!exist B1, B2, D . B1('BOOT') & B2('BOOT') & D('DL_IMAGE') & B1 < B2 & (B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & !D i B2) | (D o B2 & !D i B1))"
}
```
* Assume the trace:
```json
{
    "execution": [["begin", 1, "BOOT"], ["begin", 2, "DL_IMAGE"], ["end", 1], ["end", 2], ["begin", 3, "BOOT"], ["end", 3]]
}
```
* And assume the configuration file:
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
We chose `"MODE": "VIOLATION"` since we want to check whether a violation occurred.
In the example, the property will violate only at the last event. \
`"INTERVAL_SIZE": "AUTO"` will set the interval bitstring size into 2, since with 2 bits, we can represent four different intervals (00, 01, 10, 11). \
`"DATA_SIZE": 1` is good enough since that 1 bit can define two distinct data values, and in our example, we have only two.

In debug mode, after each event, the program will print out to console the updated BDDs.
* It also prints out other information like bitstring expansion if it happened and the mapping between intervals and data to bitstrings.
* The final state will be print at the end of the execution.

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