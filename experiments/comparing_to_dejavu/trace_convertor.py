###############################################################################################
# This script is convert a trace which can be feed the MonAmI tool to a Dejavu format.
###############################################################################################

import json
import glob


def read_json(i_json_file):
    with open(i_json_file, "r") as json_file:
        data = json.load(json_file)
    return data


def convert(i_input: str, i_output: str):
    """
    Just run the translate process
    :return: None
    """
    monamiTrace = read_json(i_input)
    dejavu_trace = ""
    for event in monamiTrace["execution"]:
        if len(event) == 3:
            dejavu_trace += f"{event[0]},{event[1]},{event[2]}\n"
        else:
            dejavu_trace += f"{event[0]},{event[1]}\n"
    with open(i_output, "w") as dejavu_trace_file:
        dejavu_trace_file.write(dejavu_trace)


for trace_file in glob.glob("monami/*.json"):
    output_file = 'dejavu/' + trace_file.split('/')[1].replace('json', 'csv')
    convert(trace_file, output_file)


