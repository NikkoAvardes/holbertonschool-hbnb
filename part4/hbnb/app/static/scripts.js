/* Application JavaScript HBnB
  Gère l'authentification, les appels API et le chargement de contenu dynamique
*/

// =========================================================================
// CONFIGURATION API
// =========================================================================

const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

// =========================================================================
// FONCTIONS UTILITAIRES POUR LES COOKIES ET L'AUTHENTIFICATION
// =========================================================================

/**
 * Récupère la valeur d'un cookie par son nom.
 * @param {string} name - Le nom du cookie.
 * @returns {string|null} La valeur du cookie ou null s'il n'est pas trouvé.
 */
function getCookie(name) {
	const value = `; ${document.cookie}`;
	const parts = value.split(`; ${name}=`);
	if (parts.length === 2) return parts.pop().split(';').shift();
	return null;
}

/**
 * Définit un cookie avec un nom, une valeur et une durée (en jours).
 * @param {string} name - Le nom du cookie.
 * @param {string} value - La valeur à stocker.
 * @param {number} [days=7] - Nombre de jours avant l'expiration.
 */
function setCookie(name, value, days = 7) {
	const date = new Date();
	date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
	const expires = `expires=${date.toUTCString()}`;
	document.cookie = `${name}=${value}; ${expires}; path=/`;
}

/**
 * Supprime un cookie en le faisant expirer immédiatement.
 * @param {string} name - Le nom du cookie à supprimer.
 */
function deleteCookie(name) {
	document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
}

/**
 * Vérifie si l'utilisateur est authentifié (présence d'un token).
 * @returns {boolean} Vrai si un token est trouvé, faux sinon.
 */
function checkAuthentication() {
	const token = getCookie('token');
	return token !== null;
}

/**
 * Met à jour le bouton de connexion/déconnexion dans l'en-tête.
 */
function updateLoginButton() {
	const loginLink = document.getElementById('login-link');
	if (loginLink) {
		if (checkAuthentication()) {
			// Afficher Déconnexion
			loginLink.textContent = 'Logout';
			loginLink.href = '#';
			loginLink.onclick = (e) => {
				e.preventDefault();
				logout();
			};
		} else {
			// Afficher Connexion
			loginLink.textContent = 'Login';
			loginLink.href = '/login.html';
			loginLink.onclick = null;
		}
	}
}

/**
 * Déconnecte l'utilisateur en supprimant le token et en redirigeant.
 */
function logout() {
	deleteCookie('token');
	window.location.href = '/';
}

// =========================================================================
// FONCTIONNALITÉS D'AUTHENTIFICATION (LOGIN)
// =========================================================================

/**
 * Tente de connecter un utilisateur via l'API.
 * @param {string} email - L'email de l'utilisateur.
 * @param {string} password - Le mot de passe de l'utilisateur.
 * @returns {Promise<{success: boolean, data?: any, error?: string}>} Le résultat de la connexion.
 */
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
			// Stocke le token JWT dans un cookie
			setCookie('token', data.access_token);
			return { success: true, data };
		} else {
			return {
				success: false,
				error: data.error || 'Échec de la connexion. Veuillez réessayer.'
			};
		}
	} catch (error) {
		console.error('Erreur de connexion:', error);
		return {
			success: false,
			error: 'Erreur réseau. Veuillez vérifier votre connexion et réessayer.'
		};
	}
}

// =========================================================================
// GESTION DES LIEUX (PLACES)
// =========================================================================

/**
 * Récupère la liste des lieux depuis l'API.
 * @param {string} [token] - Le token d'authentification Bearer optionnel.
 * @returns {Promise<Array<Object>>} La liste des lieux.
 */
async function fetchPlaces(token) {
	try {
		const headers = {
			'Content-Type': 'application/json'
		};

		// Inclure le token si disponible pour les requêtes authentifiées
		if (token) {
			headers['Authorization'] = `Bearer ${token}`;
		}

		const response = await fetch(`${API_BASE_URL}/places/`, { headers });
		if (response.ok) {
			const places = await response.json();
			return places;
		} else {
			console.error('Échec de la récupération des lieux');
			return [];
		}
	} catch (error) {
		console.error('Erreur lors de la récupération des lieux:', error);
		return [];
	}
}

