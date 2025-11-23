/* 
  HBnB Application JavaScript
  Handles authentication, API calls, and dynamic content loading
*/

// API Configuration
const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

// Utility Functions
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function setCookie(name, value, days = 7) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    const expires = `expires=${date.toUTCString()}`;
    document.cookie = `${name}=${value}; ${expires}; path=/`;
}

function deleteCookie(name) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
}

function checkAuthentication() {
    const token = getCookie('token');
    return token !== null;
}

function updateLoginButton() {
    const loginLink = document.getElementById('login-link');
    if (loginLink) {
        if (checkAuthentication()) {
            // Show logout button when user is authenticated
            loginLink.textContent = 'Logout';
            loginLink.href = '#';
            loginLink.onclick = (e) => {
                e.preventDefault();
                logout();
            };
        } else {
            // Show login link when user is not authenticated
            loginLink.textContent = 'Login';
            loginLink.href = '/login.html';
            loginLink.onclick = null;
        }
    }
}

function logout() {
    deleteCookie('token');
    window.location.href = '/';
}

// Login Functionality
async function loginUser(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            // Store JWT token in cookie
            setCookie('token', data.access_token);
            return { success: true, data };
        } else {
            return { 
                success: false, 
                error: data.error || 'Login failed. Please try again.' 
            };
        }
    } catch (error) {
        console.error('Login error:', error);
        return { 
            success: false, 
            error: 'Network error. Please check your connection and try again.' 
        };
    }
}

// Fetch Places from API
async function fetchPlaces(token) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        // Include token if available
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        const response = await fetch(`${API_BASE_URL}/places/`, { headers });
        if (response.ok) {
            const places = await response.json();
            return places;
        } else {
            console.error('Failed to fetch places');
            return [];
        }
    } catch (error) {
        console.error('Error fetching places:', error);
        return [];
    }
}

// Display Places as Cards
function displayPlaces(places) {
    const placesRow = document.getElementById('places-row');
    if (!placesRow) return;

    placesRow.innerHTML = '';

    if (places.length === 0) {
        placesRow.innerHTML = '<p style="text-align: center; color: #7f8c8d;">No places available at the moment.</p>';
        return;
    }

    places.forEach(place => {
        const card = document.createElement('div');
        card.className = 'place-card';
        card.setAttribute('data-price', place.price || 0);

        card.innerHTML = `
            <h3>${place.title || 'Unnamed Place'}</h3>
            <p class="price">$${place.price || 0} / night</p>
            <p>${place.description ? place.description.substring(0, 100) + '...' : 'No description available'}</p>
            <button class="details-button" onclick="viewPlaceDetails('${place.id}')">View Details</button>
        `;

        placesRow.appendChild(card);
    });
}

// Filter Places by Price
function filterPlacesByPrice(maxPrice) {
    const placeCards = document.querySelectorAll('.place-card');
    let visibleCount = 0;

    placeCards.forEach(card => {
        const price = parseFloat(card.getAttribute('data-price'));
        if (maxPrice === 'all' || price <= parseFloat(maxPrice)) {
            card.style.display = '';
            visibleCount++;
        } else {
            card.style.display = 'none';
        }
    });

    // Afficher le message si aucune place n'est visible
    const placesRow = document.getElementById('places-row');
    let noPlacesMsg = document.getElementById('no-places-msg');
    if (visibleCount === 0) {
        if (!noPlacesMsg) {
            noPlacesMsg = document.createElement('p');
            noPlacesMsg.id = 'no-places-msg';
            noPlacesMsg.style.textAlign = 'center';
            noPlacesMsg.style.color = '#7f8c8d';
            noPlacesMsg.textContent = 'No available places';
            placesRow.appendChild(noPlacesMsg);
        }
    } else {
        if (noPlacesMsg) {
            noPlacesMsg.remove();
        }
    }
}

// View Place Details
function viewPlaceDetails(placeId) {
    window.location.href = `/place.html?id=${placeId}`;
}

