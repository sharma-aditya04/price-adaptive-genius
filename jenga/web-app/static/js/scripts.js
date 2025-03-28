document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('urlForm');
    const resultDiv = document.getElementById('result');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const amazonUrl = document.getElementById('amazonUrl').value;
        const flipkartUrl = document.getElementById('flipkartUrl').value;

        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                amazon_url: amazonUrl,
                flipkart_url: flipkartUrl || 0
            })
        })
        .then(response => response.json())
        .then(data => {
            resultDiv.innerHTML = `AI Price: ${data.ai_price}`;
        })
        .catch(error => {
            console.error('Error:', error);
            resultDiv.innerHTML = 'An error occurred while processing your request.';
        });
    });
});