/**
 * Affiche les lieux sous forme de cartes dans la section #places-row.
 * @param {Array<Object>} places - La liste des lieux à afficher.
 */
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
			<img src="${place.image_url || '/static/images/default.png'}" alt="Place image" class="place-img">
			<button class="details-button" onclick="viewPlaceDetails('${place.id}')">View Details</button>
		`;

		placesRow.appendChild(card);
	});
}

/**
 * Filtre les cartes de lieux affichées en fonction du prix maximum.
 * @param {string} maxPrice - Le prix maximum ('all' pour aucun filtre) ou une valeur numérique.
 */
function filterPlacesByPrice(maxPrice) {
	const placeCards = document.querySelectorAll('.place-card');
	let visibleCount = 0;
	const placesRow = document.getElementById('places-row');
	let noPlacesMsg = document.getElementById('no-places-msg');

	placeCards.forEach(card => {
		const price = parseFloat(card.getAttribute('data-price'));
		if (maxPrice === 'all' || price <= parseFloat(maxPrice)) {
			card.style.display = '';
			visibleCount++;
		} else {
			card.style.display = 'none';
		}
	});

	// Gérer le message "Aucun lieu disponible"
	if (visibleCount === 0) {
		if (!noPlacesMsg && placesRow) {
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

/**
 * Redirige vers la page de détails d'un lieu.
 * @param {string} placeId - L'ID du lieu.
 */
function viewPlaceDetails(placeId) {
	window.location.href = `/place.html?id=${placeId}`;
}

// =========================================================================
// GESTION DES DÉTAILS DE LIEU
// =========================================================================

/**
 * Récupère les détails d'un lieu spécifique depuis l'API.
 * @param {string} placeId - L'ID du lieu.
 * @returns {Promise<Object|null>} Les détails du lieu ou null en cas d'échec.
 */
async function fetchPlaceDetails(placeId) {
	try {
		const response = await fetch(`${API_BASE_URL}/places/${placeId}`);
		if (response.ok) {
			const place = await response.json();
			return place;
		} else {
			console.error('Échec de la récupération des détails du lieu');
			return null;
		}
	} catch (error) {
		console.error('Erreur lors de la récupération des détails du lieu:', error);
		return null;
	}
}

/**
 * Affiche les détails du lieu dans l'élément #place-info.
 * @param {Object} place - L'objet lieu.
 */
function displayPlaceDetails(place) {
	const placeInfo = document.getElementById('place-info');
	if (!placeInfo || !place) return;

	const amenitiesInline = place.amenities && place.amenities.length > 0
		? place.amenities.map(a => a.name || a).join(', ')
		: 'No amenities listed';

	placeInfo.innerHTML = `
		<h1 class="place-title">${place.title || 'Unnamed Place'}</h1>
		<div class="place-details-box">
			<p class="place-detail"><b>Host:</b> ${place.owner ? place.owner.first_name + ' ' + place.owner.last_name : 'Unknown'}</p>
			<p class="place-detail"><b>Price per night:</b> $${place.price || 0}</p>
			<p class="place-detail"><b>Description:</b> ${place.description || 'No description available'}</p>
			<p class="place-detail"><b>Amenities:</b> ${amenitiesInline}</p>
		</div>
	`;
}

// =========================================================================
// GESTION DES AVIS (REVIEWS)
// =========================================================================

/**
 * Récupère les avis pour un lieu spécifique.
 * @param {string} placeId - L'ID du lieu.
 * @returns {Promise<Array<Object>>} La liste des avis.
 */
async function fetchReviews(placeId) {
	try {
		const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`);
		if (response.ok) {
			const reviews = await response.json();
			return reviews;
		} else {
			console.error('Échec de la récupération des avis');
			return [];
		}
	} catch (error) {
		console.error('Erreur lors de la récupération des avis:', error);
		return [];
	}
}

/**
 * Affiche les avis dans l'élément #reviews-list.
 * @param {Array<Object>} reviews - La liste des avis à afficher.
 */
function displayReviews(reviews) {
	const reviewsList = document.getElementById('reviews-list');
	if (!reviewsList) return;

	reviewsList.innerHTML = '';

	if (reviews.length === 0) {
		reviewsList.innerHTML = '<p style="text-align: left; color: #7f8c8d;">No reviews yet. Be the first to review!</p>';
		return;
	}

	reviews.forEach(review => {
		const card = document.createElement('div');
		card.className = 'review-card';

		// Utilise des étoiles pour afficher la note
		const stars = '★'.repeat(review.rating || 0) + '☆'.repeat(5 - (review.rating || 0));

		card.innerHTML = `
			<div class="review-header">
				<span class="reviewer-name">${review.user_name || 'Unknown user'}:</span>
				<p class="comment">${review.comment || review.text || 'No comment provided'}</p>
				<span class="rating"> Rating: ${stars} </span>
			</div>
		`;

		reviewsList.appendChild(card);
	});
}

