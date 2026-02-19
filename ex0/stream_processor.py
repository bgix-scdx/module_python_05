from abc import ABC, abstractmethod


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


class DataProcessor(ABC):
    """Base that create the base abstract functions"""
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
    """Process numbers, functions are inherited from DataProcessor"""
    """Since they are abstract they are re-defined here"""
    def process(self, data: any) -> str:
        Utils.Display("\nProcessing data...",
                      (0, 255, 255))
        return (str(data))

    def validate(self, data: any) -> bool:
        Utils.Display("\nValidating data...",
                      (0, 255, 255))
        is_num = True
        for i in data:
            if type(i) is not int:
                is_num = False
                break
        if is_num is False:
            Utils.Display("Validation Failed, is not int.",
                          (255, 0, 0), None, False, True)
            return False
        else:
            Utils.Display("Validation Success, Data is an int !",
                          (0, 255, 0), None, False, True)
            return True

    def format_output(self, result: str) -> str:
        count = 0
        Utils.Display("Checking the the ints...",
                      (0, 255, 255))
        nums = list()
        count = 0
        total = 0
        for i in result:
            if i.isdecimal():
                total += int(i)
                nums.append(int(i))
                count += 1
        return (f"{count} numbers, sum = {total}, avg = {total/count} ")


class TextProcessor(DataProcessor):
    """process text"""
    def process(self, data: any) -> str:
        Utils.Display("\nProcessing data...",
                      (0, 255, 255))
        return (str(data))

    def validate(self, data: any) -> bool:
        Utils.Display("\nValidating data...",
                      (0, 255, 255))
        if data is None:
            Utils.Display("Validation Failed, Data doesn't exist.",
                          (255, 0, 0), None, False, True)
            return False
        else:
            Utils.Display("Validation Success, Data Exist !",
                          (0, 255, 0), None, False, True)
            return True

    def format_output(self, result: str) -> str:
        count = 0
        Utils.Display("Checking the ammount of characters...",
                      (0, 255, 255))
        for i in result:
            count += 1
        return (str(count))


class LogProcessor(DataProcessor):
    """proccess if nil"""
    def process(self, data: any) -> str:
        Utils.Display("\nProcessing data...",
                      (0, 255, 255))
        return (str(data))

    def validate(self, data: any) -> bool:
        Utils.Display("\nValidating data...",
                      (0, 255, 255))
        if data is None:
            Utils.Display("Validation Failed, data is None.",
                          (255, 0, 0), None, False, True)
            return False
        else:
            Utils.Display("Validation Success, Data is not None!",
                          (0, 255, 0), None, False, True)
            return True

    def format_output(self, result: str) -> str:
        Utils.Display("Checking the the data",
                      (0, 255, 255))
        if result is None:
            Utils.Display("Error, Result is None",
                          (255, 0, 0))
            return (False)
        else:
            return (True)


def stream_processor() -> None:
    Utils.Display("=== Data proccessing ===",
                  [255, 0, 255], None, True, False)
    Utils.Display("-> Starting Text Processor",
                  [255, 0, 0], None, True, True, False)
    tp = TextProcessor()
    value = ["Baka", "Trop"]
    Utils.Display(f"[1] Proccessed: {tp.process(value)}",
                  (255, 0, 125), None, False, False, True)
    Utils.Display(f"[2] Validating: {tp.validate(value)}\n",
                  (255, 0, 125), None, False, False, True)
    Utils.Display(f"[3] Output: {tp.format_output(str(value))}\n",
                  (255, 0, 125), None, False, False, True)
    Utils.Display("\n-> Starting Numeric Processor",
                  [255, 0, 0], None, True, True, False)
    value = [1, 2, 3, 4, 5]
    np = NumericProcessor()
    Utils.Display(f"[1] Proccessed: {np.process(value)}",
                  (255, 0, 125), None, False, False, True)
    Utils.Display(f"[2] Proccessed: {np.validate(value)}\n",
                  (255, 0, 125), None, False, False, True)
    Utils.Display(f"[3] Output: {np.format_output(str(value))}\n",
                  (255, 0, 125), None, False, False, True)
    value = None
    lp = LogProcessor()
    Utils.Display(f"[1] Proccessed: {lp.process(value)}",
                  (255, 0, 125), None, False, False, True)
    Utils.Display(f"[2] Proccessed: {lp.validate(value)}\n",
                  (255, 0, 125), None, False, False, True)
    Utils.Display(f"[3] Output: {lp.format_output(value)}\n",
                  (255, 0, 125), None, False, False, True)


if __name__ == "__main__":
    stream_processor()
