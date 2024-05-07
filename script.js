function fetchResults() {
    // Get the search query from the search bar
    const query = document.getElementById('search-bar').value.trim();

    // Mock response data (you'll replace this with real backend results)
    const results = [
        {
            title: "Dr. John Doe - Computer Science",
            description: "Specializes in artificial intelligence and data science."
        },
        {
            title: "Dr. Jane Smith - Mathematics",
            description: "Focuses on differential equations and complex analysis."
        },
        {
            title: "Prof. Emily Clark - Physics",
            description: "Researches quantum mechanics and condensed matter physics."
        },
        {
            title: "Dr. Michael Johnson - Biology",
            description: "Expert in evolutionary biology and genetics."
        }
    ];

    // Simulating a filtered search by filtering the mock data
    const filteredResults = results.filter(item => item.title.toLowerCase().includes(query.toLowerCase()));

    // Update the results section with filtered data
    updateResults(filteredResults);
}

function updateResults(results) {
    // Get the container to display results
    const resultsContainer = document.getElementById('results-container');
    resultsContainer.innerHTML = ''; // Clear previous results

    if (results.length === 0) {
        resultsContainer.innerHTML = '<p>No results found.</p>';
    } else {
        results.forEach(result => {
            const item = document.createElement('div');
            item.className = 'result-item';

            const title = document.createElement('h3');
            title.textContent = result.title;

            const description = document.createElement('p');
            description.textContent = result.description;

            item.appendChild(title);
            item.appendChild(description);

            resultsContainer.appendChild(item);
        });
    }
}

