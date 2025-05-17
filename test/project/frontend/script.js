document.getElementById('searchForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const username = document.getElementById('usernameInput').value;
  const resultsList = document.getElementById('resultsList');
  resultsList.innerHTML = ''; // Clear previous results

  console.log(`Searching for username: ${username}`); // Debug: Log username

  try {
    // Show a loading message while waiting for the response
    resultsList.innerHTML = `<li>Searching for username: ${username}...</li>`;

    const response = await fetch(`http://127.0.0.1:5000/search?username=${username}`);
    console.log(`Response status: ${response.status}`); // Debug: Log response status

    if (!response.ok) {
      const errorData = await response.json();
      resultsList.innerHTML = `<li>${errorData.error}</li>`;
      return;
    }

    const data = await response.json();
    console.log(`Response data:`, data); // Debug: Log response data

    if (!data.results || data.results.length === 0) {
      resultsList.innerHTML = `<li>No results found for username: ${username}</li>`;
    } else {
      resultsList.innerHTML = ''; // Clear the loading message
      data.results.forEach(result => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `<a href="${result.url_user}" target="_blank">${result.url_user}</a> - ${result.status}`;
        resultsList.appendChild(listItem);
      });
    }
  } catch (error) {
    resultsList.innerHTML = `<li>Error fetching results. Please try again later.</li>`;
    console.error('Error:', error); // Debug: Log errors
  }
});