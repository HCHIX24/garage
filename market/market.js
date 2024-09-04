document.getElementById('searchInput').addEventListener('input', function() {
    const query = this.value.toLowerCase();

    if (query === 'dairy' || query === 'milk' || query === 'cheese') {
        document.getElementById('dairySection').scrollIntoView({ behavior: 'smooth' });
    } else if (query === 'bakery' || query === 'bread' || query === 'croissant') {
        document.getElementById('bakerySection').scrollIntoView({ behavior: 'smooth' });
    } else if (query === 'meats' || query === 'steak' || query === 'chicken') {
        document.getElementById('meatsSection').scrollIntoView({ behavior: 'smooth' });
    } else if (query === 'sweets' || query === 'chocolate' || query === 'cupcake') {
        document.getElementById('sweetsSection').scrollIntoView({ behavior: 'smooth' });
    }
});
let cart = [];
let cartTotal = 0.00;

function addToCart(product, price) {
    cart.push({ product, price });
    cartTotal += price;
    updateCartDisplay();
    alert(`${product} added to cart!`);
}

function updateCartDisplay() {
    const cartItemsContainer = document.getElementById('cartItemsContainer');
    const cartItems = document.getElementById('cartItems');

    // Show the cart section
    cartItemsContainer.style.display = 'block';

    // Update cart items
    cartItems.innerHTML = cart.map((item, index) => `
        <div>
            <span>${item.product} - $${item.price.toFixed(2)}</span>
            <button onclick="removeFromCart(${index})">Delete</button>
        </div>
    `).join("");

    // Update cart total
    document.getElementById('cartBtn').innerHTML = `🛒 Cart ($${cartTotal.toFixed(2)})`;
}

function removeFromCart(index) {
    // Deduct the price of the item from the total
    cartTotal -= cart[index].price;
    
    // Remove the item from the cart
    cart.splice(index, 1);

    // Update the cart display
    updateCartDisplay();
}

function clearCart() {
    cart = [];
    cartTotal = 0.00;
    updateCartDisplay();
    document.getElementById('cartItemsContainer').style.display = 'none';
}
