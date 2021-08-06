# Information
The use of BDDs in runtime verification has been explored for the first-order past time temporal logic QTL, that monitored by [DejaVu](https://github.com/havelund/dejavu), in contrast to the interval logic FoATL monitored by MonAmi. \
Given a representation of intervals as pairs of events of the form begin(A, Ad) and end(A), we can perform monitoring by translating the specification into past first-order LTL, referred to as QTL, as used by the tool DejaVu. \
We evaluate MonAmi against Dejavu by evaluating FoATL properties against their translations to QTL, using a manual translation. The manual translation optimizes the resulting QTL formulas. \
We formulated four properties using the formalisms of the two tools and evaluated tool performances (time and memory) on traces of different sizes. 
### MonAmi properties:
```json
   "property1": "!exist A . exist B . A < B & same(A, B)"
   "property2": "!exist A . exist B, C . A i B & B i C"
   "property3": "forall A, B . ((A < B) & (!exist C . (A < C & C < B))) -> !(A('2') & B('2'))"
   "property4": "forall A, B, C . (A o B & B o C) -> !(A o C)"
```
### Dejavu tranlations:
```json
  prop P1: !(Exists A . Exists B . Exists d .  P ( end(B)  & @ P ( begin(B, d) & @ P ( end(A) & @ P begin(A, d) ) ) ) )
  prop P2: ! Exists  A . Exists B . Exists C . Exists da . Exists db . Exists dc . ( end(A) & @ P ( end(B) & @ P ( end (C) & @ P ( begin (C,dc) & @ P ( begin(B,db) & @ P begin(A,da))))))
  prop P3: Forall A . Forall B . ( ( P end(B) & @ P ( begin(B,2) & @ P ( end(A) & @ P begin(A,2) ) ) ) -> ! Exists C .Exists d . (  P ( begin(B, 2) &  @P ( end(C) & @ P ( begin(C, d) & @ P end(A) ) ) ) ) )
  prop P4: Forall A . Forall B . Forall C . Forall da . Forall db . Forall dc .(  ( P  (end(B) & @ P ( end(A) & @ P ( begin(B,db)  & @ P begin(A,da) ) ) )  & P ( end(C) & @ P ( end(B) & @ P ( begin(C,dc)  & @ P begin(B,db) ) ) ) ) -> ! P ( end(C) & @ P ( end(A) & @ P ( begin(C,dc)  & @ P begin(A,da) ) ) ) ) 

```

These experiments were made specifically for the ["Monitoring Interval Logic"](https://github.com/moraneus/MonAmI/blob/main/out/papers/Monitoring_Interval_Logic.pdf) paper, 
which is submitted to SEFM 2021 conference for review.

The paper was written by the following contributors:
* [Klaus Havelund](http://www.havelund.com/), Jet Propulsion Laboratory/NASA, USA
* Moran Omer, Bar Ilan University, Israel
* [Doron Peled](https://u.cs.biu.ac.il/~doronp/), Bar Ilan University, Israel

## Preparations
### gnu-time
1. By default, the `time` command in unix/linux systems only gives a time, but `gnu-time` gives memory as well.
2. [gnu-time](https://www.gnu.org/software/time/) runs another program, then display information about the resources used by that program.
3. We used it to measure the tools' memory (MonAmI and the Dejavu prints a time measure).
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
    1. From the root directory of MonAmI you installed, CD to the `experiments/comparing_to_dejavu/monami` folder.
    2. chmod +x `run-monami_cs`
    3. Make sure that `python3` in the `run-monami_cs` script points to the Python >= 3.7 version.  
    4. `./run-monami_cs`
6. Results are written to the file `result-monami_cs`.
    
## Running Dejavu experiments
1. To run Dejavu experiment, install latest version of [Scala 2](https://www.scala-lang.org/download/scala2.html) first. Dejavu is implemented in Scala 2.13.5.
2. After installing Scala, you can run the Dejavu experiment.
3. Relevant files:   
    1. `spec*.dejavu` are the specification files.
    2. `trace_*000_property_*.csv` are the trace files.
    3. `dejavu` bash script that runs Scala and Dejavu with the right arguments.
    4. `dejavu.jar` is the compiled jar file of Dejavu.    
    5. `run-dejavu` is the bash script that runs Dejavu on different specs and traces.
    6. `result-dejavu` is the output file that contains the results.
4. Running `run-dejavu`:
    1. From the root directory of MonAmI you installed, CD to the `experiments/comparing_to_dejavu/dejavu` folder.
    2. chmod +x `run-dejavu`
    3. chmod +x `dejavu`
    4. `./run-dejavu`
5. Results are written to the file `result-dejavu`.

