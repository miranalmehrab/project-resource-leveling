import itertools
import numpy as np

from cpm import *


class EstimatedResourceSmoothing:

    def __init__(self, node_matrix=[]):
        self.node_matrix = node_matrix
        # print('- Node_Matrix -\n', self.node_matrix)
        self.critical_activities = []
        self.critical_activities_length = 0
        self.nonCritical_activities = {}
        self.project_duration = 0
        self.nonCritical_activities_length = 0
        self.R_by_time = []
        self.R2_by_time = []
        self.optimal_total_R = int(1e9)
        self.optimal_total_R_square = int(1e9)
    

    def print_estimate_schedule_details(self):
        print("Total R: ", self.optimal_total_R)
        print(self.R_by_time)
        print("Total R-square: ", self.optimal_total_R_square)
        print(self.R2_by_time)
        print("Name\tOS\tOF\tSlack")
        for node in self.node_matrix:
            if node["critical"] == True:
                print(node["name"], "\t\t", node["ES"], "\t", node["EF"], "\t", node["slack"])
            else:
                print(node["name"], "\t\t", node["OS"], "\t", node["OF"], "\t", node["slack"])


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
        allotted_resources_for_cp.shape = (1, self.project_duration + 1)
        # print(allotted_resources_for_cp)

        # self.nonCritical_activities_length = len(self.node_matrix) - len(self.critical_activities)
        # flexible_resource_allocation_matrix = np.zeros((self.nonCritical_activities_length, self.project_duration + 1), dtype=int)
        flexible_resource_allocation_matrix = np.zeros((1, self.project_duration + 1), dtype=int)

        time_resource_matrix = np.concatenate((allotted_resources_for_cp, flexible_resource_allocation_matrix))
        # print(time_resource_matrix)
        # time_resource_matrix[1] = np.arange(self.project_duration + 1)
        # print(time_resource_matrix)
        # time_resource_matrix[1] = np.zeros(self.project_duration + 1)
        print(time_resource_matrix)
        return time_resource_matrix


    def update_optimal_start_and_finish_time(self, comb_choice, pos_in_combination_and_node_matrix_ind_mapping):
        for i, shift in enumerate(comb_choice):
            node_matrix_index = pos_in_combination_and_node_matrix_ind_mapping[i]
            es, duration = int(self.node_matrix[node_matrix_index]["ES"]), int(self.node_matrix[node_matrix_index]["duration"])
            self.node_matrix[node_matrix_index]["OS"] = es + int(shift) 
            self.node_matrix[node_matrix_index]["OF"] = es + int(shift) + duration


    def check_for_optimality(self, time_resource_matrix, comb_choice, pos_in_combination_and_node_matrix_ind_mapping):
        self.R_by_time = np.sum(time_resource_matrix, 0)
        self.R2_by_time = [ r*r for r in self.R_by_time ]
        if np.sum(self.R2_by_time) < self.optimal_total_R_square:
            self.optimal_total_R_square = np.sum(self.R2_by_time)
            self.optimal_total_R = np.sum(self.R_by_time)
            self.update_optimal_start_and_finish_time(comb_choice, pos_in_combination_and_node_matrix_ind_mapping)


    def find_optimal_schedule_and_update_activity_values(self, time_resource_matrix):
        combinations = []
        pos_in_combination_and_node_matrix_ind_mapping = {}
        for index,node in enumerate(self.node_matrix):
            if node["critical"] == False:
                schedule_options_for_this_node = np.arange(int(node["slack"]) + 1)
                pos_in_combination_and_node_matrix_ind_mapping[len(combinations)] = index
                combinations.append(schedule_options_for_this_node)
        print(combinations)
        combinations = list(itertools.product(*combinations))

        # First Choice --> BAD #
        # for choice in combinations:
        #     for i, shift in enumerate(choice):
        #         node = pos_in_combination_and_node_matrix_ind_mapping[i]
        #         # print(node)
        #         es, duration, lf = int(node["ES"]), int(node["duration"]), int(node["LF"])
        #         # print("es=", es," dur=", duration," lf=", lf)
        #         for index in range(es+1, lf+1):
        #             if (index > es and index <= es + int(shift)) or (index > es + int(shift) + duration and index <= lf):
        #                 time_resource_matrix[i+1][index] = 0
        #             elif index > es + int(shift) and index <= es + int(shift) + duration:
        #                 time_resource_matrix[i+1][index] = int(node["resource"])
        #             # elif index > es + shift + duration and index <= lf:
        #             #     time_resource_matrix[i+1][index] = 0
        
        # 2nd Choice --> LET'S SEE #
        for comb_choice in combinations:
            for i, shift in enumerate(comb_choice):
                node = self.node_matrix[ pos_in_combination_and_node_matrix_ind_mapping[i] ]
                es, duration, lf = int(node["ES"]), int(node["duration"]), int(node["LF"])
                for index in range(es+1, lf+1):
                    if index > es + int(shift) and index <= es + int(shift) + duration:
                        time_resource_matrix[1][index] += int(node["resource"])
                self.check_for_optimality(time_resource_matrix, comb_choice, pos_in_combination_and_node_matrix_ind_mapping)
                time_resource_matrix[1] = np.zeros(self.project_duration + 1, dtype=int)



    def estimate_optimal_schedule(self):
        self.separate_critical_activities()
        time_resource_matrix = self.generate_time_resource_matrix()
        self.find_optimal_schedule_and_update_activity_values(time_resource_matrix)
        self.print_estimate_schedule_details()
        







def main():
    cpm = CPM()
    node_matrix = cpm.get_node_matrix()
    # print(node_matrix)
    estimatedSmoothing = EstimatedResourceSmoothing(node_matrix)

if __name__ == "__main__":
    main()