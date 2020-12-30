function uploadDataset() {
    let inputFile = document.getElementById("inputFile").files[0];
    let method = document.getElementsByName("method")[0].value
    let selectedMethod = (method[0].checked) ? "Burgess" : "Estimated";
    let formData = new FormData();

    formData.append("file", inputFile);
    formData.append('method', selectedMethod);
    fetch('/postDataset', {
        method: "POST", 
        body: formData
    })
    .then(result => {
        document.getElementById("mainContent").innerHTML = result;
        console.log('Success:\n', result);
    })
    .catch(error => {
        console.error('Oops! Sorry :(');
    });
}