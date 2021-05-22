from colorama import Fore, init, Style


class IO:
    init(convert=True)

    @staticmethod
    def banner():
        print(f'''{Fore.RED}
{" " * 55}███╗   ███╗ ██████╗ ███╗   ██╗ █████╗ ███╗   ███╗██╗
{" " * 55}████╗ ████║██╔═══██╗████╗  ██║██╔══██╗████╗ ████║██║
{" " * 55}██╔████╔██║██║   ██║██╔██╗ ██║███████║██╔████╔██║██║
{" " * 55}██║╚██╔╝██║██║   ██║██║╚██╗██║██╔══██║██║╚██╔╝██║██║
{" " * 55}██║ ╚═╝ ██║╚██████╔╝██║ ╚████║██║  ██║██║ ╚═╝ ██║██║
{" " * 55}╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝
                                                    
{Style.RESET_ALL}''')

    @staticmethod
    def seperator(i_title):
        num_of_chars = 80 - (len(i_title) // 2)
        print(f'{Fore.LIGHTCYAN_EX}{"#" * num_of_chars} ({i_title}) {"#" * num_of_chars}{Style.RESET_ALL}')

    @staticmethod
    def event_header(i_event):
        print(f'{Style.BRIGHT}|-- [EVENT]: {i_event}{Style.RESET_ALL}')

    @staticmethod
    def enumeration(i_interval, i_bitstring):
        print(f'{Style.BRIGHT}{Fore.MAGENTA}|-- [ENUMERATION]: {i_interval} -> "{i_bitstring}" '
              f'({[True if bit == "1" else False for bit in i_bitstring]}){Style.RESET_ALL}')

    @staticmethod
    def ast_header():
        print(f'{Style.BRIGHT}    |-- [AST]:{Style.RESET_ALL}')

    @staticmethod
    def execution(i_details):
        print(f'{Style.BRIGHT}[EXECUTION]: {i_details}{Style.RESET_ALL}\n')

    @staticmethod
    def property(i_details):
        print(f'{Style.BRIGHT}[PROPERTY]: {i_details}{Style.RESET_ALL}\n')

    @staticmethod
    def error(i_error):
        print(f'{Fore.RED}[ERROR]: {i_error}{Style.RESET_ALL}')

    @staticmethod
    def info(i_message):
        print(f'\n{Style.BRIGHT}[INFO]:{Style.RESET_ALL} {i_message}\n')

    @staticmethod
    def subformula(i_op, i_message):
        print(f'{Fore.LIGHTCYAN_EX}        |-- [{i_op}]:{Style.RESET_ALL} {i_message}')

    @staticmethod
    def bdd_state(i_bdd_name, i_bdd_assignments):
        print(f'{Fore.LIGHTCYAN_EX}    |-- [{i_bdd_name}]:{Style.RESET_ALL} {i_bdd_assignments}')

    @staticmethod
    def false():
        IO.info(f'{Fore.RED}{Style.BRIGHT}Specification result is False')

    @staticmethod
    def true():
        IO.info(f'{Fore.GREEN}{Style.BRIGHT}Specification result is True')

    @staticmethod
    def final(i_execution, i_property, i_bdds):
        IO.seperator('FINAL STATE')
        IO.execution(i_execution)
        IO.property(i_property)
        for bdd_name, bdd_data in i_bdds:
            IO.bdd_state(bdd_name, bdd_data)
        IO.seperator('THE END')

    @staticmethod
    def verdict(i_verdict):
        if i_verdict:
            return f'{Fore.BLUE}{i_verdict}{Style.RESET_ALL}'
        else:
            return f'{Fore.RED}{i_verdict}{Style.RESET_ALL}'

    @staticmethod
    def verdicts(i_verdicts):
        IO.seperator('VERDICTS BY ITERATION')
        for i, verdict in enumerate(i_verdicts):
            print(f'[EVENT {i+1}]: {IO.verdict(verdict)}')


