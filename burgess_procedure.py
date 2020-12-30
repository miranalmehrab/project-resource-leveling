import itertools
import numpy as np

from cpm import *


class BurgessProcedure:

    def __init__(self, node_matrix=[]):
        self.node_matrix = node_matrix
        self.critical_activities = [] #List Or Array#
        self.critical_activities_length = 0
        self.nonCritical_activities = {}
        self.delay_activity_resluts = {} #Dictionary Or Map#
        self.project_duration = 0
        self.nonCritical_activities_length = 0
        self.optimal_time_resource_matrix = None
        self.R_by_time = []
        self.R2_by_time = []
        self.optimal_total_R = int(1e9)
        self.optimal_total_R_square = int(1e9)
        # print('- Node_Matrix -\n', self.node_matrix)
    


    def print_burgess_schedule_details(self):
        print("---------------------------------")
        print("Name\tOS\tOF\tShift \tR^2")
        for node in self.node_matrix:
            if node["critical"] == True:
                print(node["name"], "\t", node["OS"], "\t", node["OF"], "\t", int(node["OS"])-int(node["ES"]))
            else:
                print(node["name"], "\t", node["OS"], "\t", node["OF"], "\t", int(node["OS"])-int(node["ES"]),"\t",self.delay_activity_resluts[node["name"]])


    def initialize_OS_OF(self):
        for node in self.node_matrix:
            node["OS"] = node["ES"] 
            node["OF"] = node["EF"]


    def separate_critical_activities(self):
        for node in self.node_matrix:
            if node["critical"] == True:
                self.project_duration += int(node["duration"])
                self.critical_activities.append(node)


    def generate_time_resource_matrix(self):
        allotted_resources_for_cp = np.zeros(self.project_duration + 1, dtype=int)

        for ca in self.critical_activities:
            for ind, value in enumerate(allotted_resources_for_cp):
                if ind > int(ca["ES"]) and ind <= int(ca["EF"]):
                    allotted_resources_for_cp[ind] = value + int(ca["resource"])              
        # allotted_resources_for_cp.shape = (1, self.project_duration + 1)
    
        # flexible_resource_allocation_matrix = np.zeros((1, self.project_duration + 1), dtype=int)
        
        # time_resource_matrix = np.concatenate((allotted_resources_for_cp, flexible_resource_allocation_matrix))
        # print(time_resource_matrix)
        return allotted_resources_for_cp

    def calculate_total_resources(self, node, allotted_resources_for_cp):
        allotted_resources = np.copy(allotted_resources_for_cp)
        for a in self.node_matrix:
            if a["critical"] == False and a["name"] != node["name"]:
                for ind, value in enumerate(allotted_resources):
                    if ind > int(a["OS"]) and ind <= int(a["OF"]):
                        allotted_resources[ind] = value + int(a["resource"]) 
        return allotted_resources

    def burgess_scheduler(self, allotted_resources_for_cp):
        sorted_node_matrix = sorted(self.node_matrix, key = lambda i: int(i['ES']), reverse=True)
        while True:
            min_sum = int(1e9)
            for node in sorted_node_matrix:
                if node["critical"] == False:
                    # print("node", node, "\n")
                    des_os = int(1e9)
                    des_nodes = node["descendant"]
                    for desN in des_nodes:
                        des_node = list(filter(lambda key: key['name'] == desN, self.node_matrix))
                        # print(des_node, "\n")
                        if des_node[0]['OS'] < des_os:
                            des_os = des_node[0]['OS']
                            # print(des_os, "\n")

                    allotted_resources = self.calculate_total_resources(node, allotted_resources_for_cp)
                    # print(allotted_resources)
                    self.delay_activity_resluts[node["name"]] = int(1e9)
                    for i in range(1, node["slack"]+1):
                        if(int(node["EF"])+i > des_os):
                            break
                        temp_alloted_resource = np.copy(allotted_resources)
                        sum = 0
                        for ind, value in enumerate(temp_alloted_resource):
                            if ind > int(node["ES"])+i and ind <= int(node["EF"])+i:
                                temp_alloted_resource[ind] = value + int(node["resource"])

                        square_resources = [r*r for r in temp_alloted_resource]
                        sum = np.sum(square_resources)
                        # print("Hi", node['name'], i, "\n")
                        # print(self.delay_activity_resluts[node["name"]], sum, "\n")
                        if sum < self.delay_activity_resluts[node["name"]]:
                            self.delay_activity_resluts[node["name"]] = sum
                            node["OS"] = int(node["ES"]) + i        
                            node["OF"] = int(node["EF"]) + i
                    if self.delay_activity_resluts[node["name"]] < min_sum:
                        min_sum = self.delay_activity_resluts[node["name"]]

            print("Min sum", min_sum)
            self.print_burgess_schedule_details()
            if min_sum < self.optimal_total_R_square:
                self.optimal_total_R_square = min_sum
            else:
                break     


    def estimate_optimal_schedule(self):
        self.initialize_OS_OF()
        self.separate_critical_activities()
        allotted_resources_for_cp = self.generate_time_resource_matrix()
        self.burgess_scheduler(allotted_resources_for_cp)
        
