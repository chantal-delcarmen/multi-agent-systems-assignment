from aegis.command_line_reader.option import Option


class CommandLineReader:
    INT = 0
    LONG = 1
    DOUBLE = 2
    STRING = 3
    BOOL = 4

    def __init__(self) -> None:
        self._option_list: list[Option] = []
        self._error_output: str = ""

    def read_cmd_line_args(self, args: list[str]) -> bool:
        for option in self._option_list:
            option.is_set = False

        arg_index = 0
        while arg_index < len(args):
            if args[arg_index].startswith("-"):
                option_name = args[arg_index].lstrip("-")
                option = None

                for opt in self._option_list:
                    if opt.name == option_name:
                        option = opt
                        break

                if option:
                    arg_index += 1
                    if arg_index < len(args):
                        self._read_value(option, args[arg_index])
            arg_index += 1

        result = True
        for option in self._option_list:
            if not option.is_set and option.is_required:
                print(f"Forgot required value: -{option.name}.")
                result = False

        if not result:
            print(self._error_output)
        return result

    def add_option(self, option: Option) -> None:
        self._option_list.append(option)

    def set_error_output(self, error_output: str) -> None:
        self._error_output = error_output

    def _read_value(self, option: Option, value_string: str) -> None:
        if option.value_type in (self.INT, self.LONG):
            option.value = int(value_string)
            option.is_set = True
        elif option.value_type == self.STRING:
            option.value = value_string
            option.is_set = True
        elif option.value_type == self.DOUBLE:
            option.value = float(value_string)
            option.is_set = True
        elif option.value_type == self.BOOL:
            option.value = value_string.lower() == "true"
            option.is_set = True

    def get_option(self, name: str) -> Option | None:
        for option in self._option_list:
            if option.name == name:
                return option
        return None
