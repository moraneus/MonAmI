# MonAmI - Monitoring Allen logic

## General Introduction: ##
* MonAmI is a Python library for monitoring the foATL (First Order Allen Temporal Logic). FoATL is an extension of Allen's temporal logic.
* MonAmI formed by events, by checking them against a FoATL property. 

## Types of Allen's interval algebra: ##

![Image of Inervals](https://www.researchgate.net/profile/Ioannis_Tsamardinos/publication/230561978/figure/fig2/AS:646067146223617@1531045819115/1-The-13-relations-between-intervals-in-Allens-algebra-Interval-A-is-always-either-at.png)
* Allen's Temporal Intervals (James F. Allen, Maintaining Knowledge About Temporal Intervals, Communications of the ACM, 26 (11), 832–843).
* __NOTE: The only relations used by the FoATL algorithm, for now, are: `before`, `overlaps`, and `includes`.__


## Implementation ##
* The tool works with Python > 3.6, and it uses the 'dd' package, which can generate and manipulate BDDs (https://github.com/tulip-control/dd).
* To achieve more efficiency, 'dd' uses Cython to bindings the C CUDD library (`dd.cudd`), used by MonAmI.
* The BDDs are used to represent Boolean functions. BDDs can be considered a compressed representation of sets of relations (https://en.wikipedia.org/wiki/Binary_decision_diagram).


### General characterization of MonAmI: ### 
1. A trace is a sequence of `begin(i, d)` or `end(i)` events where `i` is denoted for an interval ID and `d` denotes data.
2. For each event:
    1. Interval id and data, if relevant, enumerate into 2^k size bit-string.
    2. All the BDDs in {`X`, `XX`, `XY`, `XYY`, `XYYX`, `XXY`, `XXYY`, `XYX`, `XYXY`, `XD`}, represent what we have seen so far, are updated due to the new event.
    3. The specification is evaluated due to this event and the BDDs current state.
    4. MonAmI output created according to the mode defined by the user.
    
### The CODE Structure: ###
The main tree of the code which contains several parts and classes which any one of them has a specific goal.

|-- `exceptions` folder (contains the interval and specification exceptions). \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `exception.py` \
|-- `experiments` folder (Contains tools experiments folders). \
|-- `fronted` folder (Contains the property parser and satisfiability methods). \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `parser.py` \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `ast.py` \
|-- `graphics` folder (UI, responsable to console prints). \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `io.py` \
|-- `input` folder (As described above). \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `configuration` (Primary configuration file)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `data` (Data for trace generator) \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `property` (Property for evaluate) \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `rules` (Rules for trace generator) \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `trace` (Trace for monitoring) \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `trace_generator.py` \
|-- `logic` folder (Contains the classes are needed for the BDD construction). \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `bdd_atl.py` (Main class of BDDs update) \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `list_atl.py` (Version with sets instead of BDDs) \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `bitstring_table.py` (Enumarate the bitstrings) \
|-- `tests` folder (Contains several tests classes). \
|-- `monami.py` (Tool entry point, main function).


### Input Files: ###
#### Trace File: ####
1. Setting any execution for monitoring can be done by edit the `trace` file under the `input` folder or creating a new file.
2. Note: The path to the `trace` file should be updated into the configuration file, as will describe below.
3. Each event is from the type `[Event type, Interval ID, Data]` for `begin` event and `[Event type, Interval ID`]` for an 'end' event.

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

##### Create Random Trace File #####
1. You can create a random execution in the `trace` file using the script `trace_generator.py`, located in the`input` folder.
2. The trace_generator.py gets as input a `data` and `rules` files which are a JSON type.
3. It also needs to get as arguments num of intervals, output filename, the percentage of rules cover in the trace, and the maximum depth of the intervals.
4. Examples of how to call the trace generator script:
```python
# "rules" - rules filename.
# "data" - data filename.
# 500 - trace with 500 intervals (or 1000 events).
# "output.json" - output filename.
# 30 - Percentage cover of rules in the trace.
# 3 - The maximum depth on intervals.

trace_generator = TraceGenerator("rules", "data", 500, 'output.json', 30, 3)
trace_generator.start()
```

###### Data file ######
1. contain all the optional data that could appear in the trace.
2. Example of a data file:
```json
["BOOT", "DL_IMAGE", "DL_MOBPRM", "DL_ARMPRM", "DL_FAIL", "INS_ON", "INS_FAIL", "INS_RECOVER", "GET_CAMDATA", "STARVE"]
```
###### Rules File ######
1. Contain all the rules which are the basis of trace creation.
2. Rule is defined using a dictionary of dictionaries, where any inner dictionary defined an interval.
3. Any inner dictionary has a key; The keys start from "0", "1", and so on. It contains the data of the interval and the indexes where the interval starts and stops.
4. Rule files can include as many rules as needed with the limit of the trace size.
   
2. Example of `rule` file with two rules:
```json
[
        {
            "0": {"DATA": "BOOT", "B_PRIORITY": 0, "E_PRIORITY": 2},
            "1": {"DATA": "DL_IMAGE", "B_PRIORITY": 1, "E_PRIORITY": 3},
            "2": {"DATA": "BOOT", "B_PRIORITY": 4, "E_PRIORITY": 5}
        },
        {
            "0": {"DATA": "DL_ARMPRM", "B_PRIORITY": 0, "E_PRIORITY": 3},
            "1": {"DATA": "DL_FAIL", "B_PRIORITY": 1, "E_PRIORITY": 2}
        }
]
```

#### Property File: ####
1. Creating your own property can be made by edit the `property` file under the `input folder` or creating a new file.
2. Note: The path to the `property` file should be updated into the configuration file, as will describe below.
3. Example of `property` file:
```json
{
    "property": "!exist B1, B2, D . B1('BOOT') & B2('BOOT') & D('DL_IMAGE') & B1 < B2 & (B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & !D i B2) | (D o B2 & !D i B1))"
}
```
#### Configuration File: ####
1. In the `configuration` file, there are parameters that can be edited by the user:
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

### MonAmi parser ###
The parser parses one formula according to the following grammar.

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

Operator          | Meaning
----------------- | -------------
<code> &#124; </code>    | OR
`&`               | AND
`->`              | IMPLIES
`!`               | NOT
`A < B`           | A Before B 
`A o B`               | A Overlaps B
`A i B`               | A Includes B
`A('BOOT')`       | `True` if A data is 'BOOT', otherwise `False`
`same(A, B)`      | `True` if A, B have the same data , otherwise `False`
`exist`           | exist quantifier
`forall`          | forall quantifier
`(` `)`           | Bracket



The Boolean binary operators have precedence as follows: 
`|` and `->` have the same precedence, which is weaker than
the precedence of `&`, which is weaker than the precedence of 
`!`. So for example:

```
A < B & C < D | ! E < F & G < H
```

has the same meaning as this formula:

```
(A < B & C < D) | ((! E < F) & G < H)
```


## Installation: ##
1. Before execution, it needs to install python 3.6 and above.
2. In the file `requierments.txt`, there are all the packages that should be install. \
For installation, please run the command `python3 -m pip install -r requierments.txt` (from CMD in windows or Terminal in Unix). Make sure that `python3` points to your Python > 3.6 version.
3. Running the program is made by running the command `python monami.py` from the program root directory.
4. To use dd.cudd (Cython binding to the CUDD C library) interface, please look at the instruction at https://github.com/tulip-control/dd#installation.

### Troublshoting ###
#### Import error while trying to execute the tool ####
1. Change directory to the MonAmI root directory.
2. Type ``` export PYTHONPATH=$PYTHONPATH:`pwd` ``` and press enter.
#### Install CUDD on MAC ####
##### General #####
When we try to install the `dd.cudd` module in macOS laptops, we had some errors.
That probably caused due to an `SSL: CERTIFICATE_VERIFY_FAILED` error while the installation process tried to download the cudd package at first.
We manually downloaded the package and edited one of the `dd` files before installing to avoid this error.

##### Instructions #####
1. `sudo python3 -m pip download dd --no-deps`
2. `tar xzf dd-*.tar.gz`
3. `cd dd-*`
4. From https://sourceforge.net/projects/cudd-mirror/ download the cudd package.
5. Move the file (`cudd-3.0.0.tar.gz`) to the `dd-*` folder.
6. In the `dd-*` folder edit `download.py`:
   1. Replace the line: `fname = fetch(CUDD_URL, CUDD_SHA256)`
	with this line: `fname = "cudd-3.0.0.tar.gz"`
      (It is nearly at the end of the file).
6. `python3 setup.py install.

## Example of execution output in debug mode: ##
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
We chose `"MODE": "VIOLATION"` since we want to check whether a violation occured.
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


## Some epxeriments results: ##
As part of the testing process of MonAmI, we performed several experiments that tested the correctness of the tool and its performance - the time that it takes and the allocated memory during the execution. 
We created trace files in different sizes of events (1000, 2000, 4000, 8000, 16000). 
These files were created with the trace generator script.
We compare MonAmI to nfer tool ([nfer in C](http://nfer.io), [nfer in Scala](https://github.com/havelund)).


```json
{
    "1": "!exist B1, B2, D . B1('BOOT') & B2('BOOT') & D('DL_IMAGE') & B1 < B2 & (B1 i D | B2 i D | (B1 < D & D < B2) | (B1 o D & !D i B2) | (D o B2 & !D i B1))",
    "2": "!exist D, F . (D('DL_MOBPRM') | D('DL_ARMPRM')) & F('DL_FAIL') & D i F",
    "3": "!exist O, F, R . O('INS_ON') & F('INS_FAIL') & R('INS_RECOVER') & O < F & F < R & !exist X . (X('INS_ON') | X('INS_RECOVER')) & O < X & X < R",
    "4": "!exist D, G, S . D('DL_IMAGE') & G('GET_CAMDATA') & S('STARVE') & D i S & G i S"
}
```

To demonstrate some of the experiment results, we took the above 4 examples properties.


![image](https://user-images.githubusercontent.com/48603901/117803681-949ebb80-b25f-11eb-804b-3551995cf072.png)

