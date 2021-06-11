###############################################################################################
# This script is creates a trace which can be feed the MonAmI tool.
# The TraceGenerator script gets several of parameters which define the structure of the trace.
# Note: rules and data must be given as different filenames arguments.
###############################################################################################

import random
import json
import string


def read_json(i_json_file):
    with open(i_json_file, "r") as json_file:
        data = json.load(json_file)
    return data

class BadPercentageValue(Exception):
    def __init__(self, i_percentage):
        self.__m_message = f"Bad value of percentage: {i_percentage})"
        super().__init__(self.__m_message)

class BadDepthValue(Exception):
    def __init__(self, i_depth):
        self.__m_message = f"Bad value of trace depth: {i_depth})"
        super().__init__(self.__m_message)

class TraceGenerator:

    def __init__(self,
                 i_rules_file: str,
                 i_data_file: str,
                 i_nums_of_interval: int,
                 i_output: str,
                 i_rules_percentage: int,
                 i_trace_depth: int):
        """
        Initialize TraceGenerator params
        :param i_rules_file: Path to the rule JSON file.
        :param i_data_file: Path to the data JSON file.
        :param i_nums_of_interval: Number of intervals in the trace.
        :param i_output: Path to the JSON output file.
        :param i_rules_percentage: Percentage of the trace which cover by rules events.
        :param i_trace_depth: The maximum depth of the trace
        """
        self.__m_rules = read_json(i_rules_file)
        self.__m_data = read_json(i_data_file)
        self.__m_num_of_intervals = i_nums_of_interval
        self.__m_trace_length = i_nums_of_interval * 2
        self.__m_interval_ids = list(range(0, i_nums_of_interval))
        self.__m_output = i_output
        self.__m_rules_percentage = i_rules_percentage
        self.__m_data_length = len(self.__m_data)
        self.__m_trace_depth = i_trace_depth
        self.__num_of_rules = 0
        self.__num_of_repeats = 0
        self.__num_of_manage_events = 0

    def start(self):
        """
        Manage the trace generator process.
        It calls all the necessary methods.
        :return: None
        """
        self.__params_validatation()
        self.__rules_init()
        management_sequence = self.__initilaize_rules_intervals()
        full_trace = self.__generate_random_trace(management_sequence)
        self.__save_to_file(full_trace)

    def __params_validatation(self):
        """
        Validate parts of the params which is crucial for valid process.
        :return: None
        """
        if self.__m_rules_percentage < 0 or self.__m_rules_percentage > 100:
            raise BadPercentageValue(self.__m_rules_percentage)
        elif self.__m_trace_depth < 0:
            raise BadDepthValue(self.__m_trace_depth)

    def __rules_init(self):
        """
        Process the rule input file and set the num_of_repeats param according to the size of rules,
        size of the intervals and the rules cover percentage.
        :return: None
        """
        for rule in self.__m_rules:
            self.__num_of_rules += len(rule.keys())
        self.__num_of_repeats = ((self.__m_num_of_intervals * self.__m_rules_percentage) // 100) // self.__num_of_rules

    def __initilaize_rules_intervals(self):
        """
        Build set of intervals which is correspond to the rules.
        :return: All events from the rules with theirs data as a lists.
        """
        sequence = []
        for rule in self.__m_rules:
            sequence_block_size = self.__m_trace_length // self.__num_of_repeats
            start_block_index = 0
            end_block_index = sequence_block_size
            for repeat in range(self.__num_of_repeats):
                sequence.append({})
                priorities = {}
                for i in range(len(rule.keys())):
                    sequence[-1][i] = {}
                    sequence[-1][i]['DATA'] = rule[str(i)]['DATA']
                    sequence[-1][i]['ID'] = self.__interval_id_generator()
                    if i == 0:
                        sequence[-1][i]['B_INDEX'] = random.randint(start_block_index + rule[str(i)]['B_PRIORITY'],
                                                                    end_block_index -
                                                            (len(rule.keys()) * 2) + rule[str(i)]['B_PRIORITY'])
                        priorities[rule[str(i)]['B_PRIORITY']] = sequence[-1][i]['B_INDEX']
                        sequence[-1][i]['E_INDEX'] = random.randint(sequence[-1][i]['B_INDEX'] +
                                                                    rule[str(i)]['E_PRIORITY'] -
                                                                    rule[str(i)]['B_PRIORITY'],
                                                                    end_block_index -
                                                            (len(rule.keys()) * 2) + rule[str(i)]['E_PRIORITY'])
                        priorities[rule[str(i)]['E_PRIORITY']] = sequence[-1][i]['E_INDEX']
                    else:
                        sequence[-1][i]['B_INDEX'] = self.__find_range(rule[str(i)]['B_PRIORITY'], priorities,
                                                                       len(rule.keys()), end_block_index)
                        priorities[rule[str(i)]['B_PRIORITY']] = sequence[-1][i]['B_INDEX']
                        sequence[-1][i]['E_INDEX'] = self.__find_range(rule[str(i)]['E_PRIORITY'], priorities,
                                                                       len(rule.keys()), end_block_index)
                        priorities[rule[str(i)]['E_PRIORITY']] = sequence[-1][i]['E_INDEX']
                    self.__num_of_manage_events += 1
                print(priorities)
                start_block_index = end_block_index + 1
                end_block_index += sequence_block_size

        return sequence

    def __find_range(self, i_curr_priority: int, i_seen_priorities: dict, i_rule_length: int, i_end_block_index: int):
        """
        Analyze and find the right index for an event.
        :param i_curr_priority: Event current priority in the rule sequence.
        :param i_seen_priorities: Dictionary which contains the priorities of events we see already.
        :param i_rule_length: The whole rule for it's length calculation.
        :param i_end_block_index: The max block index in the trace which can contain an event from the current rule.
        :return: The index of the current event.
        """
        min_priority = min(i_seen_priorities.keys())
        max_priority = max(i_seen_priorities.keys())
        if i_curr_priority < min_priority:
            index = random.randint(i_curr_priority,
                                   i_seen_priorities[min_priority] - min_priority + i_curr_priority)
        elif i_curr_priority > max_priority:
            index = random.randint(i_seen_priorities[max_priority] + i_curr_priority - max_priority,
                                   i_end_block_index - (i_rule_length * 2) + i_curr_priority)
        else:
            higher_index = i_seen_priorities[max_priority]
            lower_index = i_seen_priorities[min_priority]
            for seen_priority in i_seen_priorities.keys():
                if i_curr_priority < seen_priority < max_priority:
                    higher_index = i_seen_priorities[seen_priority]
                    max_priority = seen_priority
                elif i_curr_priority > seen_priority > min_priority:
                    lower_index = i_seen_priorities[seen_priority]
                    min_priority = seen_priority
            index = random.randint(lower_index + i_curr_priority - min_priority,
                                   higher_index - max_priority + i_curr_priority)
        return index

    def __interval_id_generator(self, size=10, chars=string.ascii_lowercase):
        """
        Generate an ID for the intervals.
        :param size: Length on the ID
        :param chars: Variety of chars which be a part of the ID.
        :return: ID as str.
        """
        return ''.join(random.choice(chars) for _ in range(size))

    def __generate_random_trace(self, i_event_rules_sequence):
        """
        Generate the trace according the rules and the generated events which is affected by the depth param.
        :param i_event_rules_sequence: All events from the rules with theirs data as a lists.
        :return: The trace as a list
        """
        intervals = []
        start = 1
        for i in range(self.__m_num_of_intervals - self.__num_of_manage_events):
            name = self.__interval_id_generator()
            intervals.append([name, 'begin', start])
            intervals.append([name, 'end', random.randint(start, start + self.__m_trace_depth + 1)])
            start += 1
        intervals.sort(key=lambda x: x[2])
        trace = []

        for interval in intervals:
            if interval[1] == 'begin':
                data = self.__m_data[interval[2] % self.__m_data_length]
                trace.append([interval[1], interval[0], data])
            else:
                trace.append([interval[1], interval[0]])

        for sequence in i_event_rules_sequence:
            for i in range(len(sequence.keys())):
                trace.insert(sequence[i]['B_INDEX'], ['begin', sequence[i]['ID'], sequence[i]['DATA']])
                trace.insert(sequence[i]['E_INDEX'], ['end', sequence[i]['ID']])

        return trace

    def __save_to_file(self, i_trace: list):
        """
        Save trace into a JSON file.
        :param i_trace: The final ordered trace as a list.
        :return: None
        """
        data = {}
        data['execution'] = i_trace
        with open(self.__m_output, 'w') as file:
            json.dump(data, file)



trace_generator = TraceGenerator("rules", "data", 500, 'trace_1000.json', 30, 3)
trace_generator.start()

