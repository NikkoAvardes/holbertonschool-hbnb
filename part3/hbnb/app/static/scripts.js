// Configuration de l'API
const API_BASE_URL = '/api/v1';

// Fonction utilitaire pour obtenir la valeur d'un cookie
function getCookie(name) {
	const value = `; ${document.cookie}`;
	const parts = value.split(`; ${name}=`);
	if (parts.length === 2) return parts.pop().split(';').shift();
	return null;
}

// Fonction utilitaire pour supprimer un cookie
function deleteCookie(name) {
	document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
}

// Fonction pour obtenir l'ID de la place depuis l'URL
function getPlaceIdFromURL() {
	const urlParams = new URLSearchParams(window.location.search);
	return urlParams.get('place_id');
}

document.addEventListener('DOMContentLoaded', () => {
	const loginForm = document.getElementById('login-form');
	const reviewForm = document.getElementById('review-form');

	// Vérification de la page actuelle
	const currentPage = window.location.pathname.split('/').pop();

	if (loginForm) {
		// Page de login
		loginForm.addEventListener('submit', async (event) => {
			event.preventDefault();
			const email = document.getElementById('email').value;
			const password = document.getElementById('password').value;
			await loginUser(email, password);
		});
	} else if (currentPage === 'index.html' || currentPage === '') {
		// Page d'accueil
		checkAuthentication();

		// Ajouter event listener pour le filtre de prix
		const priceFilter = document.getElementById('price-filter');
		if (priceFilter) {
			priceFilter.addEventListener('change', (event) => {
				filterPlacesByPrice(event.target.value);
			});
		}
	} else if (currentPage === 'place.html') {
		// Page de détails de la place
		const token = getCookie('token');
		const placeId = getPlaceIdFromURL();

		checkAuthenticationForPlace();

		if (placeId) {
			fetchPlaceDetails(token, placeId);
		}
	} else if (currentPage === 'add_review.html') {
		// Page d'ajout de review
		const token = checkAuthentication();
		const placeId = getPlaceIdFromURL();

		if (!token) {
			window.location.href = 'index.html';
			return;
		}

		if (reviewForm && placeId) {
			reviewForm.addEventListener('submit', async (event) => {
				event.preventDefault();
				const reviewText = document.getElementById('review').value;
				const rating = document.getElementById('rating').value;
				await submitReview(token, placeId, reviewText, rating);
			});
		}
	}
});

// Fonctions pour la page de login
async function loginUser(email, password) {
	console.log('Tentative de connexion pour:', email);
	console.log('URL API:', `${API_BASE_URL}/auth/login`);

	try {
		// Vérification de la disponibilité du serveur
		console.log('Vérification de la disponibilité du serveur...');
		const healthCheck = await fetch('/api/');
		console.log('Réponse health check:', healthCheck.status);

		const response = await fetch(`${API_BASE_URL}/auth/login`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ email, password })
		});

		console.log('Statut de la réponse:', response.status);
		console.log('Réponse OK:', response.ok);

		if (response.ok) {
			const data = await response.json();
			document.cookie = `token=${data.access_token}; path=/`;
			window.location.href = 'index.html';
		} else {
			const errorData = await response.json().catch(() => ({}));
			console.error('Réponse d\'erreur de login:', errorData);
			alert('Login failed: ' + (errorData.error || response.statusText));
		}
	} catch (error) {
		console.error('Erreur de fetch:', error);
		alert('Erreur de connexion. Vérifiez que le serveur est démarré.');
	}
}

// Fonctions pour la page d'accueil
function checkAuthentication() {
	const token = getCookie('token');
	const loginLink = document.getElementById('login-link');

	if (!token) {
		if (loginLink) loginLink.style.display = 'block';
	} else {
		if (loginLink) loginLink.style.display = 'none';
		fetchPlaces(token);
	}

	return token;
}

async function fetchPlaces(token) {
	try {
		const headers = {
			'Content-Type': 'application/json'
		};

		if (token) {
			headers['Authorization'] = `Bearer ${token}`;
		}

		const response = await fetch(`${API_BASE_URL}/places`, {
			method: 'GET',
			headers: headers
		});

		if (response.ok) {
			const places = await response.json();
			displayPlaces(places);
		} else {
			console.error('Failed to fetch places');
		}
	} catch (error) {
		console.error('Error fetching places:', error);
	}
}

