# MonAmI - Monitoring Allen logic

## General Details: ##
* This tool was fully written in python using 'dd' package (Repository of 'dd' is at https://github.com/tulip-control/dd).
* It implements a monitoring version of Allen's interval algebra using BDDs.
* BDDs are used to represent Boolean functions. On a more abstract level, BDDs can be considered as a compressed representation of sets or relations (Wikipedia:  https://en.wikipedia.org/wiki/Binary_decision_diagram).

## Types of Allen's interval algebra: ##
![Image of Inervals](https://www.researchgate.net/profile/Ioannis_Tsamardinos/publication/230561978/figure/fig2/AS:646067146223617@1531045819115/1-The-13-relations-between-intervals-in-Allens-algebra-Interval-A-is-always-either-at.png) /
* __NOTE: The only relations used by the algorithm for now are: `before`, `overlaps`, and `includes`.__


## General characterization of MonAmI: ## 
1. A trace is a sequence of `begin(i, d)` or `end(i)` events where `i` is denoted for an interval ID and `d` denotes data. / 
* __NOTE: For `end` event, data is not mandatory since the data is set on the `begin` event.__
3. For each event:
    1. All possible Allen intervals are created, as these sets (`X`, `XX`, `XY`, `XYY`, `XYYX`, `XXY`, `XXYY`, `XYX`, `XYXY`, `XD`), represented as BDDs.
    2. The temporal logic formula is evaluated on these intervals.

## Installation: ##
1. Before execution, it needs to install python 3.6 and above.
2. In the file `requierments.txt`, there are all the packages that should be installed. \
For installation, please run the command `python -m pip install -r requierments.txt` (from CMD in windows or Terminal in Unix).
3. Running the program is made by running the command `python main.py` from the program root directory.

## Configuration: ##
### Trace input: ###
1. Setting any execution for monitoring can be done by edit the `trace` file under the `input` folder.
2. Each event is from the type `[Event type, Interval ID, Data]` for `begin` event and `[Event type, Interval ID] for an 'end' event.

Parameter     | Details
------------- | -------------
Event Type    | `"begin"` or `"end"` only
Interval ID   | `int`, `str`
Data          | `null`, `int`, or `str`

3. You can create a random execution in the `trace` file using the script `trace_generator.py`, which is locate in the`input` folder.
4. Example of `trace` file:
```json
{
    "execution": [["begin", 1, "Data1"], ["end", 1], ["begin", 2, "Data2"], ["end", 2], ["begin", 3, "Data3"], ["end", 3],
    ["begin", 4, "Data4"], ["begin", 5, "Data5"], ["end", 5], ["end", 4]]
}
```

### Property Input: ###
1. Creating your own property can be made by edit the `property` file under the `input folder`.
2. Here are some examples of properties:
```json
1. exist A, B, C .
   A("load") &
   B("boot") &
   C("boot") &
   A i B &
   A i C &
   B < C
  
2. exist A, B, C, D, E, F, G, H . A < B & C < D | ! E < F & G < H

3. exist A, B, C, D, E . A < B -> (C i D & E o F)

```

3. __Note that free variables are not allowed:__
```json
A < B & B i C & C o D
-------------------------
*** Error - the formula has free variables: {'C', 'B', 'A', 'D'}
*** Error - formula parses but is not well formed!


exist A, B . A < B & B i C & exist D . C o D
-------------------------
*** Error - the formula has free variables: {'C'}
*** Error - formula parses but is not well formed!
```
4. Example of `property` file:
```json
{
    "property": "exist A, B, C, D, E . (A < B & B < C) & A('Data1') & B('Data2') & C('Data3') & D i E"
}
```

### Algorithm params: ###
1. In the `configuration` file, there are few parameters that can be changed:
    1. `DEBUG` - If true, the program will print into console messages that describe the BDDs state for each event.
    2. `INTERVAL_SIZE` - Initial length of the enumeration of interval.
    3. `DATA_SIZE` - Initial length of the enumeration of data.
    4. `EXPANSION_LENGTH` - The expansion length when an enumeration needs to grow.
    
Parameter         | Details
----------------- | -------------
`DEBUG`           | `true` or `false`
`INTERVAL_SIZE`   | `int`
`DATA_SIZE`       | `int`
`EXPANSION_LENGTH`| `int`




## The CODE Structure: ##
The code contains several parts and classes which any one of them had a specific goal.

|-- `exceptions` folder (contains the interval and specification exceptions). \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `exception.py` \
|-- `fronted` folder (Contains the property parser and satisfiability methods). \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `parser.py` \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `ast.py` \
|-- `graphics` folder (UI, responsable to console prints). \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `colors.py` \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `io.py` \
 |-- `input` folder (As described above). \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `configuration` \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `property` \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `trace` \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `trace_generator.py` \
 |-- `logic` folder (Contains the classes are needed for the BDD construction). \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `bdd_atl.py` (Main class of BDDs update) \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `list_atl.py` (Version with sets instead of BDDs) \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `bitstring_table.py` (Enumarate the bitstrings) \
 |-- `tests` folder (Contains several tests classes). \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `test_before_relation.py` \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `test_data_bdds.py` \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `test_during_relation.py` \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `test_helper.py` \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `test_interval_exceptions.py` \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `test_mixed_relation.py` \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `test_overlap_relation.py` \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `test_specification_satisfaction.py` \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `time_execution_compare.py` (Compare time between BDDs and Sets version)






## BDD implementation execution output in debug mode: ##
* The output will match the `JSON` example above.
* In debug mode, after each event, the program will print out to console the updated BDDs.
* It also prints out other information like bitstring expansion.
* The final state will be print at the end of the execution.
```python

                                                       ███╗   ███╗ ██████╗ ███╗   ██╗ █████╗ ███╗   ███╗██╗
                                                       ████╗ ████║██╔═══██╗████╗  ██║██╔══██╗████╗ ████║██║
                                                       ██╔████╔██║██║   ██║██╔██╗ ██║███████║██╔████╔██║██║
                                                       ██║╚██╔╝██║██║   ██║██║╚██╗██║██╔══██║██║╚██╔╝██║██║
                                                       ██║ ╚═╝ ██║╚██████╔╝██║ ╚████║██║  ██║██║ ╚═╝ ██║██║
                                                       ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝
                                                    

############################################################################## (START) ##############################################################################
[EXECUTION]: [['begin', 1, 'Data1'], ['end', 1], ['begin', 2, 'Data2'], ['end', 2], ['begin', 3, 'Data3'], ['end', 3], ['begin', 4, 'Data4'], ['begin', 5, 'Data5'], ['end', 5], ['end', 4]]

[PROPERTY]: exist ['A', 'B', 'C', 'D', 'E'] . (A < B & B < C) & A(Data1) & B(Data2) & C(Data3) & D i E

|-- [ENUMERATION]: 1 -> "000" ([False, False, False])
|-- [ENUMERATION]: Data1 -> "000" ([False, False, False])
|-- [EVENT]: begin(1, Data1)
    |-- [X]: [{'_X0': False, '_X1': False, '_X2': False}]
    |-- [XX]: []
    |-- [XY]: []
    |-- [XYY]: []
    |-- [XYYX]: []
    |-- [XYX]: []
    |-- [XYXY]: []
    |-- [XXY]: []
    |-- [XXYY]: []
    |-- [XD]: [{'_X0': False, '_X1': False, '_X2': False, '_D0': False, '_D1': False, '_D2': False}]
    |-- [AST]:
        |-- [A < B]: []
        |-- [B < C]: []
        |-- [(A < B) & (B < C))]: []
        |-- [(A < B & B < C)]: []
        |-- [A(Data1)]: [{'A0': False, 'A1': False, 'A2': False}]
        |-- [((A < B & B < C)) & (A(Data1)))]: []
        |-- [B(Data2)]: []
        |-- [((A < B & B < C) & A(Data1)) & (B(Data2)))]: []
        |-- [C(Data3)]: []
        |-- [((A < B & B < C) & A(Data1) & B(Data2)) & (C(Data3)))]: []
        |-- [D i E]: []
        |-- [((A < B & B < C) & A(Data1) & B(Data2) & C(Data3)) & (D i E))]: []
        |-- [exist ['A', 'B', 'C', 'D', 'E'] . (A < B & B < C) & A(Data1) & B(Data2) & C(Data3) & D i E]: []

