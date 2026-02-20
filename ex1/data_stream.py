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
    def filter_data(self, data_batch: List[any],
                    critera: Optional[str]) -> List[any]:
        if isinstance(data_batch, list) is False:
            data_batch = [data_batch]
        new = list()
        count = 0
        for i in data_batch:
            if isinstance(i, critera) is True:
                new.append(i)
            else:
                count += 1
        Utils.Display(" > Default Filtering result: Success !",
                      (155, 255, 155))
        Utils.Display(f" > Removed {count} unwanted values",
                      (105, 105, 255))
        try:
            self.Errors += count
        except AttributeError:
            self.Errors = count
        self.Data = new
        return (new)

    @abstractmethod
    def get_stats(self) -> dict[str, Union[str, int, float]]:
        Utils.Display("\nDefault stats display...", (155, 0, 155), None,
                      False, True)
        for i, v in self.__dict__.items():
            Utils.Display(f"\n{i}: {v}", (155, 0, 155), None,
                          False, True)
        pass


class SensorStream(DataStream):
    """Child of data stream"""
    def process_batch(self, data_batch: List[any]) -> str:
        try:
            if isinstance(data_batch, int) is True:
                data_batch = [data_batch]
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
                    Utils.Display(f" ! Movement of {i} started at {count}",
                                  (155, 0, 155))
                elif i < last and i != main:
                    Utils.Display(f" - Movement of {i} decreased at {count}",
                                  (155, 0, 155))
                elif i > last and i > main:
                    Utils.Display(f" + Movement of {i} increased at {count}",
                                  (155, 0, 155))
                elif i != last and i == main:
                    Utils.Display(f"   Movement stabilized to {i} at {count}",
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
            return ("Process Failed")
        except ValueError:
            Utils.Display("Only a list of int needs to be provided !",
                          (255, 255, 0), None, True, False, False)
            return ("Process Failed")

    def filter_data(self, data_batch: List[any], critera: Optional[str]):
        return (super().filter_data(data_batch, critera))

    def get_stats(self) -> dict[str, Union[str, int, float]]:
        unwanted = "<not found>"
        dats = "<not foumd>"
        try:
            unwanted = self.Errors
            dats = len(self.Data)
        except AttributeError:
            pass
        Utils.Display(f"Total Unwanted value removed: {unwanted}\n"
                      f"Total list length: {dats}",
                      (255, 0, 255))
        return ({"Unwanted Removed": unwanted, "List Length": dats})


class TransactionStream(DataStream):
    """Child of data stream"""
    def process_batch(self, data_batch: List[any]) -> str:
        Utils.Display("\nInitiating Transaction...", (155, 0, 155), None,
                      False, True)
        self.Bank = 0
        self.Transaction = 0
        try:
            for i in data_batch:
                self.Bank += i
        except ValueError:
            Utils.Display("The bank does not accept other currency than ints",
                          (255, 0, 0))
            return ("Denied")
        Utils.Display(f"The bank holds {self.Bank} ints",
                      (255, 0, 0))
        return (f"{str(self.Bank)} ints")

    def filter_data(self, data_batch: List[any], critera: Optional[str]):
        Utils.Display("\nFiltering Transaction...", (155, 0, 155), None,
                      False, True)
        new = super().filter_data(data_batch, critera)
        for i in new:
            self.Bank -= i
            self.Transaction += 1
        Utils.Display(f"The bank now holds {self.Bank} ints after"
                      f" {self.Transaction} Transactions",
                      (255, 0, 0))
        return (new)

    def get_stats(self) -> dict[str, Union[str, int, float]]:
        Utils.Display("\nInformation of the bank...", (155, 0, 155), None,
                      False, True)
        Utils.Display(f"The bank holds {self.Bank} ints"
                      f"\nYou made a total of {self.Transaction} Transactions"
                      "\nThe bank thanks you for your trust.",
                      (255, 0, 255))


class EventStream(DataStream):
    """Child of data stream"""
    def process_batch(self, data_batch: List[any]) -> str:
        Utils.Display("\nInitiating Events...", (155, 0, 155), None,
                      False, True)
        self.events = list()
        for i in data_batch:
            self.events.append(i)
        Utils.Display(f"There are {len(self.events)} events",
                      (255, 0, 0))
        return ("Success")

    def filter_data(self, data_batch: List[any], critera: Optional[str]):
        bad = list()
        Utils.Display("\nFiltering Events...", (155, 0, 155), None,
                      False, True)
        for i in data_batch:
            if isinstance(i, critera) is False:
                bad.append(i)
        Utils.Display(f"The given list have {len(bad)} unvalid events",
                      (255, 0, 0))
        return (bad)

    def get_stats(self) -> dict[str, Union[str, int, float]]:
        super().get_stats()


def data_stream() -> None:
    ss = SensorStream()
    dats = [0, 0, 2, 1, 0, 0, 1, 4, 6, 8, 0, 0, 0, 0, "a", "b"]
    Utils.Display(ss.process_batch(dats),
                  (0, 0, 255))
    Utils.Display(ss.filter_data(dats,
                                 int),
                  (0, 0, 255), None, False, False, False, ", ")
    ss.get_stats()
    ts = TransactionStream()
    ts.process_batch([500, 215])
    ts.filter_data([250, 215], int)
    ts.get_stats()

    es = EventStream()
    dats = ["process", "checking", "endstatus", 42]
    es.process_batch(dats)
    es.filter_data(dats, str)
    es.get_stats()


if __name__ == "__main__":
    data_stream()
