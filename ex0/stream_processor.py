from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional


class Utils:
    """For colored messages/errors"""
    def error(message: str) -> None:
        print(f"\033[1;31m{message}\033[m")

    def Print(message: any, tcol=(255, 255, 255),
              bcol=(0, 0, 0), bold=False, ita=False, under=False,
              finish='\n', f=None) -> None:
        if bcol is None:
            bcol = (0, 0, 0)
        if tcol is None:
            tcol = (255, 255, 255)
        style = "1;" if bold else ""
        italic = "3;" if ita else ""
        underline = "4;" if under else ""
        style = style+italic+underline
        if (type(message) is dict or type(message) is list):
            for mes in message:
                print(f"\033[{style}38;2;{tcol[0]};{tcol[1]};{tcol[2]}"
                      f";48;2;{bcol[0]};{bcol[1]};{bcol[2]}m{mes}\033[0m",
                      end=finish, file=f)
            print("")
        else:
            print(f"\033[{style}38;2;{tcol[0]};{tcol[1]};{tcol[2]}"
                  f";48;2;{bcol[0]};{bcol[1]};{bcol[2]}m{message}\033[0m",
                  end=finish, file=f)


class DataProcessor(ABC):
    @abstractmethod
    def process(self, data: any) -> str:
        pass

    @abstractmethod
    def validate(self, data: any) -> bool:
        pass

    @abstractmethod
    def format_output(self, result: str) -> str:
        pass


class NumericProcessor(DataProcessor):
    def process(self, data: any) -> str:
        Utils.Print("\nProcessing data...",
                    (0, 255, 255))
        return (str(data))

    def validate(self, data: any) -> bool:
        Utils.Print("\nValidating data...",
                    (0, 255, 255))
        if data is None:
            Utils.Print("Validation Failed, Data doesn't exist.",
                        (255, 0, 0), None, False, True)
            return False
        else:
            Utils.Print("Validation Success, Data Exist !",
                        (0, 255, 0), None, False, True)
            return True

    def format_output(self, result: str) -> str:
        pass


def stream_processor() -> None:
    Utils.Print("=== Data proccessing ===",
                [255, 0, 255], None, True, False)
    Utils.Print("-> Starting Numeric Processor",
                [255, 0, 255], None, False, True, True)
    np = NumericProcessor()
    value = ["Baka", "Trop"]
    Utils.Print(f"[1] Proccessed: {np.process(value)}",
                None, None, False, False, True)
    Utils.Print(f"[2] Validating: {np.validate(value)}\n",
                None, None, False, False, True)


if __name__ == "__main__":
    stream_processor()