[INFO]: Specification result is False

|-- [ENUMERATION]: 1 -> "000" ([False, False, False])
|-- [EVENT]: end(1)
    |-- [X]: []
    |-- [XX]: [{'_X0': False, '_X1': False, '_X2': False}]
    |-- [XY]: []
    |-- [XYY]: []
    |-- [XYYX]: []
    |-- [XYX]: []
    |-- [XYXY]: []
    |-- [XXY]: []
    |-- [XXYY]: []
    |-- [XD]: [{'_X0': False, '_X1': False, '_X2': False, '_D0': False, '_D1': False, '_D2': False}]
    |-- [AST]:
        |-- [A < B]: []
        |-- [B < C]: []
        |-- [(A < B) & (B < C))]: []
        |-- [(A < B & B < C)]: []
        |-- [A(Data1)]: [{'A0': False, 'A1': False, 'A2': False}]
        |-- [((A < B & B < C)) & (A(Data1)))]: []
        |-- [B(Data2)]: []
        |-- [((A < B & B < C) & A(Data1)) & (B(Data2)))]: []
        |-- [C(Data3)]: []
        |-- [((A < B & B < C) & A(Data1) & B(Data2)) & (C(Data3)))]: []
        |-- [D i E]: []
        |-- [((A < B & B < C) & A(Data1) & B(Data2) & C(Data3)) & (D i E))]: []
        |-- [exist ['A', 'B', 'C', 'D', 'E'] . (A < B & B < C) & A(Data1) & B(Data2) & C(Data3) & D i E]: []

[INFO]: Specification result is False

