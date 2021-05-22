import random
import json
import string


class TraceGenerator:
    DATA = ['BOOT', 'DL_IMAGE', 'DL_MOBPRM', 'DL_ARMPRM', 'DL_FAIL',
            'INS_ON', 'INS_FAIL', 'INS_RECOVER', 'GET_CAMDATA', 'STARVE']

    RULES = [
        {
            'REPEAT': 6,
            0: {'DATA': 'BOOT', 'B_PRIORITY': 0, 'E_PRIORITY': 2},
            1: {'DATA': 'DL_IMAGE', 'B_PRIORITY': 1, 'E_PRIORITY': 3},
            2: {'DATA': 'BOOT', 'B_PRIORITY': 4, 'E_PRIORITY': 5}
        },
        {
            'REPEAT': 3,
            0: {'DATA': 'BOOT', 'B_PRIORITY': 0, 'E_PRIORITY': 3},
            1: {'DATA': 'DL_IMAGE', 'B_PRIORITY': 1, 'E_PRIORITY': 2},
            2: {'DATA': 'BOOT', 'B_PRIORITY': 4, 'E_PRIORITY': 5}
        },
        {
            'REPEAT': 3,
            0: {'DATA': 'DL_MOBPRM', 'B_PRIORITY': 0, 'E_PRIORITY': 3},
            1: {'DATA': 'DL_FAIL', 'B_PRIORITY': 1, 'E_PRIORITY': 2}
        },
        {
            'REPEAT': 3,
            0: {'DATA': 'DL_ARMPRM', 'B_PRIORITY': 0, 'E_PRIORITY': 3},
            1: {'DATA': 'DL_FAIL', 'B_PRIORITY': 1, 'E_PRIORITY': 2}
        },
        {
            'REPEAT': 3,
            0: {'DATA': 'INS_ON', 'B_PRIORITY': 0, 'E_PRIORITY': 1},
            1: {'DATA': 'INS_FAIL', 'B_PRIORITY': 2, 'E_PRIORITY': 3},
            2: {'DATA': 'INS_RECOVER', 'B_PRIORITY': 6, 'E_PRIORITY': 7},
            3: {'DATA': 'INS_ON', 'B_PRIORITY': 4, 'E_PRIORITY': 5}
        },
        {
            'REPEAT': 3,
            0: {'DATA': 'DL_IMAGE', 'B_PRIORITY': 0, 'E_PRIORITY': 5},
            1: {'DATA': 'GET_CAMDATA', 'B_PRIORITY': 1, 'E_PRIORITY': 4},
            2: {'DATA': 'STARVE', 'B_PRIORITY': 2, 'E_PRIORITY': 3}
        }
    ]

    def __init__(self, i_nums_of_interval, i_output):
        self.__m_num_of_intervals = i_nums_of_interval
        self.__m_trace_length = i_nums_of_interval * 2
        self.__m_data_length = len(TraceGenerator.DATA)
        self.__m_interval_ids = list(range(0, i_nums_of_interval))
        self.__m_output = i_output
        self.__num_of_rules = 0

    def start(self):
        managment_sequence = self.__initilaize_rules_intervals()
        full_trace = self.__generate_random_trace(managment_sequence)
        self.__save_to_file(full_trace)

    def __initilaize_rules_intervals(self):
        sequence = []
        for rule in TraceGenerator.RULES:
            sequence_block_size = self.__m_trace_length // rule['REPEAT']
            start_block_index = 0
            end_block_index = sequence_block_size
            for repeat in range(rule['REPEAT']):
                sequence.append({})
                priorities = {}
                for i in range(len(rule.keys()) - 1):
                    sequence[-1][i] = {}
                    sequence[-1][i]['DATA'] = rule[i]['DATA']
                    sequence[-1][i]['ID'] = self.__interval_id_generator()
                    if i == 0:
                        sequence[-1][i]['B_INDEX'] = random.randint(start_block_index + rule[i]['B_PRIORITY'],
                                                                    end_block_index -
                                                            (len(rule.keys()) * 2) + rule[i]['B_PRIORITY'])
                        priorities[rule[i]['B_PRIORITY']] = sequence[-1][i]['B_INDEX']
                        sequence[-1][i]['E_INDEX'] = random.randint(sequence[-1][i]['B_INDEX'] +
                                                                    rule[i]['E_PRIORITY'] - rule[i]['B_PRIORITY'],
                                                                    end_block_index -
                                                            (len(rule.keys()) * 2) + rule[i]['E_PRIORITY'])
                        priorities[rule[i]['E_PRIORITY']] = sequence[-1][i]['E_INDEX']
                    else:
                        sequence[-1][i]['B_INDEX'] = self.__find_range(rule[i]['B_PRIORITY'], priorities,
                                                                       rule, end_block_index)
                        priorities[rule[i]['B_PRIORITY']] = sequence[-1][i]['B_INDEX']
                        sequence[-1][i]['E_INDEX'] = self.__find_range(rule[i]['E_PRIORITY'], priorities,
                                                                       rule, end_block_index)
                        priorities[rule[i]['E_PRIORITY']] = sequence[-1][i]['E_INDEX']
                    self.__num_of_rules += 1
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

    def __generate_random_trace(self, i_managment_sequence):
        intervals = []
        for i in range(self.__m_num_of_intervals - self.__num_of_rules):
            name = self.__interval_id_generator()
            start = random.randint(0, 5000000)
            intervals.append([name, 'begin', start])
            intervals.append([name, 'end', random.randint(start, 5000000)])
        intervals.sort(key=lambda x: x[2])
        trace = []

        for interval in intervals:
            if interval[1] == 'begin':
                data = TraceGenerator.DATA[interval[2] % self.__m_data_length]
                trace.append([interval[1], interval[0], data])
            else:
                trace.append([interval[1], interval[0]])

        for sequence in i_managment_sequence:
            for i in range(len(sequence.keys())):
                trace.insert(sequence[i]['B_INDEX'], ['begin', sequence[i]['ID'], sequence[i]['DATA']])
                trace.insert(sequence[i]['E_INDEX'], ['end', sequence[i]['ID']])

        return trace

    def __save_to_file(self, i_trace):
        data = {}
        data['execution'] = i_trace
        with open(self.__m_output, 'w') as file:
            json.dump(data, file)



a = TraceGenerator(500, 'test1.json')
a.start()

