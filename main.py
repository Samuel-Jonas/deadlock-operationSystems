#!/bin/python3

from argparse import ArgumentParser
from functools import reduce

class MapFile:
    def __init__(self, filepath):
        with open(filepath) as file:
            line = file.readline().replace("\n", "")
            [self.process_qty, self.resources_qty] = [int(i) for i in line.split(" ") if i.isdecimal()]

            file.readline()

            line = file.readline().replace("\n", "")
            self.total_resources = [int(i) for i in line.split(" ") if i.isdecimal()]

            file.readline()

            line = file.readline().replace("\n", "")
            self.available_resources = [int(i) for i in line.split(" ") if i.isdecimal()]

            file.readline()

            self.allocated_resources = []

            for i in range(int(self.process_qty)):
                line = file.readline().replace("\n", "")
                self.allocated_resources += [[int(r) for r in line.split(" ") if r.isdecimal()]]

            file.readline()

            self.request_resources = []

            for i in range(int(self.process_qty)):
                line = file.readline().replace("\n", "")
                self.request_resources += [[int(r) for r in line.split(" ") if r.isdecimal()]]

    def calc_resources_by_process(self):
        self.resources_by_process = []

        for i in range(self.process_qty):
            total_resources = reduce(lambda acc, r: acc + r, self.request_resources[i])

            self.resources_by_process.append({
                "id": i,
                "total": total_resources
            })

        self.resources_by_process = sorted(self.resources_by_process, key=lambda r: r["total"], reverse=True)

def main(filepath):
    file = MapFile(filepath)
    file.calc_resources_by_process()

    print(file.__dict__)

def can_process_be_processed(file, process_id):
    for i in range(file.resources_qty):
        all_resources = file.available_resources[i] + file.allocated_resources[process_id][i]

        if all_resources < file.request_resources[process_id][i]:
            return False

    return True

if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument("filepath")
    
    args = parser.parse_args()

    main(args.filepath)