|-- [ENUMERATION]: 2 -> "001" ([False, False, True])
|-- [ENUMERATION]: Data2 -> "001" ([False, False, True])
|-- [EVENT]: begin(2, Data2)
    |-- [X]: [{'_X0': False, '_X1': False, '_X2': True}]
    |-- [XX]: [{'_X0': False, '_X1': False, '_X2': False}]
    |-- [XY]: []
    |-- [XYY]: []
    |-- [XYYX]: []
    |-- [XYX]: []
    |-- [XYXY]: []
    |-- [XXY]: [{'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': False, '_Y2': True}]
    |-- [XXYY]: []
    |-- [XD]: [{'_X0': False, '_X1': False, '_X2': False, '_D0': False, '_D1': False, '_D2': False}, {'_X0': False, '_X1': False, '_X2': True, '_D0': False, '_D1': False, '_D2': True}]
    |-- [AST]:
        |-- [A < B]: []
        |-- [B < C]: []
        |-- [(A < B) & (B < C))]: []
        |-- [(A < B & B < C)]: []
        |-- [A(Data1)]: [{'A0': False, 'A1': False, 'A2': False}]
        |-- [((A < B & B < C)) & (A(Data1)))]: []
        |-- [B(Data2)]: [{'B0': False, 'B1': False, 'B2': True}]
        |-- [((A < B & B < C) & A(Data1)) & (B(Data2)))]: []
        |-- [C(Data3)]: []
        |-- [((A < B & B < C) & A(Data1) & B(Data2)) & (C(Data3)))]: []
        |-- [D i E]: []
        |-- [((A < B & B < C) & A(Data1) & B(Data2) & C(Data3)) & (D i E))]: []
        |-- [exist ['A', 'B', 'C', 'D', 'E'] . (A < B & B < C) & A(Data1) & B(Data2) & C(Data3) & D i E]: []

[INFO]: Specification result is False

|-- [ENUMERATION]: 2 -> "001" ([False, False, True])
|-- [EVENT]: end(2)
    |-- [X]: []
    |-- [XX]: [{'_X0': False, '_X1': False}]
    |-- [XY]: []
    |-- [XYY]: []
    |-- [XYYX]: []
    |-- [XYX]: []
    |-- [XYXY]: []
    |-- [XXY]: []
    |-- [XXYY]: [{'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': False, '_Y2': True}]
    |-- [XD]: [{'_X0': False, '_X1': False, '_X2': False, '_D0': False, '_D1': False, '_D2': False}, {'_X0': False, '_X1': False, '_X2': True, '_D0': False, '_D1': False, '_D2': True}]
    |-- [AST]:
        |-- [A < B]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True}]
        |-- [B < C]: [{'B0': False, 'B1': False, 'B2': False, 'C0': False, 'C1': False, 'C2': True}]
        |-- [(A < B) & (B < C))]: []
        |-- [(A < B & B < C)]: []
        |-- [A(Data1)]: [{'A0': False, 'A1': False, 'A2': False}]
        |-- [((A < B & B < C)) & (A(Data1)))]: []
        |-- [B(Data2)]: [{'B0': False, 'B1': False, 'B2': True}]
        |-- [((A < B & B < C) & A(Data1)) & (B(Data2)))]: []
        |-- [C(Data3)]: []
        |-- [((A < B & B < C) & A(Data1) & B(Data2)) & (C(Data3)))]: []
        |-- [D i E]: []
        |-- [((A < B & B < C) & A(Data1) & B(Data2) & C(Data3)) & (D i E))]: []
        |-- [exist ['A', 'B', 'C', 'D', 'E'] . (A < B & B < C) & A(Data1) & B(Data2) & C(Data3) & D i E]: []

[INFO]: Specification result is False

|-- [ENUMERATION]: 3 -> "010" ([False, True, False])
|-- [ENUMERATION]: Data3 -> "010" ([False, True, False])
|-- [EVENT]: begin(3, Data3)
    |-- [X]: [{'_X0': False, '_X1': True, '_X2': False}]
    |-- [XX]: [{'_X0': False, '_X1': False}]
    |-- [XY]: []
    |-- [XYY]: []
    |-- [XYYX]: []
    |-- [XYX]: []
    |-- [XYXY]: []
    |-- [XXY]: [{'_X0': False, '_X1': False, '_Y0': False, '_Y1': True, '_Y2': False}]
    |-- [XXYY]: [{'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': False, '_Y2': True}]
    |-- [XD]: [{'_X0': False, '_X1': False, '_X2': False, '_D0': False, '_D1': False, '_D2': False}, {'_X0': False, '_X1': False, '_X2': True, '_D0': False, '_D1': False, '_D2': True}, {'_X0': False, '_X1': True, '_X2': False, '_D0': False, '_D1': True, '_D2': False}]
    |-- [AST]:
        |-- [A < B]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True}]
        |-- [B < C]: [{'B0': False, 'B1': False, 'B2': False, 'C0': False, 'C1': False, 'C2': True}]
        |-- [(A < B) & (B < C))]: []
        |-- [(A < B & B < C)]: []
        |-- [A(Data1)]: [{'A0': False, 'A1': False, 'A2': False}]
        |-- [((A < B & B < C)) & (A(Data1)))]: []
        |-- [B(Data2)]: [{'B0': False, 'B1': False, 'B2': True}]
        |-- [((A < B & B < C) & A(Data1)) & (B(Data2)))]: []
        |-- [C(Data3)]: [{'C0': False, 'C1': True, 'C2': False}]
        |-- [((A < B & B < C) & A(Data1) & B(Data2)) & (C(Data3)))]: []
        |-- [D i E]: []
        |-- [((A < B & B < C) & A(Data1) & B(Data2) & C(Data3)) & (D i E))]: []
        |-- [exist ['A', 'B', 'C', 'D', 'E'] . (A < B & B < C) & A(Data1) & B(Data2) & C(Data3) & D i E]: []

