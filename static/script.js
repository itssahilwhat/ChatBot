function fetchBusiness() {
    let language = document.getElementById("language").value;
    let query = document.getElementById("query").value;

    fetch('/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ language: language, query: query })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerHTML = `<strong>Result:</strong> ${data.result}`;
    })
    .catch(error => console.error('Error:', error));
}
