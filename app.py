from cpm import *
from estimated_resource_smoothing import *
from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/postDataset/', methods=['POST'])
def post_dataset():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"



def main():
    cpm = CPM()
    input_file = 'input1.csv'
    cpm.get_data_from_input_file(input_file)
    
    cpm.calculate_start_node()
    cpm.forward_pass_of_the_network()
    
    cpm.find_descendants_of_node()
    cpm.backward_pass_of_the_network()
    
    cpm.calculate_slack_time_of_the_nodes()
    cpm.mark_critical_nodes_in_network()
    cpm.print_node_matrix()

    # ==== Estimated Method ===== #
    node_matrix = cpm.get_node_matrix()
    estimatedSmoothing = EstimatedResourceSmoothing(node_matrix)
    estimatedSmoothing.estimate_optimal_schedule()

if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    # app.run(threaded=True, port=5000)
    main()