from abc import ABC, abstractmethod
from typing import Protocol
from collections import defaultdict


class Utils:
    """For colored messages/errors"""
    def error(message: str) -> None:
        print(f"\033[1;31m{message}\033[m")

    def display(message: any, tcol=(255, 255, 255),
                bcol=None, bold=False, ita=False, under=False,
                finish='\n', f=None) -> None:
        if tcol is None:
            tcol = (255, 255, 255)
        style = "1;" if bold else ""
        italic = "3;" if ita else ""
        underline = "4;" if under else ""
        bcolor = f"48;2;{bcol[0]};{bcol[1]};{bcol[2]}" if bcol else ""
        style = style+italic+underline+bcolor
        if (type(message) is dict or type(message) is list):
            for mes in message:
                print(f"\033[{style}38;2;{tcol[0]};{tcol[1]};{tcol[2]}"
                      f"m{mes}\033[0m",
                      end=finish, file=f)
            print("")
        else:
            print(f"\033[{style}38;2;{tcol[0]};{tcol[1]};{tcol[2]}"
                  f"m{message}\033[0m",
                  end=finish, file=f)

    simbols = {
        "ucl": "┐",
        "lcl": "┘",
        "ucr": "┌",
        "lcr": "└",
        "s": "─",
        "l": "│"
    }


class ProcessingPipeline(ABC):
    @abstractmethod
    def process(self, data: dict) -> dict:
        ...


class JSONAdapter(ProcessingPipeline):
    def process(self, pipeline_id: dict) -> dict:
        Utils.display("Transform: Formating Data...", (0, 255, 255),
                      bold=True)
        return pipeline_id


class CSVAdapter(ProcessingPipeline):
    def process(self, pipeline_id: dict) -> any:
        try:
            Utils.display("Transform: Structuring Data...", (0, 255, 255),
                          bold=True)
            val = ""
            for i in pipeline_id:
                if val:
                    val = val + f",'{i}','{pipeline_id.get(i)}'"
                else:
                    val = val + f"'{i}','{pipeline_id.get(i)}'"
            return val
        except TypeError:
            return None


class StreamAdapter(ProcessingPipeline):
    def process(self, pipeline_id) -> any:
        try:
            Utils.display("Transform: Adjusting Stream...", (0, 255, 255),
                          bold=True)
            val = ""
            for i in pipeline_id:
                if val:
                    val = val + f", {i} is {pipeline_id.get(i)}"
                else:
                    val = f"{i} is {pipeline_id.get(i)}"
            return val
        except TypeError:
            Utils.display("Stream Addapter Error: Invalid Type.",
                          (255, 0, 0), bold=True)
            return None


class ProcessingStage(Protocol):
    def process(pipeline, data) -> None:
        instage = InputStage()
        transtage = TransformStage()
        val = transtage.process(pipeline, instage.process(data))
        output = OuputStage()
        output.process(val)
        if val is None:
            Utils.display("Warning errors occured during the process.\n"
                          "The error has been stored for later display.",
                          (255, 255, 0))
            return "Fail"
        else:
            return "Success"


class InputStage:
    def process(self, data: dict) -> dict:
        Utils.display("Input: ", (0, 255, 255), bold=True, finish="")
        Utils.display(f'"{str(data)}"', (0, 0, 255), bold=True)
        return data


class TransformStage:
    def process(self, pipeline: ProcessingPipeline, data: dict) -> any:
        if not isinstance(data, dict):
            Utils.display("Error in transform stage, Invalid Format.",
                          (255, 0, 0), bold=True)
            return None
        try:
            return pipeline.process(data)
        except AttributeError:
            Utils.display("Error, could not call the value", (255, 0, 0),
                          bold=True)
            return None


class OuputStage:
    def process(self, data: dict) -> None:
        if isinstance(data, dict):
            Utils.display("\nOutput: \n", (0, 255, 255), bold=True,
                          finish="")
            for i in data:
                Utils.display(f"{i}: ", (0, 255, 255), finish="")
                Utils.display(f"{data.get(i)}", (0, 0, 255), ita=True)
        else:
            Utils.display("Output: ", (0, 255, 255), bold=True, finish="")
            Utils.display(f"{data}", (0, 0, 255), ita=True)


class NexusManager:
    def __init__(self) -> None:
        Utils.display(" ==> Initiating Nexus Manager...",
                      (255, 0, 0), None, True)
        Utils.display("Pipeline Capacity: ",
                      (0, 0, 255), finish="")
        Utils.display("Undefined",
                      (0, 255, 255), bold=True)
        Utils.display("\nCreating Data...", (0, 255, 125))
        self.pipelines = []
        self.Status = defaultdict(str)
        Utils.display("Setting up pipelines...", (200, 255, 200), ita=True)
        Utils.display("Setting up JSON...", (200, 255, 200), ita=True)
        Utils.display("Setting up CSV...", (200, 255, 200), ita=True)
        Utils.display("Setting up STREAM...", (200, 255, 200), ita=True)
        Utils.display("Completed !", (0, 255, 0), bold=True)

    def add_pipeline(self, pipeline: ProcessingPipeline) -> None:
        Utils.display("\nAdding Pipeline...",
                      (255, 155, 155), None, True)
        self.pipelines.append(pipeline)
        Utils.display(f"Pipeline {pipeline.__class__.__name__} added",
                      (155, 255, 155), ita=True)

    def process_data(self, data: dict) -> None:
        for i in self.pipelines:
            Utils.display(f"\n -> Calling {i.__class__.__name__}",
                          (0, 0, 255), ita=True)
            name = i.__class__.__name__
            self.Status[name] = ProcessingStage.process(i, data)
        Utils.display("\nDisplaying Status...", (0, 255, 155), bold=True)
        Utils.display("Datas have been Input -> transformed -> outputed.\n",
                      (155, 255, 155))
        for i in self.Status:
            Utils.display(f"{i} Status: ", (0, 255, 255), finish="", bold=True)
            Utils.display(f"{self.Status.get(i)}", (0, 0, 255))


def nexus_pipeline() -> None:
    testing_list = {"Login": "bgix",
                    "Status": 42,
                    "Project": "Python Module 5"}
    testing_fail = ["Trop Baka Les Amis", "Amogus"]
    manager = NexusManager()
    json = JSONAdapter()
    csv = CSVAdapter()
    stream = StreamAdapter()

    manager.add_pipeline(json)
    manager.add_pipeline(csv)
    manager.add_pipeline(stream)

    manager.process_data(testing_list)
    manager.process_data(testing_fail)


if __name__ == "__main__":
    nexus_pipeline()
