from graphics.colors import Colors


class IO:

    @staticmethod
    def banner():
        print(f'''{Colors.RED}
{" " * 55}███╗   ███╗ ██████╗ ███╗   ██╗ █████╗ ███╗   ███╗██╗
{" " * 55}████╗ ████║██╔═══██╗████╗  ██║██╔══██╗████╗ ████║██║
{" " * 55}██╔████╔██║██║   ██║██╔██╗ ██║███████║██╔████╔██║██║
{" " * 55}██║╚██╔╝██║██║   ██║██║╚██╗██║██╔══██║██║╚██╔╝██║██║
{" " * 55}██║ ╚═╝ ██║╚██████╔╝██║ ╚████║██║  ██║██║ ╚═╝ ██║██║
{" " * 55}╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝
                                                    
{Colors.DEFAULT}''')

    @staticmethod
    def seperator(i_title):
        num_of_chars = 80 - (len(i_title) // 2)
        print(f'{Colors.BLUE}{"#" * num_of_chars} ({i_title}) {"#" * num_of_chars}{Colors.DEFAULT}')

    @staticmethod
    def event_header(i_event):
        print(f'{Colors.BOLD}|-- [EVENT]: {i_event}{Colors.DEFAULT}')

    @staticmethod
    def ast_header(i_event):
        print(f'{Colors.BOLD}    |-- [AST]: {i_event}{Colors.DEFAULT}')

    @staticmethod
    def execution(i_details):
        print(f'{Colors.BOLD}[EXECUTION]: {i_details}{Colors.DEFAULT}\n')

    @staticmethod
    def property(i_details):
        print(f'{Colors.BOLD}[PROPERTY]: {i_details}{Colors.DEFAULT}\n')

    @staticmethod
    def error(i_error):
        print(f'{Colors.RED}[ERROR]: {i_error}{Colors.DEFAULT}')

    @staticmethod
    def info(i_message):
        print(f'\n{Colors.BOLD}[INFO]:{Colors.DEFAULT} {i_message}\n')

    @staticmethod
    def subformula(i_op, i_message):
        print(f'{Colors.BLUE}        |-- [{i_op}]:{Colors.DEFAULT} {i_message}')

    @staticmethod
    def bdd_state(i_bdd_name, i_bdd_assignments):
        print(f'{Colors.BLUE}    |-- [{i_bdd_name}]:{Colors.DEFAULT} {i_bdd_assignments}')

    @staticmethod
    def false():
        IO.info(f'{Colors.RED}{Colors.BOLD}Specification result is False')

    @staticmethod
    def true():
        IO.info(f'{Colors.GREEN}{Colors.BOLD}Specification result is True')


