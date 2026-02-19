from abc import ABC, abstractmethod
from typing import Union, Optional, List


class Utils:
    """For colored messages/errors"""
    def error(message: str) -> None:
        print(f"\033[1;31m{message}\033[m")

    def Display(message: any, tcol=(255, 255, 255),
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


class DataStream(ABC):
    """Base ground for the children clases"""
    @abstractmethod
    def process_batch(self, data_batch: List[any]) -> str:
        pass

    @abstractmethod
    def filter_data(self, data_batch: List[any], critera: Optional[str]):
        pass

    @abstractmethod
    def get_stats(self) -> dict[str, Union[str, int, float]]:
        pass


class SensorStream(DataStream):
    """Child of data stream"""
    def process_batch(self, data_batch: List[any]) -> str:
        try:
            main = data_batch[0]
            Utils.Display("Processing Movement...",
                          (255, 255, 0), None, False, False, True)
            last = main
            count = -1
            for i in data_batch:
                int(i)
                count += 1
                if i == main and last == i:
                    continue
                elif i != last and last == main:
                    Utils.Display(f" - Movement of {i} started at {count}",
                                  (155, 0, 155))
                elif i < last and i != main:
                    Utils.Display(f" - Movement of {i} decreased at {count}",
                                  (155, 0, 155))
                elif i > last and i > main:
                    Utils.Display(f" - Movement of {i} increased at {count}",
                                  (155, 0, 155))
                elif i != last and i == main:
                    Utils.Display(f" - Movement stabilized to {i} at {count}",
                                  (155, 0, 155))
                last = i
            return ("Processing Ended")
        except IndexError:
            Utils.Display("A list need to be provided !",
                          (255, 255, 0), None, True, False, False)
            return ("Process Failed")
        except TypeError:
            Utils.Display("Only a list of int needs to be provided !",
                          (255, 255, 0), None, True, False, False)
        except ValueError:
            Utils.Display("Only a list of int needs to be provided !",
                          (255, 255, 0), None, True, False, False)
            return ("Process Failed")

    def filter_data(self, data_batch: List[any], critera: Optional[str]):
        pass

    def get_stats(self) -> dict[str, Union[str, int, float]]:
        pass


class TransactionStream(DataStream):
    """Child of data stream"""
    def process_batch(self, data_batch: List[any]) -> str:
        pass

    def filter_data(self, data_batch: List[any], critera: Optional[str]):
        pass

    def get_stats(self) -> dict[str, Union[str, int, float]]:
        pass


class EventStream(DataStream):
    """Child of data stream"""
    def process_batch(self, data_batch: List[any]) -> str:
        pass

    def filter_data(self, data_batch: List[any], critera: Optional[str]):
        pass

    def get_stats(self) -> dict[str, Union[str, int, float]]:
        pass


def data_stream() -> None:
    ss = SensorStream()
    Utils.Display(ss.process_batch([5, 5, 5, 4, 3, 2, 1, 5, 5, 5, 1, 5, "a"]),
                  (0, 0, 255))


if __name__ == "__main__":
    data_stream()
