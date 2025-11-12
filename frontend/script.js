async function sendMessage() {
    const inputField = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const userMessage = inputField.value.trim();
    if (!userMessage) return;
  
    addMessage(userMessage, "user");
    inputField.value = "";
  
    addMessage("Typing...", "bot", true);
  
    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
      });
  
      const data = await response.json();
      removeTypingIndicator();
      addMessage(data.response || "No response received.", "bot");
    } catch (error) {
      removeTypingIndicator();
      addMessage("Error connecting to server.", "bot");
    }
  }
  
  function addMessage(text, sender, isTemp = false) {
    const chatBox = document.getElementById("chat-box");
    const msg = document.createElement("div");
    msg.className = `message ${sender}`;
    msg.textContent = text;
    if (isTemp) msg.id = "typing";
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
  }
  
  function removeTypingIndicator() {
    const typing = document.getElementById("typing");
    if (typing) typing.remove();
  }
  