/**
 * Soumet un nouvel avis via l'API (nécessite un token d'authentification).
 * @param {string} placeId - L'ID du lieu.
 * @param {string} reviewText - Le texte de l'avis.
 * @param {number} rating - La note (1-5).
 * @returns {Promise<{success: boolean, data?: any, error?: string}>} Le résultat de la soumission.
 */
async function submitReview(placeId, reviewText, rating) {
	const token = getCookie('token');

	if (!token) {
		alert('Vous devez être connecté pour soumettre un avis');
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
				error: data.error || 'Échec de la soumission de l\'avis'
			};
		}
	} catch (error) {
		console.error('Erreur lors de la soumission de l\'avis:', error);
		return {
			success: false,
			error: 'Erreur réseau. Veuillez réessayer.'
		};
	}
}


// =========================================================================
// GESTION DES ÉVÉNEMENTS DOM (DOMContentLoaded)
// =========================================================================

document.addEventListener('DOMContentLoaded', () => {
	// 1. Initialisation générale (bouton de connexion/déconnexion)
	updateLoginButton();

	// 2. Gestionnaire du formulaire de connexion
	const loginForm = document.getElementById('login-form');
	if (loginForm) {
		loginForm.addEventListener('submit', async (event) => {
			event.preventDefault();

			const email = document.getElementById('email').value;
			const password = document.getElementById('password').value;
			const errorElement = document.getElementById('login-error');

			// Logique de gestion des erreurs et du bouton de soumission
			if (errorElement) { errorElement.style.display = 'none'; errorElement.textContent = ''; }
			const submitButton = loginForm.querySelector('button[type="submit"]');
			submitButton.disabled = true;
			submitButton.textContent = 'Connecting...';

			const result = await loginUser(email, password);

			if (result.success) {
				window.location.href = '/';
			} else {
				if (errorElement) { errorElement.textContent = result.error; errorElement.style.display = 'block'; }
				submitButton.disabled = false;
				submitButton.textContent = 'Login';
			}
		});
	}

	// 3. Page d'index - Chargement et filtrage des lieux
	if (document.getElementById('places-list')) {
		const token = getCookie('token');

		// Charger les lieux
		fetchPlaces(token).then(places => {
			displayPlaces(places);
		});

		// Écouteur pour le filtre de prix
		const priceFilter = document.getElementById('price-filter');
		if (priceFilter) {
			priceFilter.addEventListener('change', (event) => {
				const selectedPrice = event.target.value;
				filterPlacesByPrice(selectedPrice);
			});
		}
	}

	// 4. Page de détails d'un lieu
	if (document.getElementById('place-info')) {
		const urlParams = new URLSearchParams(window.location.search);
		const placeId = urlParams.get('id');

		if (placeId) {
			// Charger les détails du lieu
			fetchPlaceDetails(placeId).then(place => {
				if (place) {
					displayPlaceDetails(place);
				} else {
					document.getElementById('place-info').innerHTML =
						'<p style="color: red;">Place not found</p>';
				}
			});

			// Charger les avis
			fetchReviews(placeId).then(reviews => {
				displayReviews(reviews);
			});

			// Gérer l'affichage du formulaire d'avis (si l'utilisateur est connecté)
			const reviewForm = document.getElementById('review-form');
			const addReviewBtnContainer = document.getElementById('add-review-button-container');
			if (checkAuthentication()) {
				// Afficher le formulaire et masquer le conteneur du bouton (s'ils existent)
				if (reviewForm) reviewForm.style.display = 'block';
				if (addReviewBtnContainer) addReviewBtnContainer.style.display = 'none';

				// S'assurer que le titre "Add a Review" est là
				let addReviewLabel = document.getElementById('add-review-label');
				if (!addReviewLabel) {
					addReviewLabel = document.createElement('h2');
					addReviewLabel.id = 'add-review-label';
					addReviewLabel.textContent = 'Add a Review';
					const addReviewSection = document.getElementById('add-review');
					if (addReviewSection) {
						addReviewSection.insertBefore(addReviewLabel, reviewForm);
					}
				}
			} else {
				// Supprimer le formulaire et les éléments liés si l'utilisateur n'est pas connecté
				if (reviewForm) reviewForm.remove();
				if (addReviewBtnContainer) addReviewBtnContainer.remove();
				let addReviewLabel = document.getElementById('add-review-label');
				if (addReviewLabel) addReviewLabel.remove();
			}

			// Gestion de la soumission du formulaire d'avis
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

	// 5. Page d'ajout d'avis séparée (add-review.html)
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
			// Afficher le nom du lieu en cours d'évaluation
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

					// Rediriger vers les détails du lieu après 2 secondes
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