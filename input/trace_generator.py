import random
import json
import string
import sys

def read_json(i_json_file):
    with open(i_json_file, "r") as json_file:
        data = json.load(json_file)
    return data

class TraceGenerator:

    def __init__(self, i_nums_of_interval, i_output, i_rules_percentage):
        self.__m_num_of_intervals = i_nums_of_interval
        self.__m_trace_length = i_nums_of_interval * 2
        self.__m_interval_ids = list(range(0, i_nums_of_interval))
        self.__m_output = i_output
        self.__m_rules_percentage = i_rules_percentage
        self.__m_rules = read_json('rules')
        self.__m_data = read_json('data')
        self.__m_data_length = len(self.__m_data)
        self.__num_of_rules = 0
        self.__num_of_repeats = 0
        self.__num_of_manage_events = 0

    def start(self):
        self.__rules_init()
        management_sequence = self.__initilaize_rules_intervals()
        full_trace = self.__generate_random_trace(management_sequence)
        self.__save_to_file(full_trace)

    def __rules_init(self):
        if self.__m_rules_percentage < 0 or self.__m_rules_percentage > 100:
            print(f"[ERROR]: percentage must be between 0 to 100")
            sys.exit()

        for rule in self.__m_rules:
            self.__num_of_rules += len(rule.keys())

        self.__num_of_repeats = ((self.__m_num_of_intervals * self.__m_rules_percentage) // 100) // self.__num_of_rules

    def __initilaize_rules_intervals(self):
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
                                                                    rule[str(i)]['E_PRIORITY'] - rule[str(i)]['B_PRIORITY'],
                                                                    end_block_index -
                                                            (len(rule.keys()) * 2) + rule[str(i)]['E_PRIORITY'])
                        priorities[rule[str(i)]['E_PRIORITY']] = sequence[-1][i]['E_INDEX']
                    else:
                        sequence[-1][i]['B_INDEX'] = self.__find_range(rule[str(i)]['B_PRIORITY'], priorities,
                                                                       rule, end_block_index)
                        priorities[rule[str(i)]['B_PRIORITY']] = sequence[-1][i]['B_INDEX']
                        sequence[-1][i]['E_INDEX'] = self.__find_range(rule[str(i)]['E_PRIORITY'], priorities,
                                                                       rule, end_block_index)
                        priorities[rule[str(i)]['E_PRIORITY']] = sequence[-1][i]['E_INDEX']
                    self.__num_of_manage_events += 1
                print(priorities)
                start_block_index = end_block_index + 1
                end_block_index += sequence_block_size

        return sequence

    def __find_range(self, i_curr_priority, i_seen_priorities, i_rule, i_end_block_index):
        min_priority = min(i_seen_priorities.keys())
        max_priority = max(i_seen_priorities.keys())
        if i_curr_priority < min_priority:
            index = random.randint(i_curr_priority,
                                   i_seen_priorities[min_priority] - min_priority + i_curr_priority)
        elif i_curr_priority > max_priority:
            index = random.randint(i_seen_priorities[max_priority] + i_curr_priority - max_priority,
                                   i_end_block_index - (len(i_rule.keys()) * 2) + i_curr_priority)
        else:
            higher_index = i_seen_priorities[max_priority]
            lower_index = i_seen_priorities[min_priority]
            for seen_priority in i_seen_priorities.keys():
                if i_curr_priority < seen_priority and seen_priority < max_priority:
                    higher_index = i_seen_priorities[seen_priority]
                    max_priority = seen_priority
                elif i_curr_priority > seen_priority and seen_priority > min_priority:
                    lower_index = i_seen_priorities[seen_priority]
                    min_priority = seen_priority
            index = random.randint(lower_index + i_curr_priority - min_priority,
                                   higher_index - max_priority + i_curr_priority)
        return index

    def __interval_id_generator(self, size=10, chars=string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))

    def __generate_random_trace(self, i_management_sequence):
        intervals = []
        for i in range(self.__m_num_of_intervals - self.__num_of_manage_events):
            name = self.__interval_id_generator()
            start = random.randint(0, 5000000)
            intervals.append([name, 'begin', start])
            intervals.append([name, 'end', random.randint(start, 5000000)])
        intervals.sort(key=lambda x: x[2])
        trace = []

        for interval in intervals:
            if interval[1] == 'begin':
                data = self.__m_data[interval[2] % self.__m_data_length]
                trace.append([interval[1], interval[0], data])
            else:
                trace.append([interval[1], interval[0]])

        for sequence in i_management_sequence:
            for i in range(len(sequence.keys())):
                trace.insert(sequence[i]['B_INDEX'], ['begin', sequence[i]['ID'], sequence[i]['DATA']])
                trace.insert(sequence[i]['E_INDEX'], ['end', sequence[i]['ID']])

        return trace

    def __save_to_file(self, i_trace):
        data = {}
        data['execution'] = i_trace
        with open(self.__m_output, 'w') as file:
            json.dump(data, file)



a = TraceGenerator(500, 'trace_16000.json', 50)
a.start()

