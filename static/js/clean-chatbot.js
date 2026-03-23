// Clean AI Chatbot - Simple Implementation
// Circular AI icon at bottom-right corner

class CleanAIChatbot {
    constructor() {
        this.init();
    }

    init() {
        this.createChatUI();
        this.attachEventListeners();
    }

    createChatUI() {
        // Create the HTML structure
        const chatHTML = `
            <!-- AI Floating Chat Button -->
            <div id="ai-chat-btn">
                🤖
            </div>

            <!-- AI Chat Box -->
            <div id="ai-chat-box">
                <div id="ai-chat-header">
                    AI Career Assistant
                    <span id="ai-close">✖</span>
                </div>

                <div id="ai-chat-messages">
                    <div class="ai-msg">
                        <b>AI:</b> 👋 Hello! I'm your AI Career Assistant. I can help you with:
                        <br>• 🎓 College suggestions based on rank
                        <br>• 💼 Career guidance and paths
                        <br>• 📚 Exam preparation tips
                        <br>• 🎯 Branch recommendations
                        <br><br>Try: "TS EAMCET rank 3500" or "JEE rank 5000"
                    </div>
                </div>

                <div id="ai-chat-input">
                    <input id="ai-user-input" placeholder="Ask your doubt..." maxlength="500" />
                    <button onclick="cleanChatbot.sendMessage()">➤</button>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', chatHTML);
        this.addStyles();
    }

    addStyles() {
        const styles = `
            <style id="cleanChatbotStyles">
                /* Floating AI Chat Button */
                #ai-chat-btn {
                    position: fixed;
                    bottom: 25px;
                    right: 25px;
                    width: 64px;
                    height: 64px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #a855f7, #4895ef);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 30px;
                    cursor: pointer;
                    box-shadow: 0 12px 30px rgba(168, 85, 247, 0.6);
                    z-index: 2000;
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                }