[INFO]: Specification result is False

|-- [ENUMERATION]: 3 -> "010" ([False, True, False])
|-- [EVENT]: end(3)
    |-- [X]: []
    |-- [XX]: [{'_X2': False, '_X0': False, '_X1': False}, {'_X2': True, '_X0': False, '_X1': False}, {'_X0': False, '_X1': True, '_X2': False}]
    |-- [XY]: []
    |-- [XYY]: []
    |-- [XYYX]: []
    |-- [XYX]: []
    |-- [XYXY]: []
    |-- [XXY]: []
    |-- [XXYY]: [{'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': False, '_Y2': True}, {'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': True, '_Y2': False}, {'_X0': False, '_X1': False, '_X2': True, '_Y0': False, '_Y1': True, '_Y2': False}]
    |-- [XD]: [{'_X0': False, '_X1': False, '_X2': False, '_D0': False, '_D1': False, '_D2': False}, {'_X0': False, '_X1': False, '_X2': True, '_D0': False, '_D1': False, '_D2': True}, {'_X0': False, '_X1': True, '_X2': False, '_D0': False, '_D1': True, '_D2': False}]
    |-- [AST]:
        |-- [A < B]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True}, {'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': True, 'B2': False}, {'A0': False, 'A1': False, 'A2': True, 'B0': False, 'B1': True, 'B2': False}]
        |-- [B < C]: [{'B0': False, 'B1': False, 'B2': False, 'C0': False, 'C1': False, 'C2': True}, {'B0': False, 'B1': False, 'B2': False, 'C0': False, 'C1': True, 'C2': False}, {'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True, 'C2': False}]
        |-- [(A < B) & (B < C))]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True, 'C2': False}]
        |-- [(A < B & B < C)]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True, 'C2': False}]
        |-- [A(Data1)]: [{'A0': False, 'A1': False, 'A2': False}]
        |-- [((A < B & B < C)) & (A(Data1)))]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True, 'C2': False}]
        |-- [B(Data2)]: [{'B0': False, 'B1': False, 'B2': True}]
        |-- [((A < B & B < C) & A(Data1)) & (B(Data2)))]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True, 'C2': False}]
        |-- [C(Data3)]: [{'C0': False, 'C1': True, 'C2': False}]
        |-- [((A < B & B < C) & A(Data1) & B(Data2)) & (C(Data3)))]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True, 'C2': False}]
        |-- [D i E]: []
        |-- [((A < B & B < C) & A(Data1) & B(Data2) & C(Data3)) & (D i E))]: []
        |-- [exist ['A', 'B', 'C', 'D', 'E'] . (A < B & B < C) & A(Data1) & B(Data2) & C(Data3) & D i E]: []

[INFO]: Specification result is False

|-- [ENUMERATION]: 4 -> "011" ([False, True, True])
|-- [ENUMERATION]: Data4 -> "011" ([False, True, True])
|-- [EVENT]: begin(4, Data4)
    |-- [X]: [{'_X0': False, '_X1': True, '_X2': True}]
    |-- [XX]: [{'_X2': False, '_X0': False, '_X1': False}, {'_X2': True, '_X0': False, '_X1': False}, {'_X0': False, '_X1': True, '_X2': False}]
    |-- [XY]: []
    |-- [XYY]: []
    |-- [XYYX]: []
    |-- [XYX]: []
    |-- [XYXY]: []
    |-- [XXY]: [{'_X2': False, '_X0': False, '_X1': False, '_Y0': False, '_Y1': True, '_Y2': True}, {'_X2': True, '_X0': False, '_X1': False, '_Y0': False, '_Y1': True, '_Y2': True}, {'_X0': False, '_X1': True, '_X2': False, '_Y0': False, '_Y1': True, '_Y2': True}]
    |-- [XXYY]: [{'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': False, '_Y2': True}, {'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': True, '_Y2': False}, {'_X0': False, '_X1': False, '_X2': True, '_Y0': False, '_Y1': True, '_Y2': False}]
    |-- [XD]: [{'_X0': False, '_X1': False, '_X2': False, '_D0': False, '_D1': False, '_D2': False}, {'_X0': False, '_X1': False, '_X2': True, '_D0': False, '_D1': False, '_D2': True}, {'_X0': False, '_X1': True, '_X2': False, '_D0': False, '_D1': True, '_D2': False}, {'_X0': False, '_X1': True, '_X2': True, '_D0': False, '_D1': True, '_D2': True}]
    |-- [AST]:
        |-- [A < B]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True}, {'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': True, 'B2': False}, {'A0': False, 'A1': False, 'A2': True, 'B0': False, 'B1': True, 'B2': False}]
        |-- [B < C]: [{'B0': False, 'B1': False, 'B2': False, 'C0': False, 'C1': False, 'C2': True}, {'B0': False, 'B1': False, 'B2': False, 'C0': False, 'C1': True, 'C2': False}, {'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True, 'C2': False}]
        |-- [(A < B) & (B < C))]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True, 'C2': False}]
        |-- [(A < B & B < C)]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True, 'C2': False}]
        |-- [A(Data1)]: [{'A0': False, 'A1': False, 'A2': False}]
        |-- [((A < B & B < C)) & (A(Data1)))]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True, 'C2': False}]
        |-- [B(Data2)]: [{'B0': False, 'B1': False, 'B2': True}]
        |-- [((A < B & B < C) & A(Data1)) & (B(Data2)))]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True, 'C2': False}]
        |-- [C(Data3)]: [{'C0': False, 'C1': True, 'C2': False}]
        |-- [((A < B & B < C) & A(Data1) & B(Data2)) & (C(Data3)))]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True, 'C2': False}]
        |-- [D i E]: []
        |-- [((A < B & B < C) & A(Data1) & B(Data2) & C(Data3)) & (D i E))]: []
        |-- [exist ['A', 'B', 'C', 'D', 'E'] . (A < B & B < C) & A(Data1) & B(Data2) & C(Data3) & D i E]: []

