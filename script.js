// Function to send the search query to the backend and process results
function performSearch(event) {
    // Prevent form submission
    event.preventDefault();

    // Get the search query
    const query = document.getElementById("search-query").value.trim();
    if (!query) return;

    // Placeholder URL, replace with the actual endpoint once ready
    const apiUrl = "http://localhost:5000/search";

    // Prepare the request payload
    const requestData = { query: query };

    // Make a request to the backend API
    fetch(apiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response data (list of faculty links) and update the results
        updateResults(data.results);
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

// Function to update results in the results container
function updateResults(results) {
    const resultsContainer = document.getElementById("results-container");
    resultsContainer.innerHTML = ""; // Clear previous results

    // Display a message if no results were found
    if (results.length === 0) {
        resultsContainer.innerHTML = '<p>No results found.</p>';
        return;
    }

    // Populate the results container with the new results
    results.forEach(result => {
        const item = document.createElement("a");
        item.className = "result-item";
        item.href = result.link; // URL of the professor's page
        item.target = "_blank";
        item.innerText = result.name; // Professor's name

        resultsContainer.appendChild(item);
    });
}


