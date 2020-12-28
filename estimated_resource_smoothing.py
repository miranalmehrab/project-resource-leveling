from cpm import *
import numpy as np


class EstimatedResourceSmoothing:

    def __init__(self, node_matrix=[]):
        self.node_matrix = node_matrix
        print('- Node_Matrix -\n', self.node_matrix)
        self.critical_activities = []
        self.nonCritical_activities = {}
        self.project_duration = 0
        self.nonCritical_activities_length = 0
        self.R_by_time = []
        self.R2_by_time = []
    

    def estimate_optimal_schedule(self):
        for node in node_matrix:
            if node["critical"] == True:
                self.project_duration += node["duration"]
                self.critical_activities.append(node)
                
        allotted_resources_for_cp = np.zeros((self.critical_activities.__len__, self.project_duration + 1), dtype=int)
        for ca in self.critical_activities:
            np.put(allotted_resources_for_cp, [ca["ES"], ca["EF"]], [ca["resource"]])
        allotted_resources_for_cp = np.sum(allotted_resources_for_cp, axis = 0)

        self.nonCritical_activities_length = self.node_matrix.__len__ - self.critical_activities.__len__
        flexible_resource_allocation_matrix = np.zeros((self.nonCritical_activities_length, self.project_duration + 1), dtype=int)
        time_resource_matrix = np.concatenate((allotted_resources_for_cp, flexible_resource_allocation_matrix))






def main():
    cpm = CPM()
    node_matrix = cpm.get_node_matrix()
    print(node_matrix)
    estimatedSmoothing = EstimatedResourceSmoothing(node_matrix)

if __name__ == "__main__":
    main()