# Information
As part of the testing process of MonAmI, we performed several experiments that tested the correctness of the tool and its performance - the time that it takes and the allocated memory during the execution. 
We created trace files in different sizes of events (1000, 2000, 4000, 8000, 16000). These files were created with the trace generator script. 
We compare MonAmI to nfer tool ([nfer in C](https://bitbucket.org/seanmk/nfer/src/master/), [nfer in Scala](https://github.com/rv-tools/nfer)).

## Preparations
1. To measure memory and time, we used the `gnu-time` binary (the time mode in gnu-time used only for the nfer C version).
2. We created bash scripts that execute the tools by calling them with different arguments line by line.
3. Each execution is called with the gnu-time, for example:
```bash
   /usr/bin/time python3.9 run-nfer-c.py spec1.nferc trace_1000_property_1.csv false false
```
The `/usr/bin/time` was the installation path of gnu-time in Ubuntu. 
4. We set the gnu-time (by add to `.bashrc`) to output the memory and time data in clear way:
```bash
export TIME="/usr/bin/time results\ncmd:%C\nreal: %es\nuser: %Us \nsys: %Ss \nmemory: %MKB \ncpu: %P"
```

## Running MonAmI experiments
1. MonAmI runs in 2 modes cs (`CONTINUE-SMALL`) and cb (`CONTINUE-BIG`)
2. We take mode cs to explain, but it works the same with mode cb.
3. Relevant files:   
    1. `spec*.monami` are the specifications file.
    2. `trace_*000_property_*.json` are the traces files.
    3. `rules_property_*` are the rules that helped create the trace files (not relevant for running the experiment).
    4. `result-monami-cs` is the output file that stores the results.
    5. `run-monami-cs` is the bash script that runs monami in different modes.
4. Running `run-monami-cs`:
    1. CD to monami experiment folder.
    2. chmod +x `run-monami-cs`
    3. `./run-monami-cs`
    
## Running nfer Scala version experiments
1. To run nfer scala, please follow the instructions in [nfer in Scala](https://github.com/rv-tools/nfer) at first.
2. After installing Scala, you can run nfer Scala version experiment.
3. Relevant files:   
    1. `spec*.nfer` are the specifications file.
    2. `trace_*000_property_*.json` are the traces files.
    3. `nfer` bash script that runs Scala and nfer with the right arguments.
    4. `nfer.jar` is the compiled jar file of nfer.    
    5. `result-nfer-scala` is the output file that stores the results.
    6. `run-nfer-scala` is the bash script that runs nfer Scala in different modes.
4. Running `run-nfer-scala`:
    1. CD to nfer_scala experiment folder.
    2. chmod +x `run-nfer-scala`
    3. `./run-nfer-scala`
    
## Running nfer C version experiments
1. To run nfer C version, we used the python [nferModule](https://pypi.org/project/NferModule/) (`pip install NferModule`).
2. Relevant files:   
    1. `spec*.nferc` are the specifications file.
    2. `trace_*000_property_*.csv` are the traces files.
    3. `run-nfer-c.py` Python script which execute nfer C version.
    4. `result-nfer-c` is the output file that stores the results.
    5. `run-nfer-c` is the bash script that runs nfer C in different modes.
4. Running `run-nfer-c`:
    1. CD to nfer_c experiment folder.
    2. chmod +x `run-nfer-c`
    3. `./run-nfer-c`