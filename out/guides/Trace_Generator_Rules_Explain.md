# Rules File 
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

### Graphic explain:
```
0          2            4          5
|---BOOT---|            |---BOOT---|
     |---DL_IMAGE---|
     1              3
```

"0": {"DATA": "BOOT", "B_PRIORITY": 0, "E_PRIORITY": 2}, \
"1": {"DATA": "DL_IMAGE", "B_PRIORITY": 1, "E_PRIORITY": 3}, \
"2": {"DATA": "BOOT", "B_PRIORITY": 4, "E_PRIORITY": 5},

```
6          7   8          10
|---BOOT---|   |---BOOT---|
                      |---DL_IMAGE---|
                      9              11
```


"3": {"DATA": "BOOT", "B_PRIORITY": 6, "E_PRIORITY": 7}, \
"4": {"DATA": "DL_IMAGE", "B_PRIORITY": 9, "E_PRIORITY": 11}, \
"5": {"DATA": "BOOT", "B_PRIORITY": 8, "E_PRIORITY": 10} 

```
0                                3                         
|-----------DL_ARMPRM------------|   
        |---DL_IMAGE---|
        1              2
```

"0": {"DATA": "DL_ARMPRM", "B_PRIORITY": 0, "E_PRIORITY": 3}, \
"1": {"DATA": "DL_FAIL", "B_PRIORITY": 1, "E_PRIORITY": 2},

```
4               5   6             7
|---DL_ARMPRM---|   |---DL_FAIL---|
```

"2": {"DATA": "DL_ARMPRM", "B_PRIORITY": 4, "E_PRIORITY": 5}, \
"3": {"DATA": "DL_FAIL", "B_PRIORITY": 6, "E_PRIORITY": 7}
```
0            1   2              3  4            5   6                 7
|---INS_ON---|   |---INS_FAIL---|  |---INS_ON---|   |---INS_RECOVER---| 
```

"0": {"DATA": "INS_ON", "B_PRIORITY": 0, "E_PRIORITY": 1}, \
"1": {"DATA": "INS_FAIL", "B_PRIORITY": 2, "E_PRIORITY": 3}, \
"2": {"DATA": "INS_RECOVER", "B_PRIORITY": 6, "E_PRIORITY": 7}, \
"3": {"DATA": "INS_ON", "B_PRIORITY": 4, "E_PRIORITY": 5},

```
8            10                                     
|---INS_ON---|   
      |---INS_FAIL---|  |---INS_ON---|   |---INS_RECOVER---|  
      2              11 12           13  14                15
```

"4": {"DATA": "INS_ON", "B_PRIORITY": 8, "E_PRIORITY": 10}, \
"5": {"DATA": "INS_FAIL", "B_PRIORITY": 9, "E_PRIORITY": 11}, \
"6": {"DATA": "INS_RECOVER", "B_PRIORITY": 14, "E_PRIORITY": 15}, \
"7": {"DATA": "INS_ON", "B_PRIORITY": 12, "E_PRIORITY": 13}

```
0                                                         5
|------------------------DL_IMAGE ------------------------|
             1                               4
             |---------GET_CAMDATA ----------|
                      |---STARVE---|  
                      2            3
```

"0": {"DATA": "DL_IMAGE", "B_PRIORITY": 0, "E_PRIORITY": 5}, \
"1": {"DATA": "GET_CAMDATA", "B_PRIORITY": 1, "E_PRIORITY": 4}, \
"2": {"DATA": "STARVE", "B_PRIORITY": 2, "E_PRIORITY": 3},

```
6              7    8                 10
|---DL_IMAGE---|    |---GET_CAMDATA ---|
                                |---STARVE---|  
                                9           11
```

"3": {"DATA": "DL_IMAGE", "B_PRIORITY": 6, "E_PRIORITY": 7}, \
"4": {"DATA": "GET_CAMDATA", "B_PRIORITY": 8, "E_PRIORITY": 10}, \
"5": {"DATA": "STARVE", "B_PRIORITY": 9, "E_PRIORITY": 11}