[INFO]: Specification result is False

|-- [ENUMERATION]: 5 -> "100" ([True, False, False])
|-- [ENUMERATION]: Data5 -> "100" ([True, False, False])
|-- [EVENT]: begin(5, Data5)
    |-- [X]: [{'_X0': False, '_X1': True, '_X2': True}, {'_X0': True, '_X1': False, '_X2': False}]
    |-- [XX]: [{'_X2': False, '_X0': False, '_X1': False}, {'_X2': True, '_X0': False, '_X1': False}, {'_X0': False, '_X1': True, '_X2': False}]
    |-- [XY]: [{'_X0': False, '_X1': True, '_X2': True, '_Y0': True, '_Y1': False, '_Y2': False}]
    |-- [XYY]: []
    |-- [XYYX]: []
    |-- [XYX]: []
    |-- [XYXY]: []
    |-- [XXY]: [{'_X2': False, '_X0': False, '_X1': False, '_Y0': False, '_Y1': True, '_Y2': True}, {'_X2': True, '_X0': False, '_X1': False, '_Y0': False, '_Y1': True, '_Y2': True}, {'_X2': False, '_X0': False, '_X1': False, '_Y0': True, '_Y1': False, '_Y2': False}, {'_X2': True, '_X0': False, '_X1': False, '_Y0': True, '_Y1': False, '_Y2': False}, {'_X0': False, '_X1': True, '_X2': False, '_Y0': False, '_Y1': True, '_Y2': True}, {'_X0': False, '_X1': True, '_X2': False, '_Y0': True, '_Y1': False, '_Y2': False}]
    |-- [XXYY]: [{'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': False, '_Y2': True}, {'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': True, '_Y2': False}, {'_X0': False, '_X1': False, '_X2': True, '_Y0': False, '_Y1': True, '_Y2': False}]
    |-- [XD]: [{'_X0': False, '_X1': False, '_X2': False, '_D0': False, '_D1': False, '_D2': False}, {'_X0': False, '_X1': False, '_X2': True, '_D0': False, '_D1': False, '_D2': True}, {'_X0': False, '_X1': True, '_X2': False, '_D0': False, '_D1': True, '_D2': False}, {'_X0': False, '_X1': True, '_X2': True, '_D0': False, '_D1': True, '_D2': True}, {'_X0': True, '_X1': False, '_X2': False, '_D0': True, '_D1': False, '_D2': False}]
    |-- [AST]:
        |-- [A < B]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True}, {'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': True, 'B2': False}, {'A0': False, 'A1': False, 'A2': True, 'B0': False, 'B1': True, 'B2': False}]
        |-- [B < C]: [{'B0': False, 'B1': False, 'B2': False, 'C0': False, 'C1': False, 'C2': True}, {'B0': False, 'B1': False, 'B2': False, 'C0': False, 'C1': True, 'C2': False}, {'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True, 'C2': False}]
        |-- [(A < B) & (B < C))]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True, 'C2': False}]
        |-- [(A < B & B < C)]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True, 'C2': False}]
        |-- [A(Data1)]: [{'A0': False, 'A1': False, 'A2': False}]
        |-- [((A < B & B < C)) & (A(Data1)))]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True, 'C2': False}]
        |-- [B(Data2)]: [{'B0': False, 'B1': False, 'B2': True}]
        |-- [((A < B & B < C) & A(Data1)) & (B(Data2)))]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True, 'C2': False}]
        |-- [C(Data3)]: [{'C0': False, 'C1': True, 'C2': False}]
        |-- [((A < B & B < C) & A(Data1) & B(Data2)) & (C(Data3)))]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True, 'C2': False}]
        |-- [D i E]: []
        |-- [((A < B & B < C) & A(Data1) & B(Data2) & C(Data3)) & (D i E))]: []
        |-- [exist ['A', 'B', 'C', 'D', 'E'] . (A < B & B < C) & A(Data1) & B(Data2) & C(Data3) & D i E]: []

