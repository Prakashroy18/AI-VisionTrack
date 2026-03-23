// AI Chatbot Integration Script
// Include this script in your HTML pages to activate the AI chatbot

(function() {
    'use strict';
    
    // Check if chatbot is already loaded
    if (window.aiChatbotLoaded) {
        console.log('AI Chatbot already loaded');
        return;
    }
    
    // Load the chatbot script
    function loadChatbot() {
        const script = document.createElement('script');
        script.src = '/static/js/ai-chatbot.js';
        script.onload = function() {
            console.log('AI Career Counselor Chatbot loaded successfully');
            window.aiChatbotLoaded = true;
        };
        script.onerror = function() {
            console.error('Failed to load AI Chatbot script');
        };
        document.head.appendChild(script);
    }
    
    // Load chatbot when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', loadChatbot);
    } else {
        loadChatbot();
    }
    
    // Optional: Add keyboard shortcut to open chatbot (Ctrl+Shift+C)
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.shiftKey && e.key === 'C') {
            e.preventDefault();
            if (window.aiChatbot && window.aiChatbot.toggleChatbot) {
                window.aiChatbot.toggleChatbot();
            }
        }
    });
    
    // Optional: Auto-open chatbot after delay (comment out if not needed)
    // setTimeout(() => {
    //     if (window.aiChatbot && window.aiChatbot.toggleChatbot) {
    //         window.aiChatbot.toggleChatbot();
    //     }
    // }, 3000); // Open after 3 seconds
    
})();
