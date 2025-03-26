from typing import override

class Param:
    INT_PARAM = 0
    FLOAT_PARAM = 1
    STRING_PARAM = 2

    def __init__(self, value: int | float | str):
        if isinstance(value, int):
            self.param_type = self.INT_PARAM
            self.int_param = value
        elif isinstance(value, float):
            self.param_type = self.FLOAT_PARAM
            self.float_param = value
        else:
            self.param_type = self.STRING_PARAM
            self.string_param = value

    @override
    def __str__(self) -> str:
        if self.param_type == self.INT_PARAM:
            return str(self.int_param)
        elif self.param_type == self.FLOAT_PARAM:
            return str(self.float_param)
        else:
            return self.string_param

    @staticmethod
    def param_list_to_string(param_list: list['Param']) -> str:
        return "( " + " , ".join(str(param) for param in param_list) + " )"