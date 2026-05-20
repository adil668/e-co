function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
}

function showToast(message) {
    const toastEl = document.getElementById("liveToast");
    if (!toastEl) return;
    toastEl.querySelector(".toast-body").textContent = message;
    bootstrap.Toast.getOrCreateInstance(toastEl).show();
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".toast.show").forEach((el) => bootstrap.Toast.getOrCreateInstance(el, { delay: 3500 }).show());

    document.querySelectorAll(".password-toggle").forEach((button) => {
        button.addEventListener("click", () => {
            const input = button.parentElement.querySelector("input");
            input.type = input.type === "password" ? "text" : "password";
            button.innerHTML = input.type === "password" ? '<i class="bi bi-eye"></i>' : '<i class="bi bi-eye-slash"></i>';
        });
    });

    document.querySelectorAll(".add-cart-form").forEach((form) => {
        form.addEventListener("submit", async (event) => {
            event.preventDefault();
            const response = await fetch(form.action, {
                method: "POST",
                headers: { "X-Requested-With": "XMLHttpRequest", "X-CSRFToken": getCookie("csrftoken") },
                body: new FormData(form),
            });
            if (response.redirected) {
                window.location.href = response.url;
                return;
            }
            const data = await response.json();
            if (data.ok) {
                const count = document.getElementById("cartCount");
                if (count) count.textContent = data.cart_count;
                showToast(data.message);
            }
        });
    });

    document.querySelectorAll(".wishlist-form").forEach((form) => {
        form.addEventListener("submit", async (event) => {
            event.preventDefault();
            const response = await fetch(form.action, {
                method: "POST",
                headers: { "X-Requested-With": "XMLHttpRequest", "X-CSRFToken": getCookie("csrftoken") },
                body: new FormData(form),
            });
            if (response.status === 403 || response.redirected) {
                window.location.href = "/account/login/";
                return;
            }
            const data = await response.json();
            showToast(data.message);
        });
    });

    document.querySelectorAll(".cart-line").forEach((line) => {
        const input = line.querySelector(".qty-input");
        const itemId = line.dataset.itemId;
        const sync = async () => {
            const body = new FormData();
            body.append("quantity", input.value);
            const response = await fetch(`/cart/update/${itemId}/`, {
                method: "POST",
                headers: { "X-Requested-With": "XMLHttpRequest", "X-CSRFToken": getCookie("csrftoken") },
                body,
            });
            const data = await response.json();
            if (data.ok) {
                line.querySelector(".line-total").textContent = `₹${data.item_total}`;
                document.getElementById("cartSubtotal").textContent = `₹${data.cart_total}`;
                document.getElementById("cartCashback").textContent = `₹${data.cashback_total}`;
                document.getElementById("cartCount").textContent = data.cart_count;
            }
        };
        line.querySelectorAll(".qty-btn").forEach((button) => {
            button.addEventListener("click", () => {
                input.value = Math.max(1, Number(input.value || 1) + Number(button.dataset.step));
                sync();
            });
        });
        input.addEventListener("change", sync);
    });

    document.querySelectorAll(".thumb").forEach((thumb) => {
        thumb.addEventListener("click", () => {
            const main = document.getElementById("mainProductImage");
            if (main) main.src = thumb.dataset.src;
            document.querySelectorAll(".thumb").forEach((item) => item.classList.remove("active"));
            thumb.classList.add("active");
        });
    });

    const liveSearch = document.getElementById("liveSearch");
    const suggestions = document.getElementById("searchSuggestions");
    let searchTimer;
    if (liveSearch && suggestions) {
        liveSearch.addEventListener("input", () => {
            clearTimeout(searchTimer);
            searchTimer = setTimeout(async () => {
                const query = liveSearch.value.trim();
                if (query.length < 2) {
                    suggestions.style.display = "none";
                    return;
                }
                const response = await fetch(`/search/suggestions/?q=${encodeURIComponent(query)}`);
                const data = await response.json();
                suggestions.innerHTML = data.results.map((item) => `<a href="/products/${item.slug}/">${item.name}</a>`).join("");
                suggestions.style.display = data.results.length ? "block" : "none";
            }, 220);
        });
    }

    document.querySelectorAll("[data-countdown]").forEach((card) => {
        const target = new Date(card.dataset.countdown).getTime();
        const label = card.querySelector(".countdown");
        const tick = () => {
            const distance = target - Date.now();
            if (distance <= 0) {
                label.textContent = "Offer expired";
                return;
            }
            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance / (1000 * 60 * 60)) % 24);
            const minutes = Math.floor((distance / (1000 * 60)) % 60);
            label.textContent = `${days}d ${hours}h ${minutes}m left`;
        };
        tick();
        setInterval(tick, 60000);
    });

    document.querySelectorAll(".cashback-modal-btn").forEach((button) => {
        button.addEventListener("click", () => {
            document.getElementById("cashbackModalTitle").textContent = button.dataset.title;
            document.getElementById("cashbackModalDesc").textContent = button.dataset.desc;
            bootstrap.Modal.getOrCreateInstance(document.getElementById("cashbackModal")).show();
        });
    });
});
