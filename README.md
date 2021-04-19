# MonAmI - Monitoring Allen logic - made in Israel

## General Details: ##
* This tool was fully written in python using 'dd' package (Repository of 'dd' is at https://github.com/tulip-control/dd).
* It implements a monitoring version of Allen's interval algebra using BDDs.
* BDDs are used to represent Boolean functions. On a more abstract level, BDDs can be considered as a compressed representation of sets or relations (Wikipedia:  https://en.wikipedia.org/wiki/Binary_decision_diagram).

## Types of Allen's interval algebra: ##
![Image of Inervals](https://www.researchgate.net/profile/Ioannis_Tsamardinos/publication/230561978/figure/fig2/AS:646067146223617@1531045819115/1-The-13-relations-between-intervals-in-Allens-algebra-Interval-A-is-always-either-at.png)

__NOTE: The only relations used by the algorithm for now are: `before`, `overlaps`, and `includes`.__
## General characterization of MonAmI: ## 
1. A trace is a sequence of `begin(i, d)` or `end(i)` events where `i` is denoted for an interval ID and `d` denotes data.
    * __NOTE: For `end` event, data is not mandatory since the data is set on the `begin` event.__
3. For each event:
    1. All possible Allen intervals are created, as these sets (`X`, `XX`, `XY`, `XYY`, `XYYX`, `XXY`, `XXYY`, `XYX`, `XYXY`, `XD`), represented as BDDs.
    2. The temporal logic formula is evaluated on these intervals.

## Installation: ##
1. Before execution, it needs to install python 3.6 and above.
2. In the file `requierments.txt`, there are all the packages that should be installed. \
For installation, please run the command `python -m pip install -r requierments.txt` (from CMD in windows or Terminal in Linux).
3. Running the program is made by running the command `python main.py` from the program root directory.

## Configuration: ##
### Program Input (Execution and Specification): ###
1. Setting any execution for monitoring can be done by edit the `input` file under the `execution` key.
2. Each event is from the type `[Event type, Interval ID, Data]` for `begin` event and `[Event type, Interval ID]` for an 'end' event.
3. You can create a random `execution` in the input file using the script `interval_generator.py`, added into the tool (`input` folder).
4. Creating your own specification is also in the `input` file under the `specification`. 
4. Example of `input` file:
```json
{
    "execution": [["begin", 1, "Data 1"], ["end", 1], ["begin", 2, "Data 2"], ["end", 2], ["begin", 3, "Data 3"], ["end", 3],
    ["begin", 4, "Data 4"], ["begin", 5, "Data 5"], ["end", 5], ["end", 4]],
    "specification": "exist X, B, C . X < B & B < C & X('Data 1') & B('Data 2') & C('Data 3')"
}
```

Parameter     | Details
------------- | -------------
Event Type    | `"begin"` or `"end"` only
Interval ID   | `int`, `str`
Data          | `null`, `int`, or `str`

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
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `input` \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- `intervals_generator.py` \
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






## Execution output in debug mode: ##
* In debug mode, after each event, the program will print out to console the updated BDDs.
* It also prints out other information which is relevant to the execution.
* The final state will be print at the end of the execution.
```python

                                                       ███╗   ███╗ ██████╗ ███╗   ██╗ █████╗ ███╗   ███╗██╗
                                                       ████╗ ████║██╔═══██╗████╗  ██║██╔══██╗████╗ ████║██║
                                                       ██╔████╔██║██║   ██║██╔██╗ ██║███████║██╔████╔██║██║
                                                       ██║╚██╔╝██║██║   ██║██║╚██╗██║██╔══██║██║╚██╔╝██║██║
                                                       ██║ ╚═╝ ██║╚██████╔╝██║ ╚████║██║  ██║██║ ╚═╝ ██║██║
                                                       ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝
                                                    

############################################################################## (START) ##############################################################################
[EXECUTION]: [['begin', 1, 'Data 1'], ['end', 1], ['begin', 2, 'Data 2'], ['end', 2], ['begin', 3, 'Data 3'], ['end', 3], ['begin', 4, 'Data 4'], ['begin', 5, 'Data 5'], ['end', 5], ['end', 4]]

[PROPERTY]: exist ['A', 'B', 'C'] . A < B & B < C & A(Data 1) & B(Data 2) & C(Data 3)

|-- [EVENT]: begin->1
    |-- [XXY]: []
    |-- [XY]: []
    |-- [X]: [{'X0': False}]
    |-- [XD]: [{'X0': False, 'D0': False}]
    |-- [AST]: begin -> 1
        |-- [A < B]: []
        |-- [B < C]: []
        |-- [(A < B) & (B < C))]: []
        |-- [A(Data 1)]: [{'A0': False}]
        |-- [(A < B & B < C) & (A(Data 1)))]: []
        |-- [B(Data 2)]: []
        |-- [(A < B & B < C & A(Data 1)) & (B(Data 2)))]: []
        |-- [C(Data 3)]: []
        |-- [(A < B & B < C & A(Data 1) & B(Data 2)) & (C(Data 3)))]: []
        |-- [exist ['A', 'B', 'C'] . And(And(And(And(Before(A,B),Before(B,C)),Data(A,Data 1)),Data(B,Data 2)),Data(C,Data 3))]: []

[INFO]: Specification result is False

|-- [EVENT]: end->1
    |-- [XXYY]: []
    |-- [XXY]: []
    |-- [XYXY]: []
    |-- [XYX]: []
    |-- [XYYX]: []
    |-- [XYY]: []
    |-- [XY]: []
    |-- [XX]: [{'X0': False}]
    |-- [X]: []
    |-- [AST]: end -> 1
        |-- [A < B]: []
        |-- [B < C]: []
        |-- [(A < B) & (B < C))]: []
        |-- [A(Data 1)]: [{'A0': False}]
        |-- [(A < B & B < C) & (A(Data 1)))]: []
        |-- [B(Data 2)]: []
        |-- [(A < B & B < C & A(Data 1)) & (B(Data 2)))]: []
        |-- [C(Data 3)]: []
        |-- [(A < B & B < C & A(Data 1) & B(Data 2)) & (C(Data 3)))]: []
        |-- [exist ['A', 'B', 'C'] . And(And(And(And(Before(A,B),Before(B,C)),Data(A,Data 1)),Data(B,Data 2)),Data(C,Data 3))]: []

[INFO]: Specification result is False

|-- [EVENT]: begin->2
    |-- [XXY]: [{'X0': False, 'Y0': True}]
    |-- [XY]: []
    |-- [X]: [{'X0': True}]
    |-- [XD]: [{'X0': False, 'D0': False}, {'X0': True, 'D0': True}]
    |-- [AST]: begin -> 2
        |-- [A < B]: []
        |-- [B < C]: []
        |-- [(A < B) & (B < C))]: []
        |-- [A(Data 1)]: [{'A0': False}]
        |-- [(A < B & B < C) & (A(Data 1)))]: []
        |-- [B(Data 2)]: [{'B0': True}]
        |-- [(A < B & B < C & A(Data 1)) & (B(Data 2)))]: []
        |-- [C(Data 3)]: []
        |-- [(A < B & B < C & A(Data 1) & B(Data 2)) & (C(Data 3)))]: []
        |-- [exist ['A', 'B', 'C'] . And(And(And(And(Before(A,B),Before(B,C)),Data(A,Data 1)),Data(B,Data 2)),Data(C,Data 3))]: []

[INFO]: Specification result is False

|-- [EVENT]: end->2
    |-- [XXYY]: [{'X0': False, 'Y0': True}]
    |-- [XXY]: []
    |-- [XYXY]: []
    |-- [XYX]: []
    |-- [XYYX]: []
    |-- [XYY]: []
    |-- [XY]: []
    |-- [XX]: [{}]
    |-- [X]: []
    |-- [AST]: end -> 2
        |-- [A < B]: [{'A0': False, 'B0': True}]
        |-- [B < C]: [{'B0': False, 'C0': True}]
        |-- [(A < B) & (B < C))]: []
        |-- [A(Data 1)]: [{'A0': False}]
        |-- [(A < B & B < C) & (A(Data 1)))]: []
        |-- [B(Data 2)]: [{'B0': True}]
        |-- [(A < B & B < C & A(Data 1)) & (B(Data 2)))]: []
        |-- [C(Data 3)]: []
        |-- [(A < B & B < C & A(Data 1) & B(Data 2)) & (C(Data 3)))]: []
        |-- [exist ['A', 'B', 'C'] . And(And(And(And(Before(A,B),Before(B,C)),Data(A,Data 1)),Data(B,Data 2)),Data(C,Data 3))]: []

[INFO]: Specification result is False

############################################################################## (INFO) ##############################################################################

[INFO]: BDD variables Interval growth (1 -> 2)

############################################################################## (INFO) ##############################################################################

[INFO]: BDD variables Data growth (1 -> 2)

|-- [EVENT]: begin->3
    |-- [XXY]: [{'X0': False, 'Y0': True, 'Y1': False}]
    |-- [XY]: []
    |-- [X]: [{'X0': True, 'X1': False}]
    |-- [XD]: [{'D0': False, 'D1': False, 'X0': False, 'X1': False}, {'D0': False, 'D1': True, 'X0': False, 'X1': True}, {'D0': True, 'D1': False, 'X0': True, 'X1': False}]
    |-- [AST]: begin -> 3
        |-- [A < B]: [{'A0': False, 'A1': False, 'B0': False, 'B1': True}]
        |-- [B < C]: [{'B0': False, 'B1': False, 'C0': False, 'C1': True}]
        |-- [(A < B) & (B < C))]: []
        |-- [A(Data 1)]: [{'A0': False, 'A1': False}]
        |-- [(A < B & B < C) & (A(Data 1)))]: []
        |-- [B(Data 2)]: [{'B0': False, 'B1': True}]
        |-- [(A < B & B < C & A(Data 1)) & (B(Data 2)))]: []
        |-- [C(Data 3)]: [{'C0': True, 'C1': False}]
        |-- [(A < B & B < C & A(Data 1) & B(Data 2)) & (C(Data 3)))]: []
        |-- [exist ['A', 'B', 'C'] . And(And(And(And(Before(A,B),Before(B,C)),Data(A,Data 1)),Data(B,Data 2)),Data(C,Data 3))]: []

[INFO]: Specification result is False

|-- [EVENT]: end->3
    |-- [XXYY]: [{'X0': False, 'X1': False, 'Y0': False, 'Y1': True}, {'X0': False, 'X1': False, 'Y0': True, 'Y1': False}, {'X0': False, 'X1': True, 'Y0': True, 'Y1': False}]
    |-- [XXY]: []
    |-- [XYXY]: []
    |-- [XYX]: []
    |-- [XYYX]: []
    |-- [XYY]: []
    |-- [XY]: []
    |-- [XX]: [{'X1': False, 'X0': False}, {'X1': True, 'X0': False}, {'X0': True, 'X1': False}]
    |-- [X]: []
    |-- [AST]: end -> 3
        |-- [A < B]: [{'A0': False, 'A1': False, 'B0': False, 'B1': True}, {'A0': False, 'A1': False, 'B0': True, 'B1': False}, {'A0': False, 'A1': True, 'B0': True, 'B1': False}]
        |-- [B < C]: [{'B0': False, 'B1': False, 'C0': False, 'C1': True}, {'B0': False, 'B1': False, 'C0': True, 'C1': False}, {'B0': False, 'B1': True, 'C0': True, 'C1': False}]
        |-- [(A < B) & (B < C))]: [{'A0': False, 'A1': False, 'B0': False, 'B1': True, 'C0': True, 'C1': False}]
        |-- [A(Data 1)]: [{'A0': False, 'A1': False}]
        |-- [(A < B & B < C) & (A(Data 1)))]: [{'A0': False, 'A1': False, 'B0': False, 'B1': True, 'C0': True, 'C1': False}]
        |-- [B(Data 2)]: [{'B0': False, 'B1': True}]
        |-- [(A < B & B < C & A(Data 1)) & (B(Data 2)))]: [{'A0': False, 'A1': False, 'B0': False, 'B1': True, 'C0': True, 'C1': False}]
        |-- [C(Data 3)]: [{'C0': True, 'C1': False}]
        |-- [(A < B & B < C & A(Data 1) & B(Data 2)) & (C(Data 3)))]: [{'A0': False, 'A1': False, 'B0': False, 'B1': True, 'C0': True, 'C1': False}]
        |-- [exist ['A', 'B', 'C'] . And(And(And(And(Before(A,B),Before(B,C)),Data(A,Data 1)),Data(B,Data 2)),Data(C,Data 3))]: [{}]

[INFO]: Specification result is True

########################################################################### (FINAL STATE) ###########################################################################
[EXECUTION]: [['begin', 1, 'Data 1'], ['end', 1], ['begin', 2, 'Data 2'], ['end', 2], ['begin', 3, 'Data 3'], ['end', 3], ['begin', 4, 'Data 4'], ['begin', 5, 'Data 5'], ['end', 5], ['end', 4]]

[PROPERTY]: exist ['A', 'B', 'C'] . A < B & B < C & A(Data 1) & B(Data 2) & C(Data 3)

    |-- [X]: []
    |-- [XX]: [{'X1': False, 'X0': False}, {'X1': True, 'X0': False}, {'X0': True, 'X1': False}]
    |-- [XY]: []
    |-- [XYY]: []
    |-- [XYYX]: []
    |-- [XYX]: []
    |-- [XYXY]: []
    |-- [XXY]: []
    |-- [XXYY]: [{'X0': False, 'X1': False, 'Y0': False, 'Y1': True}, {'X0': False, 'X1': False, 'Y0': True, 'Y1': False}, {'X0': False, 'X1': True, 'Y0': True, 'Y1': False}]
    |-- [XD]: [{'D0': False, 'D1': False, 'X0': False, 'X1': False}, {'D0': False, 'D1': True, 'X0': False, 'X1': True}, {'D0': True, 'D1': False, 'X0': True, 'X1': False}]

[INFO]: Specification result is True

############################################################################# (THE END) #############################################################################
```

