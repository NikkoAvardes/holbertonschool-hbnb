/**
 * Global Configuration and Helper Functions
 */

const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

/**
 * Helper function to retrieve the value of a cookie by name.
 * @param {string} name - The name of the cookie.
 * @returns {string | null} - The cookie value or null if not found.
 */
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

/**
 * Helper function to extract a query parameter from the URL.
 * @param {string} param - The name of the query parameter (e.g., 'place_id').
 * @returns {string | null} - The parameter value or null if not found.
 */
function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

/**
 * --- Task 1: Login Implementation (login.html) ---
 */
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const errorMessage = document.getElementById('error-message');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            errorMessage.style.display = 'none';

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch(`${API_BASE_URL}/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    // Store the JWT token in a cookie for session management
                    document.cookie = `token=${data.access_token}; path=/; max-age=${60 * 60 * 24}`; // Expires in 1 day
                    window.location.href = 'index.html'; // Redirect to the main page
                } else {
                    const errorData = await response.json();
                    errorMessage.textContent = `Login failed: ${errorData.message || response.statusText}`;
                    errorMessage.style.display = 'block';
                }
            } catch (error) {
                console.error('Login request failed:', error);
                errorMessage.textContent = 'An unexpected error occurred during login.';
                errorMessage.style.display = 'block';
            }
        });
    }
    // Check if on login.html and if already authenticated, redirect
    if (loginForm && getCookie('token')) {
        window.location.href = 'index.html';
    }
});

/**
 * --- Task 2: Index (List of Places) Implementation (index.html) ---
 */
let allPlaces = []; // Global store for places data to enable client-side filtering

/**
 * Checks authentication status and controls UI elements (login/logout links).
 * Fetches places if authenticated.
 * @returns {string | null} The JWT token or null.
 */
function checkAuthenticationIndex() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const logoutButton = document.getElementById('logout-button');

    if (loginLink && logoutButton) {
        if (!token) {
            loginLink.style.display = 'block';
            logoutButton.style.display = 'none';
        } else {
            loginLink.style.display = 'none';
            logoutButton.style.display = 'block';
            fetchPlaces(token); // Fetch data only if authenticated
        }
    }
    return token;
}

/**
 * Fetches places data from the API.
 * @param {string} token - The JWT token for authorization.
 */
async function fetchPlaces(token) {
    try {
        const response = await fetch(`${API_BASE_URL}/places`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            allPlaces = await response.json(); // Store data globally
            displayPlaces(allPlaces);
        } else if (response.status === 401 || response.status === 403) {
            // Unauthorized/Forbidden - possibly expired token
            alert('Session expired. Please log in again.');
            document.cookie = 'token=; path=/; max-age=0'; // Clear invalid token
            window.location.href = 'login.html';
        } else {
            console.error('Failed to fetch places:', response.statusText);
            document.getElementById('places-list').innerHTML = '<p>Error loading places.</p>';
        }
    } catch (error) {
        console.error('Network error fetching places:', error);
        document.getElementById('places-list').innerHTML = '<p>Network error. Cannot load places.</p>';
    }
}

/**
 * Dynamically renders the list of places.
 * @param {Array<Object>} places - The list of places to display.
 */
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = ''; // Clear previous content

    if (places.length === 0) {
        placesList.innerHTML = '<p>No places found.</p>';
        return;
    }

    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        // Store price for filtering
        placeCard.dataset.price = place.price_per_night; 

        placeCard.innerHTML = `
            <h3>${place.name}</h3>
            <p>Price per night: **$${place.price_per_night}**</p>
            <p>${place.description.substring(0, 100)}...</p>
            <button class="details-button" onclick="window.location.href='place.html?place_id=${place.id}'">View Details</button>
        `;
        placesList.appendChild(placeCard);
    });
}

/**
 * Handles client-side filtering of places based on max price.
 */
function handlePriceFilter() {
    const filterValue = document.getElementById('price-filter').value;
    const maxPrice = filterValue === 'all' ? Infinity : parseFloat(filterValue);
    const placeCards = document.querySelectorAll('.place-card');

    placeCards.forEach(card => {
        const price = parseFloat(card.dataset.price);
        if (price <= maxPrice || filterValue === 'all') {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Initial setup for index.html
if (document.getElementById('places-list')) {
    checkAuthenticationIndex();

    // Setup filter listener
    document.getElementById('price-filter').addEventListener('change', handlePriceFilter);

    // Setup logout listener
    document.getElementById('logout-button').addEventListener('click', () => {
        document.cookie = 'token=; path=/; max-age=0'; // Clear the cookie
        window.location.reload(); // Reload the page to show login link
    });
}

/**
 * --- Task 3: Place Details Implementation (place.html) ---
 */

/**
 * Fetches and displays details for a specific place, including reviews.
 * @param {string | null} token - The JWT token or null.
 * @param {string} placeId - The ID of the place.
 */
async function fetchPlaceDetails(token, placeId) {
    const placeDetailsSection = document.getElementById('place-details');
    const addReviewSection = document.getElementById('add-review-section'); // Assuming a dedicated section for the link/form

    if (!placeId) {
        placeDetailsSection.innerHTML = '<h2>Error: Place ID not found in URL.</h2>';
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
            method: 'GET',
            headers: token ? { 'Authorization': `Bearer ${token}` } : {} // Include token if present
        });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place, placeDetailsSection);

            // Conditional display of Add Review Link/Form
            if (token) {
                addReviewSection.innerHTML = `<a href="add_review.html?place_id=${placeId}" class="details-button">Add Review</a>`;
                addReviewSection.style.display = 'block';
            } else {
                addReviewSection.style.display = 'none';
            }

        } else {
            placeDetailsSection.innerHTML = `<h2>Error: Failed to load place (Status: ${response.status}).</h2>`;
        }
    } catch (error) {
        console.error('Network error fetching place details:', error);
        placeDetailsSection.innerHTML = '<h2>Network error. Cannot load place details.</h2>';
    }
}

/**
 * Renders the place details and reviews.
 */
function displayPlaceDetails(place, container) {
    container.innerHTML = `
        <div class="place-details">
            <h1>${place.name}</h1>
            <img src="${place.image_url || 'sample-image.jpg'}" alt="${place.name}" style="max-width: 100%;">
            
            <div class="place-info">
                <p><strong>Host:</strong> ${place.host_id || 'Unknown Host'}</p>
                <p><strong>Price per Night:</strong> $${place.price_per_night}</p>
                <p><strong>Max Guests:</strong> ${place.max_guests}</p>
                <p><strong>Description:</strong> ${place.description}</p>
                </div>
            
            <div id="reviews-list">
                <h2>Reviews (${place.reviews ? place.reviews.length : 0})</h2>
                ${place.reviews && place.reviews.length > 0 ? place.reviews.map(review => `
                    <div class="review-card">
                        <p><strong>User:</strong> ${review.user_id || 'Anonymous'}</p>
                        <p><strong>Rating:</strong> ${review.rating} / 5</p>
                        <p>Comment: ${review.text}</p>
                    </div>
                `).join('') : '<p>No reviews yet.</p>'}
            </div>
        </div>
    `;
}

// Initial setup for place.html
if (document.getElementById('place-details')) {
    const placeId = getQueryParam('place_id');
    const token = getCookie('token');
    fetchPlaceDetails(token, placeId);
}


/**
 * --- Task 4: Add Review Form Implementation (add_review.html) ---
 */

/**
 * Checks authentication for the add_review page and sets up the form.
 * @returns {string | null} The JWT token or null.
 */
function checkAuthenticationReviewPage() {
    const token = getCookie('token');
    if (!token) {
        // Redirect to index page if not authenticated
        window.location.href = 'index.html'; 
    }
    return token;
}

// Initial setup for add_review.html
document.addEventListener('DOMContentLoaded', () => {
    const reviewForm = document.getElementById('review-form');
    
    if (reviewForm) {
        const token = checkAuthenticationReviewPage();
        const placeId = getQueryParam('place_id');
        
        // Display the place ID in the form title for context
        const formTitle = document.getElementById('review-form-title');
        if (formTitle && placeId) {
             formTitle.textContent = `Add Review for Place ID: ${placeId}`;
        }

        if (token && placeId) {
            reviewForm.addEventListener('submit', async (event) => {
                event.preventDefault();

                const reviewText = document.getElementById('review-text').value;
                const rating = document.getElementById('rating').value;

                await submitReview(token, placeId, reviewText, rating);
            });
        }
    }
});

/**
 * Submits the review data to the API.
 */
async function submitReview(token, placeId, reviewText, rating) {
    const submitStatus = document.getElementById('submit-status'); // Assuming an element for status messages
    submitStatus.textContent = ''; // Clear previous status

    try {
        const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ text: reviewText, rating: parseInt(rating), place_id: placeId })
        });

        if (response.ok) {
            alert('Review submitted successfully!');
            document.getElementById('review-form').reset(); // Clear the form
            // Optionally redirect back to the place details page
            window.location.href = `place.html?place_id=${placeId}`;
        } else if (response.status === 401 || response.status === 403) {
             alert('Session expired. Please log in again.');
             document.cookie = 'token=; path=/; max-age=0'; // Clear invalid token
             window.location.href = 'login.html';
        } else {
            const errorData = await response.json();
            alert(`Failed to submit review: ${errorData.message || response.statusText}`);
        }
    } catch (error) {
        console.error('Network error submitting review:', error);
        alert('An unexpected error occurred. Please try again.');
    }
}