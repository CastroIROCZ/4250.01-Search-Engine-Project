// Function to send the search query to the backend and receive a response
function performSearch(event) {
    event.preventDefault();  // Prevent form submission
    const query = document.getElementById('search-query').value.trim();
    if (!query) return;

    fetch("http://localhost:5000/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        updateResults(data.results);
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

// Function to update the results container with the results
function updateResults(results) {
    const resultsContainer = document.getElementById("results-container");
    resultsContainer.innerHTML = "";  // Clear previous results

    results.forEach(result => {
        const item = document.createElement("div");
        item.className = "result-item";

        const img = document.createElement("img");
        img.src = result.image_url;
        img.alt = "Faculty Image";
        //img.style.width = "100px";

        const name = document.createElement("div");
        name.textContent = result.name;

        const email = document.createElement("div");
        email.textContent = result.email;

        const phone = document.createElement("div");
        phone.textContent = result.phone;

        const link = document.createElement("a");
        link.href = result.url;
        link.textContent = "View Profile";
        link.target = "_blank";

        item.appendChild(img);
        item.appendChild(name);
        item.appendChild(email);
        item.appendChild(phone);
        item.appendChild(link);

        resultsContainer.appendChild(item);
    });
}

