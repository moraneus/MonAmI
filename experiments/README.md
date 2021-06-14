# Information
To evaluate MonAmi, we performed a comparison with the interval-based tools:
* [nfer Scala version](https://github.com/rv-tools/nfer).
* [nfer C version](https://bitbucket.org/seanmk/nfer/src/master/). 

nfer is the closest tool related to MonAmi, and we comment on the relations between these two tools and their capabilities.
We formulated four properties using the formalisms of the two tools, all related to receiving data from a planetary rover, 
and evaluated tool performances (time and memory) on traces of different sizes. 
The planetary rover scenario is inspired by the realistic properties of the Curiosity Mars rover. \
These experiments were made specifically for the ["Monitoring Interval Logic"](https://github.com/moraneus/MonAmI/blob/main/out/papers/Monitoring_Interval_Logic.pdf) paper, 
which is submitted to RV 2021 conference for review.

The paper was written by the following contributors:
* [Klaus Havelund](http://www.havelund.com/), Jet Propulsion Laboratory/NASA, USA
* Moran Omer, Bar Ilan University, Israel
* [Doron Peled](https://u.cs.biu.ac.il/~doronp/), Bar Ilan University, Israel

## Preparations
### gnu-time
1. [gnu-time](https://www.gnu.org/software/time/) have the power to runs another program, then display information about the resources used by that program.
2. We used it to measure the tools' memory and measure the time only for the nfer C version (MonAmI and nfer Scala version returned inner time measure).
3. By default, the `time` command in unix\linux systems only gives a time, but that `gnu-time` gives memory as well.
4. In Ubuntu, `gnu-time` can be found at `/usr/bin/time`, while in macOS, it needs to be installed at first (`brew install gnu-time`).  
5. To make it more clear and simple, we set the `gnu-time`, by adding a line to `.bashrc`, to output the memory and time data as we want:
```bash
export TIME="/usr/bin/time results\ncmd:%C\nreal: %es\nuser: %Us \nsys: %Ss \nmemory: %MKB \ncpu: %P"
```

### Automated scripts   
1. We created bash scripts that execute the tools by calling them with different arguments line by line.
2. Each execution is called with the `gnu-time` program.
3. For example:
```bash
   /usr/bin/time python3 run_monami_experiments.py spec1.monami trace_1000_property_1.json 1) >> result-monami_cb 2>&1
```
* `/usr/bin/time`: `gnu-time` binary in Ubuntu, which was the OS using for the experiments.
* `python3`: the interpreter which runs the MonAmI tool. Make sure that Python3 command is exist in your OS and it points to a Python >= 3.7. \
  In any other case you must define a Python variable\path in the script specifying where Python >= 3.7 is.
* `run_monami_experiments.py`: the main experiment MonAmI script.
* `spec1.monami`: spec for this MonAmI experiment execution.
* `trace_1000_property_1.json`: the trace input file.
* `1`: denotes for mode `CONTINUE-BIG`.
* `>> result-monami_cb`: append experiment results into `result-monami_cb` file.


## Running MonAmI experiments
1. To run MonAmI experiments, it needs to be installed first. For MonAmI installation please follow the [install instructions](https://github.com/moraneus/MonAmI#installing-monami).
2. MonAmI runs in 2 modes `cs` (`CONTINUE-SMALL`) and `cb` (`CONTINUE-BIG`)
3. We explain mode `cs`, but it works the same with mode `cb`.
4. Relevant files:   
    1. `spec*.monami` are the specifications file.
    2. `trace_*000_property_*.json` are the traces files.
    3. `rules_property_*` rules that helped create the trace files (not relevant for running the experiment).
    4. `result-monami_cs` is the output file that stores the results.
    5. `run-monami_cs` is the bash script that runs MonAmi in different modes.
5. Running `run-monami_cs`:
    1. From the root directory of MonAmI you installed, CD to the `experiments\monami` folder.
    2. chmod +x `run-monami_cs`
    3. Make sure that `python3` in the `run-monami_cs` script points to the Python >= 3.7 version.  
    4. `./run-monami_cs`
6. Result file will create in the same directory (`experiments\monami`) in a file called `result-monami_cs`.
    
## Running nfer Scala version experiments
1. To run nfer scala experiment, install [Scala 2.13.5 version](https://www.scala-lang.org/download/2.13.5.html) at first.
2. After installing Scala, you can run nfer Scala version experiment.
3. Relevant files:   
    1. `spec*.nfer` are the specifications file.
    2. `trace_*000_property_*.json` are the traces files.
    3. `nfer` bash script that runs Scala and nfer with the right arguments.
    4. `nfer.jar` is the compiled jar file of nfer.    
    5. `result-nfer-scala` is the output file that stores the results.
    6. `run-nfer-scala` is the bash script that runs nfer Scala in different modes.
4. Running `run-nfer-scala`:
    1. From the root directory of MonAmI you installed, CD to the `experiments\nfer_scala` folder.
    2. chmod +x `run-nfer-scala`
    3. chmod +x `nfer`
    4. `./run-nfer-scala`
5. Result file will create in the same directory (`experiments\nfer_scala`) in a file called `result-nfer-scala`.
    
## Running nfer C version experiments
1. To run nfer C version, we used the python [nferModule](https://pypi.org/project/NferModule/) (`pip install NferModule`).
2. Relevant files:   
    1. `spec*.nferc` are the specifications file.
    2. `trace_*000_property_*.csv` are the traces files.
    3. `run-nfer-c.py` Python script which execute nfer C version.
    4. `result-nfer-c` is the output file that stores the results.
    5. `run-nfer-c` is the bash script that runs nfer C in different modes.
4. Running `run-nfer-c`:
    1. From the root directory of MonAmI you installed, CD to the `experiments\nfer_c` folder.
    2. chmod +x `run-nfer-c`
    3. 3. Make sure that `python3` in the `run-monami-c` script points to the Python >= 3.7 version.  
    3. `./run-nfer-c`
5. Result file will create in the same directory (`experiments\nfer_c`) in a file called `result-nfer-c`.