[INFO]: Specification result is False

|-- [ENUMERATION]: 5 -> "100" ([True, False, False])
|-- [EVENT]: end(5)
    |-- [X]: [{'_X0': False, '_X1': True, '_X2': True}]
    |-- [XX]: [{'_X2': False, '_X0': False, '_X1': False}, {'_X2': True, '_X0': False, '_X1': False}, {'_X0': False, '_X1': True, '_X2': False}, {'_X0': True, '_X1': False, '_X2': False}]
    |-- [XY]: []
    |-- [XYY]: [{'_X0': False, '_X1': True, '_X2': True, '_Y0': True, '_Y1': False, '_Y2': False}]
    |-- [XYYX]: []
    |-- [XYX]: []
    |-- [XYXY]: []
    |-- [XXY]: [{'_X2': False, '_X0': False, '_X1': False, '_Y0': False, '_Y1': True, '_Y2': True}, {'_X2': True, '_X0': False, '_X1': False, '_Y0': False, '_Y1': True, '_Y2': True}, {'_X0': False, '_X1': True, '_X2': False, '_Y0': False, '_Y1': True, '_Y2': True}]
    |-- [XXYY]: [{'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': False, '_Y2': True}, {'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': True, '_Y2': False}, {'_X0': False, '_X1': False, '_X2': False, '_Y0': True, '_Y1': False, '_Y2': False}, {'_X0': False, '_X1': False, '_X2': True, '_Y0': False, '_Y1': True, '_Y2': False}, {'_X0': False, '_X1': False, '_X2': True, '_Y0': True, '_Y1': False, '_Y2': False}, {'_X0': False, '_X1': True, '_X2': False, '_Y0': True, '_Y1': False, '_Y2': False}]
    |-- [XD]: [{'_X0': False, '_X1': False, '_X2': False, '_D0': False, '_D1': False, '_D2': False}, {'_X0': False, '_X1': False, '_X2': True, '_D0': False, '_D1': False, '_D2': True}, {'_X0': False, '_X1': True, '_X2': False, '_D0': False, '_D1': True, '_D2': False}, {'_X0': False, '_X1': True, '_X2': True, '_D0': False, '_D1': True, '_D2': True}, {'_X0': True, '_X1': False, '_X2': False, '_D0': True, '_D1': False, '_D2': False}]
    |-- [AST]:
        |-- [A < B]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True}, {'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': True, 'B2': False}, {'A0': False, 'A1': False, 'A2': False, 'B0': True, 'B1': False, 'B2': False}, {'A0': False, 'A1': False, 'A2': True, 'B0': False, 'B1': True, 'B2': False}, {'A0': False, 'A1': False, 'A2': True, 'B0': True, 'B1': False, 'B2': False}, {'A0': False, 'A1': True, 'A2': False, 'B0': True, 'B1': False, 'B2': False}]
        |-- [B < C]: [{'B0': False, 'B1': False, 'B2': False, 'C0': False, 'C1': False, 'C2': True}, {'B0': False, 'B1': False, 'B2': False, 'C0': False, 'C1': True, 'C2': False}, {'B0': False, 'B1': False, 'B2': False, 'C0': True, 'C1': False, 'C2': False}, {'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True, 'C2': False}, {'B0': False, 'B1': False, 'B2': True, 'C0': True, 'C1': False, 'C2': False}, {'B0': False, 'B1': True, 'B2': False, 'C0': True, 'C1': False, 'C2': False}]
        |-- [(A < B) & (B < C))]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True, 'C2': False}, {'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': True, 'C1': False, 'C2': False}, {'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': True, 'B2': False, 'C0': True, 'C1': False, 'C2': False}, {'A0': False, 'A1': False, 'A2': True, 'B0': False, 'B1': True, 'B2': False, 'C0': True, 'C1': False, 'C2': False}]
        |-- [(A < B & B < C)]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True, 'C2': False}, {'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': True, 'C1': False, 'C2': False}, {'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': True, 'B2': False, 'C0': True, 'C1': False, 'C2': False}, {'A0': False, 'A1': False, 'A2': True, 'B0': False, 'B1': True, 'B2': False, 'C0': True, 'C1': False, 'C2': False}]
        |-- [A(Data1)]: [{'A0': False, 'A1': False, 'A2': False}]
        |-- [((A < B & B < C)) & (A(Data1)))]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True, 'C2': False}, {'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': True, 'C1': False, 'C2': False}, {'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': True, 'B2': False, 'C0': True, 'C1': False, 'C2': False}]
        |-- [B(Data2)]: [{'B0': False, 'B1': False, 'B2': True}]
        |-- [((A < B & B < C) & A(Data1)) & (B(Data2)))]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True, 'C2': False}, {'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': True, 'C1': False, 'C2': False}]
        |-- [C(Data3)]: [{'C0': False, 'C1': True, 'C2': False}]
        |-- [((A < B & B < C) & A(Data1) & B(Data2)) & (C(Data3)))]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True, 'C2': False}]
        |-- [D i E]: []
        |-- [((A < B & B < C) & A(Data1) & B(Data2) & C(Data3)) & (D i E))]: []
        |-- [exist ['A', 'B', 'C', 'D', 'E'] . (A < B & B < C) & A(Data1) & B(Data2) & C(Data3) & D i E]: []

