(function () {
    const widget = document.querySelector(".chatbot-widget");
    if (!widget) {
        return;
    }

    const toggleButton = widget.querySelector(".chatbot-toggle");
    const closeButton = widget.querySelector(".chatbot-close");
    const panel = widget.querySelector(".chatbot-panel");
    const form = widget.querySelector(".chatbot-form");
    const input = widget.querySelector(".chatbot-input");
    const messages = widget.querySelector(".chatbot-messages");
    const typing = widget.querySelector(".chatbot-typing");
    const sendButton = widget.querySelector(".chatbot-send");
    const endpoint = "/chatbot/chat/";

    function openChat() {
        widget.classList.add("is-open");
        toggleButton.setAttribute("aria-expanded", "true");
        panel.setAttribute("aria-hidden", "false");
        input.focus();
        scrollToBottom();
    }

    function closeChat() {
        widget.classList.remove("is-open");
        toggleButton.setAttribute("aria-expanded", "false");
        panel.setAttribute("aria-hidden", "true");
        toggleButton.focus();
    }

    function addMessage(text, role, matches) {
        const bubble = document.createElement("div");
        bubble.className = `chatbot-message chatbot-message-${role}`;
        bubble.textContent = text;

        if (role === "bot" && Array.isArray(matches) && matches.length > 0) {
            bubble.appendChild(renderSources(matches));
        }

        messages.appendChild(bubble);
        scrollToBottom();
    }

    function renderSources(matches) {
        const sources = document.createElement("div");
        sources.className = "chatbot-sources";

        const bestSources = matches.slice(0, 2).map(function (match) {
            const metadata = match.metadata || {};
            const title = metadata.title || "Stored content";
            const score = typeof match.score === "number" ? ` (${Math.round(match.score * 100)}%)` : "";
            return `${title}${score}`;
        });

        sources.textContent = `Sources: ${bestSources.join(", ")}`;
        return sources;
    }

    function addError(text) {
        addMessage(text, "error");
    }

    function setLoading(isLoading) {
        typing.hidden = !isLoading;
        input.disabled = isLoading;
        sendButton.disabled = isLoading;
        if (!isLoading) {
            input.focus();
        }
    }

    function scrollToBottom() {
        messages.scrollTop = messages.scrollHeight;
    }

    async function sendMessage(message) {
        setLoading(true);
        try {
            const response = await fetch(endpoint, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest"
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || "The chatbot could not answer right now.");
            }

            addMessage(data.answer || "I could not find an answer.", "bot", data.matches || []);
        } catch (error) {
            addError(error.message || "Something went wrong. Please try again.");
        } finally {
            setLoading(false);
        }
    }

    toggleButton.addEventListener("click", function () {
        if (widget.classList.contains("is-open")) {
            closeChat();
        } else {
            openChat();
        }
    });

    closeButton.addEventListener("click", closeChat);

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        const message = input.value.trim();
        if (!message) {
            return;
        }

        addMessage(message, "user");
        input.value = "";
        sendMessage(message);
    });
})();
