from cpm import *

class EstimatedResourceSmoothing:

    def __init__(self, node_matrix=[]):
        self.node_matrix = node_matrix
        print('- Node_Matrix -\n', self.node_matrix)






def main():
    cpm = CPM()
    node_matrix = cpm.get_node_matrix()
    print(node_matrix)
    estimatedSmoothing = EstimatedResourceSmoothing(node_matrix)

if __name__ == "__main__":
    main()