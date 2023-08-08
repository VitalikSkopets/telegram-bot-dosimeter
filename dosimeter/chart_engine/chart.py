import os
import pathlib

import matplotlib
import matplotlib.pyplot as plt

from dosimeter.parse.parser import RegionInfoDTO

matplotlib.use("agg")


class ChartEngine(object):
    """
    A class designed to create png files with a chart.
    """

    file_name = "bar-chart.png"

    def __init__(self, dir_path: pathlib.Path) -> None:
        """
        Instantiate a GraphEngine instance.
        """
        self.dir_path = dir_path
        if pathlib.Path(self.dir_path).exists():
            return
        self.dir_path.mkdir(exist_ok=True)

    def create(self, data: RegionInfoDTO) -> None:
        """
        A method for rendering a chart and writing it to a file.
        """
        title = data.region
        names = data.info.keys()
        values = data.info.values()

        plt.style.use("default")
        plt.bar(names, values)
        plt.xlabel("Пункты наблюдения", fontdict={"size": 14})
        plt.ylabel("Мощность дозы (мкз/ч)", fontdict={"size": 14})
        plt.title(title, fontdict={"size": 20})
        plt.xticks(rotation=90)

        for keys, vals in data.info.items():
            container = plt.bar(keys, vals)
            plt.bar_label(container, label_type="edge", padding=3.0)

        plt.ylim(0, 1.0)
        plt.grid(True, axis="y")
        plt.savefig(self.dir_path / self.file_name, bbox_inches="tight")
        plt.close()

    def delete(self) -> None:
        """
        Method for deleting a png file with a chart.
        """
        if pathlib.Path(self.dir_path / self.file_name).exists():
            os.remove(self.dir_path / self.file_name)
