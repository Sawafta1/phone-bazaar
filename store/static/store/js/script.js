// store/static/store/js/script.js

document.addEventListener('DOMContentLoaded', function () {
    // Add to Cart (same as before)
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    addToCartButtons.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const phoneId = this.getAttribute('data-id');

            fetch(`/add-to-cart/${phoneId}/`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Phone added to cart!');
                }
            });
        });
    });

    // Remove specific quantity from cart
    const removeButtons = document.querySelectorAll('.remove-btn');

    removeButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            const phoneId = this.getAttribute('data-id');
            const input = document.querySelector(`.quantity-input[data-id="${phoneId}"]`);
            const amount = input ? parseInt(input.value) : 1;

            fetch('/remove-from-cart/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `phone_id=${phoneId}&amount=${amount}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                }
            });
        });
    });
});

// CSRF helper
function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        if (cookie.trim().startsWith('csrftoken=')) {
            return cookie.trim().split('=')[1];
        }
    }
    return '';
}
