# MonAmI - Monitoring Allen logic - made in Israel

## General Details: ##
* This tool was fully written in python using 'dd' package (Repository of 'dd' is at https://github.com/tulip-control/dd).
* It implements a monitoring version of Allen's interval algebra using BDDs.
* BDDs are used to represent Boolean functions. On a more abstract level, BDDs can be considered as a compressed representation of sets or relations (Wikipedia:  https://en.wikipedia.org/wiki/Binary_decision_diagram).

## Types of Allen's interval algebra: ##
![Image of Inervals](https://www.researchgate.net/profile/Ioannis_Tsamardinos/publication/230561978/figure/fig2/AS:646067146223617@1531045819115/1-The-13-relations-between-intervals-in-Allens-algebra-Interval-A-is-always-either-at.png)

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

## Execution Configuration: ##
1. Setting any execution for monitoring can be done by edit the 'input.json' file.
2. Each event is from the type `[Event type, Interval ID, Data]` for `begin` event and `[Event type, Interval ID]` for an 'end' event.
3. Example of `input.json` file:
```json
{
  "TITLE" :
  {
    "run":
    [
      ["begin", 1, null], ["end", 1], ["begin", "Two", "Data 2"], ["end", "Two"], ["begin", 3, ""], ["end", 3]
    ]
  }
}
```
Parameter     | Details
------------- | -------------
Event Type    | `"begin"` or `"end"` only
Interval ID   | `int`, `str`
Data          | `null`, `int`, or `str`

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
                                                    

################################################## (TITLE) ##################################################
[EXECUTION]: [['begin', 1, None], ['end', 1], ['begin', 'Two', 'Data 2'], ['end', 'Two'], ['begin', 3, ''], ['end', 3]]
################################################## ([EVENT]: begin->1) ##################################################
[XXY]: []
[XY]: []
[X]: [{'X0': False}]
[XD]: [{'X0': False, 'D0': False}]
################################################## ([EVENT]: end->1) ##################################################
[XXYY]: []
[XXY]: []
[XYXY]: []
[XYX]: []
[XYYX]: []
[XYY]: []
[XY]: []
[XX]: [{'X0': False}]
[X]: []
################################################## ([EVENT]: begin->Two) ##################################################
[XXY]: [{'X0': False, 'Y0': True}]
[XY]: []
[X]: [{'X0': True}]
[XD]: [{'X0': False, 'D0': False}, {'X0': True, 'D0': True}]
################################################## ([EVENT]: end->Two) ##################################################
[XXYY]: [{'X0': False, 'Y0': True}]
[XXY]: []
[XYXY]: []
[XYX]: []
[XYYX]: []
[XYY]: []
[XY]: []
[XX]: [{}]
[X]: []
################################################## (INFO) ##################################################

[INFO]: BDD variables Interval growth (1 -> 3)

################################################## (INFO) ##################################################

[INFO]: BDD variables Data growth (1 -> 3)

################################################## ([EVENT]: begin->3) ##################################################
[XXY]: [{'X0': False, 'X1': False, 'Y0': False, 'Y1': True, 'Y2': False}]
[XY]: []
[X]: [{'X0': False, 'X1': True, 'X2': False}]
[XD]: [{'X0': False, 'X1': False, 'X2': False, 'D0': False, 'D1': False, 'D2': False}, {'X0': False, 'X1': False, 'X2': True, 'D0': False, 'D1': False, 'D2': True}, {'X0': False, 'X1': True, 'X2': False, 'D0': False, 'D1': True, 'D2': False}]
################################################## ([EVENT]: end->3) ##################################################
[XXYY]: [{'X0': False, 'X1': False, 'X2': False, 'Y0': False, 'Y1': False, 'Y2': True}, {'X0': False, 'X1': False, 'X2': False, 'Y0': False, 'Y1': True, 'Y2': False}, {'X0': False, 'X1': False, 'X2': True, 'Y0': False, 'Y1': True, 'Y2': False}]
[XXY]: []
[XYXY]: []
[XYX]: []
[XYYX]: []
[XYY]: []
[XY]: []
[XX]: [{'X2': False, 'X0': False, 'X1': False}, {'X2': True, 'X0': False, 'X1': False}, {'X0': False, 'X1': True, 'X2': False}]
[X]: []
################################################## (FINAL STATE) ##################################################
[X]: []
[XX]: [{'X2': False, 'X0': False, 'X1': False}, {'X2': True, 'X0': False, 'X1': False}, {'X0': False, 'X1': True, 'X2': False}]
[XY]: []
[XYY]: []
[XYYX]: []
[XYX]: []
[XYXY]: []
[XXY]: []
[XXYY]: [{'X0': False, 'X1': False, 'X2': False, 'Y0': False, 'Y1': False, 'Y2': True}, {'X0': False, 'X1': False, 'X2': False, 'Y0': False, 'Y1': True, 'Y2': False}, {'X0': False, 'X1': False, 'X2': True, 'Y0': False, 'Y1': True, 'Y2': False}]
[XD]: [{'X0': False, 'X1': False, 'X2': False, 'D0': False, 'D1': False, 'D2': False}, {'X0': False, 'X1': False, 'X2': True, 'D0': False, 'D1': False, 'D2': True}, {'X0': False, 'X1': True, 'X2': False, 'D0': False, 'D1': True, 'D2': False}]
################################################## (THE END) ##################################################

```