[INFO]: Specification result is False

|-- [ENUMERATION]: 4 -> "011" ([False, True, True])
|-- [EVENT]: end(4)
    |-- [X]: []
    |-- [XX]: [{'_X1': False, '_X2': False, '_X0': False}, {'_X1': False, '_X2': True, '_X0': False}, {'_X1': True, '_X2': False, '_X0': False}, {'_X1': True, '_X2': True, '_X0': False}, {'_X0': True, '_X1': False, '_X2': False}]
    |-- [XY]: []
    |-- [XYY]: []
    |-- [XYYX]: [{'_X0': False, '_X1': True, '_X2': True, '_Y0': True, '_Y1': False, '_Y2': False}]
    |-- [XYX]: []
    |-- [XYXY]: []
    |-- [XXY]: []
    |-- [XXYY]: [{'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': False, '_Y2': True}, {'_Y2': False, '_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': True}, {'_Y2': True, '_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': True}, {'_X0': False, '_X1': False, '_X2': False, '_Y0': True, '_Y1': False, '_Y2': False}, {'_Y2': False, '_X0': False, '_X1': False, '_X2': True, '_Y0': False, '_Y1': True}, {'_Y2': True, '_X0': False, '_X1': False, '_X2': True, '_Y0': False, '_Y1': True}, {'_X0': False, '_X1': False, '_X2': True, '_Y0': True, '_Y1': False, '_Y2': False}, {'_X0': False, '_X1': True, '_X2': False, '_Y0': False, '_Y1': True, '_Y2': True}, {'_X0': False, '_X1': True, '_X2': False, '_Y0': True, '_Y1': False, '_Y2': False}]
    |-- [XD]: [{'_X0': False, '_X1': False, '_X2': False, '_D0': False, '_D1': False, '_D2': False}, {'_X0': False, '_X1': False, '_X2': True, '_D0': False, '_D1': False, '_D2': True}, {'_X0': False, '_X1': True, '_X2': False, '_D0': False, '_D1': True, '_D2': False}, {'_X0': False, '_X1': True, '_X2': True, '_D0': False, '_D1': True, '_D2': True}, {'_X0': True, '_X1': False, '_X2': False, '_D0': True, '_D1': False, '_D2': False}]
    |-- [AST]:
        |-- [A < B]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True}, {'B2': False, 'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': True}, {'B2': True, 'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': True}, {'A0': False, 'A1': False, 'A2': False, 'B0': True, 'B1': False, 'B2': False}, {'B2': False, 'A0': False, 'A1': False, 'A2': True, 'B0': False, 'B1': True}, {'B2': True, 'A0': False, 'A1': False, 'A2': True, 'B0': False, 'B1': True}, {'A0': False, 'A1': False, 'A2': True, 'B0': True, 'B1': False, 'B2': False}, {'A0': False, 'A1': True, 'A2': False, 'B0': False, 'B1': True, 'B2': True}, {'A0': False, 'A1': True, 'A2': False, 'B0': True, 'B1': False, 'B2': False}]
        |-- [B < C]: [{'B0': False, 'B1': False, 'B2': False, 'C0': False, 'C1': False, 'C2': True}, {'C2': False, 'B0': False, 'B1': False, 'B2': False, 'C0': False, 'C1': True}, {'C2': True, 'B0': False, 'B1': False, 'B2': False, 'C0': False, 'C1': True}, {'B0': False, 'B1': False, 'B2': False, 'C0': True, 'C1': False, 'C2': False}, {'C2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True}, {'C2': True, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True}, {'B0': False, 'B1': False, 'B2': True, 'C0': True, 'C1': False, 'C2': False}, {'B0': False, 'B1': True, 'B2': False, 'C0': False, 'C1': True, 'C2': True}, {'B0': False, 'B1': True, 'B2': False, 'C0': True, 'C1': False, 'C2': False}]
        |-- [(A < B) & (B < C))]: [{'C2': False, 'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True}, {'C2': True, 'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True}, {'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': True, 'C1': False, 'C2': False}, {'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': True, 'B2': False, 'C0': False, 'C1': True, 'C2': True}, {'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': True, 'B2': False, 'C0': True, 'C1': False, 'C2': False}, {'A0': False, 'A1': False, 'A2': True, 'B0': False, 'B1': True, 'B2': False, 'C0': False, 'C1': True, 'C2': True}, {'A0': False, 'A1': False, 'A2': True, 'B0': False, 'B1': True, 'B2': False, 'C0': True, 'C1': False, 'C2': False}]
        |-- [(A < B & B < C)]: [{'C2': False, 'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True}, {'C2': True, 'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True}, {'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': True, 'C1': False, 'C2': False}, {'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': True, 'B2': False, 'C0': False, 'C1': True, 'C2': True}, {'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': True, 'B2': False, 'C0': True, 'C1': False, 'C2': False}, {'A0': False, 'A1': False, 'A2': True, 'B0': False, 'B1': True, 'B2': False, 'C0': False, 'C1': True, 'C2': True}, {'A0': False, 'A1': False, 'A2': True, 'B0': False, 'B1': True, 'B2': False, 'C0': True, 'C1': False, 'C2': False}]
        |-- [A(Data1)]: [{'A0': False, 'A1': False, 'A2': False}]
        |-- [((A < B & B < C)) & (A(Data1)))]: [{'C2': False, 'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True}, {'C2': True, 'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True}, {'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': True, 'C1': False, 'C2': False}, {'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': True, 'B2': False, 'C0': False, 'C1': True, 'C2': True}, {'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': True, 'B2': False, 'C0': True, 'C1': False, 'C2': False}]
        |-- [B(Data2)]: [{'B0': False, 'B1': False, 'B2': True}]
        |-- [((A < B & B < C) & A(Data1)) & (B(Data2)))]: [{'C2': False, 'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True}, {'C2': True, 'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True}, {'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': True, 'C1': False, 'C2': False}]
        |-- [C(Data3)]: [{'C0': False, 'C1': True, 'C2': False}]
        |-- [((A < B & B < C) & A(Data1) & B(Data2)) & (C(Data3)))]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True, 'C2': False}]
        |-- [D i E]: [{'D0': False, 'D1': True, 'D2': True, 'E0': True, 'E1': False, 'E2': False}]
        |-- [((A < B & B < C) & A(Data1) & B(Data2) & C(Data3)) & (D i E))]: [{'A0': False, 'A1': False, 'A2': False, 'B0': False, 'B1': False, 'B2': True, 'C0': False, 'C1': True, 'C2': False, 'D0': False, 'D1': True, 'D2': True, 'E0': True, 'E1': False, 'E2': False}]
        |-- [exist ['A', 'B', 'C', 'D', 'E'] . (A < B & B < C) & A(Data1) & B(Data2) & C(Data3) & D i E]: [{}]

