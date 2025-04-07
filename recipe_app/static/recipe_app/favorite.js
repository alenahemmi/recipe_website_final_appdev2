document.addEventListener('DOMContentLoaded', function () {
    const favBtn = document.getElementById('favorite-toggle');

    if (favBtn) {
        favBtn.addEventListener('click', function (e) {
            e.preventDefault();

            console.log('Button clicked!');

            fetch(favBtn.dataset.url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);

                if (data.favorited) {
                    favBtn.innerHTML = '💖 Favorited';
                } else {
                    favBtn.innerHTML = '🤍 Not Favorited';
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
});
