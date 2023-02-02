import datetime
import re


class BasicProcessors:

    def __init__(self) -> None:
        pass

#  Post Processors
class Integer(BasicProcessors):
    """Removes whatever whitespace to make a string valid for int casting but does not cast to integer. Characters and symbols are removed are ignored"""
    def __init__(self, initial_value:str) -> None:
        super().__init__()
        self.__value = initial_value

    def get_value(self) -> str:
        return "".join(self.__value.split())

class StringStripper(BasicProcessors):

    def __init__(self, initial_value:str) -> None:
        super().__init__()
        self.__value = initial_value

    def get_value(self) -> str:
        return str(self.__value.strip())

class ReplaceWith(BasicProcessors):

    def __init__(self, replace_item:str, with_item:str) -> None:
        super().__init__()
        self.__value = ""
        self.__first_item = str(replace_item)
        self.__second_item = str(with_item)

    def set_value(self, value:str):
        self.__value = str(value)
        return self

    def get_value(self) -> str:
        return self.__value.replace(self.__first_item, self.__second_item)

class RemoveChar(BasicProcessors):

    def __init__(self, char) -> None:
        super().__init__()
        self.__value = ""
        self.__char = str(char)

    def set_value(self, value:str):
        self.__value = str(value)
        return self

    def get_value(self) -> str:
        return self.__value.replace(self.__char, "")

class ToUpperCase(BasicProcessors):

    def __init__(self, initial_value:str) -> None:
        super().__init__()
        self.__value = initial_value

    def get_value(self) -> str:
        return self.__value.upper()

class ToLowerCase(BasicProcessors):

    def __init__(self, initial_value:str) -> None:
        super().__init__()
        self.__value = initial_value

    def get_value(self) -> str:
        return self.__value.lower()

class ExtractFromRegx(BasicProcessors):

    def __init__(self, regex) -> None:
        super().__init__()
        self.__regex = regex

    def set_value(self, value:str):
        self.__value = str(value)
        return self

    def get_value(self) -> str:
        substring = re.search(self.__regex, self.__value)
        if substring:
            return substring.group()
        else:
            return self.__value


class ToDatetime(BasicProcessors):

    def __init__(self, format) -> None:
        super().__init__()
        self.__format = format

    def set_value(self, value:str):
        self.value = str(value)
        return self

    def get_value(self) -> str:
        try:
            return datetime.datetime.strptime(self.value, self.__format)
        except:
            raise


class ToDate(ToDatetime):

    def __init__(self, format) -> None:
        super().__init__(format)
        self.__format = format

    def get_value(self) -> str:
        try:
            return datetime.datetime.strptime(self.value, self.__format).date()
        except:
            raise


#  Evaluators
# NB: Evaluators evaluate() method always return a boolean value
class EqualsTo(BasicProcessors):
    """This conditional processor is used to evaluate if a value is equals to another or not"""


    def __init__(self, conditional_value) -> None:
        super().__init__()
        self.__conditional_value = conditional_value

    
    def evaluate(self, comparative) -> bool:
        """evaluates the equals to condition"""
        return self.__conditional_value == comparative

class NoteEquals(BasicProcessors):
    def __init__(self, conditional_value)->None:
        super().__init__()
        self.__conditional_value = conditional_value
    
    def evaluate(self, comparative) -> bool:
        return not self.__conditional_value == comparative

class GreatherOrEqual(BasicProcessors):
    """This conditional processor is used to evaluate if a value is greather than to another or not"""

    def __init__(self, conditional_value) -> None:
        super().__init__()
        self.__conditional_value = conditional_value

    
    def evaluate(self, comparative) -> bool:
        """evaluates the equals to condition"""
        return comparative >= self.__conditional_value