function displayPlaces(places) {
	const placesList = document.getElementById('places-list');
	if (!placesList) return;

	placesList.innerHTML = '';

	places.forEach(place => {
		const placeDiv = document.createElement('div');
		placeDiv.className = 'place-card';
		placeDiv.setAttribute('data-price', place.price);

		placeDiv.innerHTML = `
            <h3>${place.title}</h3>
            <p><strong>Price:</strong> $${place.price} per night</p>
            <p><strong>Location:</strong> ${place.city || ''}, ${place.country || ''}</p>
            <p>${place.description || ''}</p>
            <a href="place.html?place_id=${place.id}" class="details-button">View Details</a>
        `;

		placesList.appendChild(placeDiv);
	});
}

function filterPlacesByPrice(selectedPrice) {
	const places = document.querySelectorAll('.place-card');

	places.forEach(place => {
		const placePrice = parseFloat(place.getAttribute('data-price'));

		if (selectedPrice === 'all' || placePrice <= parseFloat(selectedPrice)) {
			place.style.display = 'block';
		} else {
			place.style.display = 'none';
		}
	});
}

// Fonctions pour la page de détails de place
function checkAuthenticationForPlace() {
	const token = getCookie('token');
	const addReviewSection = document.getElementById('add-review');

	if (!token) {
		if (addReviewSection) addReviewSection.style.display = 'none';
	} else {
		if (addReviewSection) addReviewSection.style.display = 'block';
	}

	return token;
}

async function fetchPlaceDetails(token, placeId) {
	try {
		const headers = {
			'Content-Type': 'application/json'
		};

		if (token) {
			headers['Authorization'] = `Bearer ${token}`;
		}

		const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
			method: 'GET',
			headers: headers
		});

		if (response.ok) {
			const place = await response.json();
			displayPlaceDetails(place);
		} else {
			console.error('Failed to fetch place details');
		}
	} catch (error) {
		console.error('Error fetching place details:', error);
	}
}

function displayPlaceDetails(place) {
	// Titre de la place
	const placeTitle = document.getElementById('place-title');
	if (placeTitle) {
		placeTitle.textContent = place.title;
	}

	// Détails de la place
	const placeDetails = document.getElementById('place-details');
	if (!placeDetails) return;

	placeDetails.innerHTML = `
        <div class="place-info">
            <h3>Description</h3>
            <p>${place.description || 'No description available'}</p>
            <p><strong>Price:</strong> $${place.price} per night</p>
            <p><strong>Location:</strong> ${place.city || ''}, ${place.country || ''}</p>
            <div class="amenities">
                <h4>Amenities:</h4>
                <ul>
                    ${place.amenities ? place.amenities.map(amenity => `<li>${amenity.name}</li>`).join('') : '<li>No amenities listed</li>'}
                </ul>
            </div>
        </div>
    `;

	// Afficher les reviews
	const reviewsList = document.getElementById('reviews-list');
	if (reviewsList && place.reviews) {
		reviewsList.innerHTML = '';

		if (place.reviews.length > 0) {
			place.reviews.forEach(review => {
				const reviewDiv = document.createElement('div');
				reviewDiv.className = 'review';
				reviewDiv.innerHTML = `
                    <p><strong>Rating:</strong> ${review.rating}/5</p>
                    <p>${review.text}</p>
                    <p><em>By: ${review.user_id}</em></p>
                `;
				reviewsList.appendChild(reviewDiv);
			});
		} else {
			reviewsList.innerHTML = '<p>No reviews yet.</p>';
		}
	}
}

// Fonctions pour l'ajout de reviews
async function submitReview(token, placeId, reviewText, rating) {
	try {
		const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${token}`
			},
			body: JSON.stringify({
				text: reviewText,
				rating: parseInt(rating)
			})
		});

		if (response.ok) {
			alert('Review submitted successfully!');
			document.getElementById('review-form').reset();
		} else {
			alert('Failed to submit review');
		}
	} catch (error) {
		alert('Failed to submit review: ' + error.message);
	}
}