#!/bin/python3

from argparse import ArgumentParser
from functools import reduce
import re

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

    def can_process_be_processed(self, process_id):
        for i in range(self.resources_qty):
            all_resources = self.available_resources[i] + self.allocated_resources[process_id][i]

            if all_resources < self.request_resources[process_id][i]:
                return False

        return True
    
    def print_has_deadlock(self):
        for i in self.resources_by_process:
            missing_resources = []
            
            for j in range(self.resources_qty):
                all_resources = self.available_resources[j] + self.allocated_resources[i["id"]][j]

                if all_resources < self.request_resources[i["id"]][j]:
                    missing_resources.append({
                        "id": j + 1,
                        "missing":  self.request_resources[i["id"]][j] - all_resources
                    })

            if missing_resources:
                program_exit = "O processo {0} est?? em deadlock".format(i["id"] + 1)
                
                for i in missing_resources:
                    program_exit += ", faltam {0} inst??ncias de R{1}".format(i["missing"], i["id"])
                
                print(program_exit)
                
    def has_deadlock(self):
        self.calc_resources_by_process()

        while self.resources_by_process:
            processed = False

            for i in self.resources_by_process:
                if self.can_process_be_processed(i["id"]):
                    for j in range(self.resources_qty):
                        self.available_resources[j] += self.allocated_resources[i["id"]][j]
                        
                    print(self.resources_by_process)
                    self.resources_by_process.remove(i)
                    processed = True
                    break

            if not processed:
                self.print_has_deadlock()
                return True
            
        print("Todos os processos foram finalizados.")
        return False

def main(filepath):
    file = MapFile(filepath)
    file.has_deadlock()

if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("filepath")
    
    args = parser.parse_args()

    main(args.filepath)
