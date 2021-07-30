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
1. By default, the `time` command in unix/linux systems only gives a time, but `gnu-time` gives memory as well.
2. [gnu-time](https://www.gnu.org/software/time/) runs another program, then display information about the resources used by that program.
3. We used it to measure the tools' memory and measure the time for the nfer C version (MonAmI and the nfer Scala version prints a time measure).
4. In Ubuntu, `gnu-time` can be found at `/usr/bin/time`, while in macOS, it needs to be installed at first (`brew install gnu-time`).  
5. We control the output of`gnu-time` by adding a line to `.bashrc`, to only output the memory and time:
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
1. To run MonAmI experiments, it needs to be installed first. For MonAmI installation please follow the [installation instructions](https://github.com/moraneus/MonAmI#installing-monami).
2. MonAmI runs in 2 modes `cs` (`CONTINUE-SMALL` : the formula is evaluated for every new event) and `cb` (`CONTINUE-BIG` : the formula is evaluated at the end only)
3. We explain mode `cs`, but it works the same with mode `cb`.
4. Relevant files:   
    1. `spec*.monami` are the specification files.
    2. `trace_*000_property_*.json` are the trace files.
    3. `run-monami_cs` is the bash script that runs MonAmi on different specs and traces.
    4. `result-monami_cs` is the output file that contains the results.
5. Running `run-monami_cs`:
    1. From the root directory of MonAmI you installed, CD to the `experiments/monami` folder.
    2. chmod +x `run-monami_cs`
    3. Make sure that `python3` in the `run-monami_cs` script points to the Python >= 3.7 version.  
    4. `./run-monami_cs`
6. Results are written to the file `result-monami_cs`.
    
## Running nfer Scala version experiments
1. To run nfer scala experiment, install latest version of [Scala 2](https://www.scala-lang.org/download/scala2.html) first. nfer Scala is implemented in Scala 2.13.5.
2. After installing Scala, you can run the nfer Scala experiment.
3. Relevant files:   
    1. `spec*.nfer` are the specification files.
    2. `trace_*000_property_*.json` are the trace files.
    3. `nfer` bash script that runs Scala and nfer with the right arguments.
    4. `nfer.jar` is the compiled jar file of nfer.    
    5. `run-nfer-scala` is the bash script that runs nfer Scala on different specs and traces.
    6. `result-nfer-scala` is the output file that contains the results.
4. Running `run-nfer-scala`:
    1. From the root directory of MonAmI you installed, CD to the `experiments/nfer_scala` folder.
    2. chmod +x `run-nfer-scala`
    3. chmod +x `nfer`
    4. `./run-nfer-scala`
5. Results are written to the file `result-nfer-scala`.
    
## Running nfer C version experiments
1. To run nfer C version, we used the python [nferModule](https://pypi.org/project/NferModule/) (`pip install NferModule`).
2. Relevant files:   
    1. `spec*.nferc` are the specification files.
    2. `trace_*000_property_*.csv` are the trace files.
    4. `run-nfer-c` is the bash script that runs nfer C on different specs and traces.
    5. `result-nfer-c` is the output file that contains the results.
4. Running `run-nfer-c`:
    1. From the root directory of MonAmI you installed, CD to the `experiments/nfer_c` folder.
    2. chmod +x `run-nfer-c`
    3. Make sure that `python3` in the `run-monami-c` script points to the Python >= 3.7 version.  
    3. `./run-nfer-c`
5. Results are written to the file `result-nfer-c`.