// Fetch Place Details
async function fetchPlaceDetails(placeId) {
    try {
        const response = await fetch(`${API_BASE_URL}/places/${placeId}`);
        if (response.ok) {
            const place = await response.json();
            return place;
        } else {
            console.error('Failed to fetch place details');
            return null;
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
        return null;
    }
}

// Display Place Details
function displayPlaceDetails(place) {
    const placeInfo = document.getElementById('place-info');
    if (!placeInfo || !place) return;

    const amenitiesList = place.amenities && place.amenities.length > 0
        ? `<ul>${place.amenities.map(a => `<li>${a.name || a}</li>`).join('')}</ul>`
        : '<p>No amenities listed</p>';

    placeInfo.innerHTML = `
        <h1>${place.title || 'Unnamed Place'}</h1>
        <p class="host">Host: ${place.owner ? place.owner.first_name + ' ' + place.owner.last_name : 'Unknown'}</p>
        <p class="price">$${place.price || 0} per night</p>
        <p class="description">${place.description || 'No description available'}</p>
        <div class="amenities">
            <h3>Amenities</h3>
            ${amenitiesList}
        </div>
    `;
}

// Fetch Reviews for a Place
async function fetchReviews(placeId) {
    try {
        const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`);
        if (response.ok) {
            const reviews = await response.json();
            return reviews;
        } else {
            console.error('Failed to fetch reviews');
            return [];
        }
    } catch (error) {
        console.error('Error fetching reviews:', error);
        return [];
    }
}

// Display Reviews
function displayReviews(reviews) {
    const reviewsList = document.getElementById('reviews-list');
    if (!reviewsList) return;

    reviewsList.innerHTML = '';

    if (reviews.length === 0) {
        reviewsList.innerHTML = '<p style="text-align: center; color: #7f8c8d;">No reviews yet. Be the first to review!</p>';
        return;
    }

    reviews.forEach(review => {
        const card = document.createElement('div');
        card.className = 'review-card';
        
        card.innerHTML = `
            <div class="review-header">
                <span class="reviewer-name">${review.user_name}</span>
                <span class="rating">★ ${review.rating || 'N/A'}/5</span>
            </div>
            <p class="comment">${review.comment || review.text || 'No comment provided'}</p>
        `;
        
        reviewsList.appendChild(card);
    });
}

// Submit Review
async function submitReview(placeId, reviewText, rating) {
    const token = getCookie('token');
    
    if (!token) {
        alert('You must be logged in to submit a review');
        window.location.href = '/login.html';
        return { success: false };
    }

    try {
        const response = await fetch(`${API_BASE_URL}/reviews/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                place_id: placeId,
                text: reviewText,
                rating: parseInt(rating)
            })
        });

        const data = await response.json();

        if (response.ok) {
            return { success: true, data };
        } else {
            return { 
                success: false, 
                error: data.error || 'Failed to submit review' 
            };
        }
    } catch (error) {
        console.error('Error submitting review:', error);
        return { 
            success: false, 
            error: 'Network error. Please try again.' 
        };
    }
}

