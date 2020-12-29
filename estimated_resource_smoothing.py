import itertools
import numpy as np

from cpm import *


class EstimatedResourceSmoothing:

    def __init__(self, node_matrix=[]):
        self.node_matrix = node_matrix
        print('- Node_Matrix -\n', self.node_matrix)
        self.critical_activities = []
        self.critical_activities_length = 0
        self.nonCritical_activities = {}
        self.project_duration = 0
        self.nonCritical_activities_length = 0
        self.R_by_time = []
        self.R2_by_time = []
    

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

        self.nonCritical_activities_length = len(self.node_matrix) - len(self.critical_activities)
        flexible_resource_allocation_matrix = np.zeros((self.nonCritical_activities_length, self.project_duration + 1), dtype=int)

        time_resource_matrix = np.concatenate((allotted_resources_for_cp, flexible_resource_allocation_matrix))
        print(time_resource_matrix)
        return time_resource_matrix



    def find_optimal_schedule_and_update_activity_values(self, time_resource_matrix):
        combinations = []
        activity_id_mapping = {}
        for node in self.node_matrix:
            if node["critical"] == False:
                schedule_options_for_this_node = np.arange(int(node["slack"]) + 1)
                activity_id_mapping[len(combinations)] = node["id"]
                combinations.append(schedule_options_for_this_node)
        print(combinations)
        combinations = list(itertools.product(*combinations))
        # print(combinations)



    def estimate_optimal_schedule(self):
        self.separate_critical_activities()
        time_resource_matrix = self.generate_time_resource_matrix()
        self.find_optimal_schedule_and_update_activity_values(time_resource_matrix)







def main():
    cpm = CPM()
    node_matrix = cpm.get_node_matrix()
    print(node_matrix)
    estimatedSmoothing = EstimatedResourceSmoothing(node_matrix)

if __name__ == "__main__":
    main()