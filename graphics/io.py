from graphics.colors import Colors


class IO:

    @staticmethod
    def banner():
        print(f'''{Colors.RED}
                            ███╗   ███╗ ██████╗ ███╗   ██╗ █████╗ ███╗   ███╗██╗
                            ████╗ ████║██╔═══██╗████╗  ██║██╔══██╗████╗ ████║██║
                            ██╔████╔██║██║   ██║██╔██╗ ██║███████║██╔████╔██║██║
                            ██║╚██╔╝██║██║   ██║██║╚██╗██║██╔══██║██║╚██╔╝██║██║
                            ██║ ╚═╝ ██║╚██████╔╝██║ ╚████║██║  ██║██║ ╚═╝ ██║██║
                            ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝
                                                    
{Colors.DEFAULT}''')

    @staticmethod
    def seperator(i_title):
        print(f'{Colors.BLUE}{"#" * 50} ({i_title}) {"#" * 50}{Colors.DEFAULT}')

    @staticmethod
    def execution_details(i_details):
        print(f'{Colors.GREEN}{Colors.BOLD}[EXECUTION]: {i_details}{Colors.DEFAULT}')

    @staticmethod
    def error(i_error):
        print(f'{Colors.RED}[ERROR]: {i_error}{Colors.DEFAULT}')

    @staticmethod
    def info(i_message):
        print(f'\n[INFO]: {i_message}\n')

    @staticmethod
    def bdd_state(i_bdd_name, i_bdd_assignments):
        print(f'[{i_bdd_name}]: {i_bdd_assignments}')
