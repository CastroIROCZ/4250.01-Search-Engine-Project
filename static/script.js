// Function to send the search query to the backend and receive a response
function performSearch(event) {
    // Prevent form submission
    event.preventDefault();

    // Get the search query value
    const query = document.getElementById('search-query').value.trim();

    // Check if there's a query input
    if (!query) return;

    // Prepare the search query
    const requestData = { query: query };

    // Make a request to the backend API
    fetch("http://localhost:5000/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        // Display the dummy response data in the console
        console.log("Received response:", data);

        // Update the results container with the received dummy data
        updateResults(data.results);
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

// Function to update the results container with dummy data for now to test functionality 
function updateResults(results) {
    const resultsContainer = document.getElementById("results-container");
    resultsContainer.innerHTML = ""; // Clear previous results

    // Display each result from the received data
    results.forEach(result => {
        const item = document.createElement("a");
        item.className = "result-item";
        item.href = result.link; // The URL of the result
        item.target = "_blank";
        item.innerText = result.name; // Display name

        resultsContainer.appendChild(item);
    });
}
