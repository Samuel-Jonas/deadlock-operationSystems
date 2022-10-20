#!/bin/python3
from argparse import ArgumentParser

class MapFile:
    def __init__(self, filepath):
        with open(filepath) as file:
            line = file.readline().replace("\n", "")
            [self.process_qty, self.resources_qty] = line.split(" ")

            file.readline()

            line = file.readline().replace("\n", "")
            self.total_resources = line.split(" ")

            file.readline()

            line = file.readline().replace("\n", "")
            self.available_resources = line.split(" ")

            file.readline()

            self.allocated_resources = []

            for i in range(int(self.process_qty)):
                line = file.readline().replace("\n", "")
                self.allocated_resources += [line.split(" ")]

            file.readline()

            self.request_resources = []

            for i in range(int(self.process_qty)):
                line = file.readline().replace("\n", "")
                self.request_resources += [line.split(" ")]

if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument("filepath")
    
    args = parser.parse_args()

    print(MapFile(args.filepath).__dict__)