                #ai-chat-btn:hover {
                    transform: scale(1.1);
                    box-shadow: 0 16px 40px rgba(168, 85, 247, 0.9);
                }

                /* AI Chat Box */
                #ai-chat-box {
                    position: fixed;
                    bottom: 100px; /* appears above the button */
                    right: 25px;
                    width: 340px;
                    height: 420px;
                    background: #0a0e27;
                    border-radius: 18px;
                    display: none;
                    flex-direction: column;
                    box-shadow: 0 20px 50px rgba(0,0,0,0.7);
                    z-index: 2000;
                    animation: slideUp 0.35s ease;
                }

                @keyframes slideUp {
                    from { transform: translateY(20px); opacity: 0; }
                    to { transform: translateY(0); opacity: 1; }
                }

                /* Header */
                #ai-chat-header {
                    padding: 14px;
                    background: linear-gradient(135deg, #a855f7, #4895ef);
                    font-weight: 700;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    border-radius: 18px 18px 0 0;
                    color: white;
                }

                #ai-close {
                    cursor: pointer;
                    font-size: 16px;
                    opacity: 0.8;
                    transition: opacity 0.3s ease;
                }

                #ai-close:hover {
                    opacity: 1;
                }

                /* Messages */
                #ai-chat-messages {
                    flex: 1;
                    padding: 12px;
                    overflow-y: auto;
                    font-size: 0.95rem;
                    background: rgba(15, 23, 42, 0.5);
                }

                #ai-chat-messages::-webkit-scrollbar {
                    width: 6px;
                }

                #ai-chat-messages::-webkit-scrollbar-track {
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 3px;
                }

                #ai-chat-messages::-webkit-scrollbar-thumb {
                    background: rgba(168, 85, 247, 0.5);
                    border-radius: 3px;
                }

                /* Message styles */
                .user-msg, .ai-msg {
                    margin: 8px 0;
                    padding: 8px 12px;
                    border-radius: 12px;
                    animation: messageSlide 0.3s ease;
                }

                @keyframes messageSlide {
                    from {
                        transform: translateY(10px);
                        opacity: 0;
                    }
                    to {
                        transform: translateY(0);
                        opacity: 1;
                    }
                }

                .user-msg {
                    text-align: right;
                    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
                    color: white;
                    margin-left: 20%;
                }

                .ai-msg {
                    text-align: left;
                    background: rgba(168, 85, 247, 0.1);
                    border: 1px solid rgba(168, 85, 247, 0.3);
                    color: #e0e7ff;
                    margin-right: 20%;
                }

                /* Input */
                #ai-chat-input {
                    display: flex;
                    padding: 10px;
                    border-top: 1px solid rgba(255,255,255,0.1);
                    background: rgba(30, 41, 59, 0.8);
                }

                #ai-chat-input input {
                    flex: 1;
                    padding: 8px 12px;
                    border-radius: 8px;
                    border: 1px solid rgba(168, 85, 247, 0.3);
                    background: rgba(15, 23, 42, 0.8);
                    outline: none;
                    color: white;
                    font-size: 14px;
                    transition: all 0.3s ease;
                }

                #ai-chat-input input:focus {
                    border-color: #4895ef;
                    box-shadow: 0 0 0 2px rgba(72, 149, 239, 0.2);
                }

                #ai-chat-input input::placeholder {
                    color: #64748b;
                }

                #ai-chat-input button {
                    margin-left: 8px;
                    padding: 8px 12px;
                    background: linear-gradient(135deg, #4895ef, #1d4ed8);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    font-weight: 600;
                }

                #ai-chat-input button:hover {
                    transform: translateY(-1px);
                    box-shadow: 0 4px 12px rgba(72, 149, 239, 0.4);
                }

                /* AI typing indicator */
                .ai-typing {
                    display: flex;
                    align-items: center;
                    gap: 6px;
                    margin: 8px 0;
                    font-size: 0.9rem;
                    color: #c7d2fe;
                }

                .ai-typing span {
                    width: 6px;
                    height: 6px;
                    background: #a855f7;
                    border-radius: 50%;
                    animation: blink 1.4s infinite both;
                }

                .ai-typing span:nth-child(2) {
                    animation-delay: 0.2s;
                }

                .ai-typing span:nth-child(3) {
                    animation-delay: 0.4s;
                }

                @keyframes blink {
                    0% { opacity: 0.2; }
                    20% { opacity: 1; }
                    100% { opacity: 0.2; }
                }
                @media (max-width: 480px) {
                    #ai-chat-box {
                        width: calc(100vw - 50px);
                        right: 25px;
                        left: 25px;
                    }
                }
            </style>
        `;
        
        if (!document.getElementById('cleanChatbotStyles')) {
            document.head.insertAdjacentHTML('beforeend', styles);
        }
    }

    attachEventListeners() {
        const chatBtn = document.getElementById("ai-chat-btn");
        const chatBox = document.getElementById("ai-chat-box");
        const closeBtn = document.getElementById("ai-close");
        const input = document.getElementById("ai-user-input");

        // Toggle chat
        chatBtn.onclick = () => this.openChat();
        closeBtn.onclick = () => this.closeChat();

        // Enter key to send
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });

        // Auto-focus input when chat opens
        chatBtn.addEventListener('click', () => {
            setTimeout(() => input.focus(), 300);
        });
    }

    openChat() {
        const chatBox = document.getElementById("ai-chat-box");
        chatBox.style.display = "flex";
    }

    closeChat() {
        const chatBox = document.getElementById("ai-chat-box");
        chatBox.style.display = "none";
    }

    async sendMessage() {
        const input = document.getElementById("ai-user-input");
        const messages = document.getElementById("ai-chat-messages");
        const msg = input.value.trim();
        
        if (!msg) return;

        // Add user message
        this.addMessage(msg, 'user');
        input.value = "";

        // Typing indicator
        const typingDiv = document.createElement("div");
        typingDiv.className = "ai-typing";
        typingDiv.innerHTML = `
            <span></span><span></span><span></span>
            <em style="margin-left:6px;">AI is typing...</em>
        `;
        messages.appendChild(typingDiv);
        messages.scrollTop = messages.scrollHeight;

        try {
            // Fetch AI reply
            const response = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: msg })
            });

            const data = await response.json();
            console.log("AI Response:", data);

            // Remove typing indicator
            typingDiv.remove();

            // Add AI response with proper error handling
            if(data.reply){
                this.addMessage(data.reply, 'ai');
            } else {
                this.addMessage("AI could not respond. Please try again.", 'ai');
            }
            
        } catch (error) {
            console.error('Chat error:', error);
            
            // Remove typing indicator
            typingDiv.remove();
            
            // Fallback response
            this.addMessage("I can help with college rankings, career guidance, and exam preparation. Try asking about 'TS EAMCET rank 3500'!", 'ai');
        }
    }

    addMessage(message, type) {
        const messages = document.getElementById("ai-chat-messages");
        const messageDiv = document.createElement('div');
        messageDiv.className = `${type}-msg`;
        messageDiv.innerHTML = `<b>${type === 'user' ? 'You' : 'AI'}:</b> ${message}`;
        
        messages.appendChild(messageDiv);
        messages.scrollTop = messages.scrollHeight;
    }
}

// Initialize the chatbot
let cleanChatbot;
document.addEventListener('DOMContentLoaded', () => {
    cleanChatbot = new CleanAIChatbot();
});
