function uploadDataset() {
    // let inputFile = document.getElementById("inputFile").files[0];
    let inputFile = document.querySelector('input[type="file"]').files[0];
    let method = document.getElementsByName("method")[0].value;
    let selectedMethod = (method[0].checked) ? "Burgess" : "Estimated";
    let formData = new FormData();

    formData.append("file", inputFile);
    formData.append('method', selectedMethod);
    console.log(inputFile, selectedMethod);
    fetch('/postDataset/', {
        method: "POST", 
        body: formData,
    })
    .then(response => {
        return response.json();
      })
    .then(result => {
        console.log('Success:\n', result);
        document.getElementById("mainContent").innerHTML = "Optimal R-square = " + result["optimal_total_R_square"];
    })
    .catch(error => {
        console.error('Oops! Sorry :(');
    });
}