// DOM Content Loaded Event
document.addEventListener('DOMContentLoaded', () => {
    // Update login button based on authentication status
    updateLoginButton();

    // Login Form Handler
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const errorElement = document.getElementById('login-error');
            
            // Clear previous error
            if (errorElement) {
                errorElement.style.display = 'none';
                errorElement.textContent = '';
            }

            // Disable submit button during request
            const submitButton = loginForm.querySelector('button[type="submit"]');
            submitButton.disabled = true;
            submitButton.textContent = 'Logging in...';

            // Attempt login
            const result = await loginUser(email, password);

            if (result.success) {
                // Redirect to index page
                window.location.href = '/';
            } else {
                // Display error message
                if (errorElement) {
                    errorElement.textContent = result.error;
                    errorElement.style.display = 'block';
                }
                
                // Re-enable submit button
                submitButton.disabled = false;
                submitButton.textContent = 'Login';
            }
        });
    }

    // Index Page - Load Places
    if (document.getElementById('places-list')) {
        const token = getCookie('token');
        
        // Fetch places with token if authenticated
        fetchPlaces(token).then(places => {
            displayPlaces(places);
        });
        
        // Price Filter Event Listener
        const priceFilter = document.getElementById('price-filter');
        if (priceFilter) {
            priceFilter.addEventListener('change', (event) => {
                const selectedPrice = event.target.value;
                filterPlacesByPrice(selectedPrice);
            });
        }
    }

    // Place Details Page
    if (document.getElementById('place-info')) {
        const urlParams = new URLSearchParams(window.location.search);
        const placeId = urlParams.get('id');
        
        if (placeId) {
            // Load place details
            fetchPlaceDetails(placeId).then(place => {
                if (place) {
                    displayPlaceDetails(place);
                } else {
                    document.getElementById('place-info').innerHTML = 
                        '<p style="color: red;">Place not found</p>';
                }
            });

            // Load reviews
            fetchReviews(placeId).then(reviews => {
                displayReviews(reviews);
            });

            // Show/hide review form and login button based on authentication
            const reviewForm = document.getElementById('review-form');
            const addReviewBtnContainer = document.getElementById('add-review-button-container');
            if (checkAuthentication()) {
                if (reviewForm) reviewForm.style.display = 'block';
                if (addReviewBtnContainer) addReviewBtnContainer.style.display = 'none';
            } else {
                if (reviewForm) reviewForm.style.display = 'none';
                if (addReviewBtnContainer) addReviewBtnContainer.style.display = 'block';
                const addReviewBtn = document.getElementById('add-review-btn');
                if (addReviewBtn) {
                    addReviewBtn.onclick = function() {
                        window.location.href = '/login.html';
                    };
                }
            }

            // Review form submission
            if (reviewForm) {
                reviewForm.addEventListener('submit', async (event) => {
                    event.preventDefault();
                    const reviewText = document.getElementById('review-text').value;
                    const rating = document.getElementById('rating').value;
                    const submitButton = reviewForm.querySelector('button[type="submit"]');
                    submitButton.disabled = true;
                    submitButton.textContent = 'Submitting...';
                    const result = await submitReview(placeId, reviewText, rating);
                    if (result.success) {
                        alert('Review submitted successfully!');
                        fetchReviews(placeId).then(reviews => {
                            displayReviews(reviews);
                        });
                        reviewForm.reset();
                    } else {
                        alert('Error: ' + result.error);
                    }
                    submitButton.disabled = false;
                    submitButton.textContent = 'Submit Review';
                });
            }
        }
    }

    // Add Review Page (separate page)
    const addReviewForm = document.getElementById('add-review-form');
    if (addReviewForm) {
        const urlParams = new URLSearchParams(window.location.search);
        const placeId = urlParams.get('place_id');
        
        if (!checkAuthentication()) {
            alert('You must be logged in to add a review');
            window.location.href = '/';
            return;
        }

        if (placeId) {
            // Load place name
            fetchPlaceDetails(placeId).then(place => {
                const placeNameElement = document.getElementById('place-name');
                if (placeNameElement && place) {
                    placeNameElement.textContent = `Review for: ${place.title}`;
                }
            });

            addReviewForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                
                const reviewText = document.getElementById('review-text').value;
                const rating = document.getElementById('rating').value;
                const messageElement = document.getElementById('review-message');
                
                const submitButton = addReviewForm.querySelector('button[type="submit"]');
                submitButton.disabled = true;
                submitButton.textContent = 'Submitting...';

                const result = await submitReview(placeId, reviewText, rating);

                if (result.success) {
                    if (messageElement) {
                        messageElement.textContent = 'Review submitted successfully!';
                        messageElement.style.color = 'green';
                        messageElement.style.display = 'block';
                    }
                    
                    // Redirect back to place details after 2 seconds
                    setTimeout(() => {
                        window.location.href = `/place.html?id=${placeId}`;
                    }, 2000);
                } else {
                    if (messageElement) {
                        messageElement.textContent = 'Error: ' + result.error;
                        messageElement.style.color = 'red';
                        messageElement.style.display = 'block';
                    }
                    
                    submitButton.disabled = false;
                    submitButton.textContent = 'Submit Review';
                }
            });
            } else {
            alert('No place selected');
            window.location.href = '/';
        }
    }
});