[INFO]: Specification result is True

########################################################################### (FINAL STATE) ###########################################################################
[EXECUTION]: [['begin', 1, 'Data1'], ['end', 1], ['begin', 2, 'Data2'], ['end', 2], ['begin', 3, 'Data3'], ['end', 3], ['begin', 4, 'Data4'], ['begin', 5, 'Data5'], ['end', 5], ['end', 4]]

[PROPERTY]: exist ['A', 'B', 'C', 'D', 'E'] . (A < B & B < C) & A(Data1) & B(Data2) & C(Data3) & D i E

    |-- [X]: []
    |-- [XX]: [{'_X1': False, '_X2': False, '_X0': False}, {'_X1': False, '_X2': True, '_X0': False}, {'_X1': True, '_X2': False, '_X0': False}, {'_X1': True, '_X2': True, '_X0': False}, {'_X0': True, '_X1': False, '_X2': False}]
    |-- [XY]: []
    |-- [XYY]: []
    |-- [XYYX]: [{'_X0': False, '_X1': True, '_X2': True, '_Y0': True, '_Y1': False, '_Y2': False}]
    |-- [XYX]: []
    |-- [XYXY]: []
    |-- [XXY]: []
    |-- [XXYY]: [{'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': False, '_Y2': True}, {'_Y2': False, '_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': True}, {'_Y2': True, '_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': True}, {'_X0': False, '_X1': False, '_X2': False, '_Y0': True, '_Y1': False, '_Y2': False}, {'_Y2': False, '_X0': False, '_X1': False, '_X2': True, '_Y0': False, '_Y1': True}, {'_Y2': True, '_X0': False, '_X1': False, '_X2': True, '_Y0': False, '_Y1': True}, {'_X0': False, '_X1': False, '_X2': True, '_Y0': True, '_Y1': False, '_Y2': False}, {'_X0': False, '_X1': True, '_X2': False, '_Y0': False, '_Y1': True, '_Y2': True}, {'_X0': False, '_X1': True, '_X2': False, '_Y0': True, '_Y1': False, '_Y2': False}]
    |-- [XD]: [{'_X0': False, '_X1': False, '_X2': False, '_D0': False, '_D1': False, '_D2': False}, {'_X0': False, '_X1': False, '_X2': True, '_D0': False, '_D1': False, '_D2': True}, {'_X0': False, '_X1': True, '_X2': False, '_D0': False, '_D1': True, '_D2': False}, {'_X0': False, '_X1': True, '_X2': True, '_D0': False, '_D1': True, '_D2': True}, {'_X0': True, '_X1': False, '_X2': False, '_D0': True, '_D1': False, '_D2': False}]

[INFO]: Specification result is True

############################################################################# (THE END) #############################################################################
```

