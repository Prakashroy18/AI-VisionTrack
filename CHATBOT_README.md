# 🤖 AI Career Counselor Chatbot

A **hybrid AI chatbot** that combines rule-based logic with intelligent conversation to provide career guidance, college suggestions, and exam preparation help.

## 🎯 Features

### 🎓 **College Suggestions**
- **Rank-based recommendations** for JEE Main, TS EAMCET, AP EAMCET
- **Branch filtering** (CSE, ECE, Mechanical, etc.)
- **Detailed information**: Fees, placements, cutoffs, specialties
- **Smart fallback** for out-of-range ranks

### 💼 **Career Guidance**
- **Engineering paths**: CSE, ECE, Mechanical, Civil, etc.
- **Medical careers**: Specializations and prospects
- **Business management**: MBA paths and specializations
- **Skills requirements**: Technical and soft skills
- **Salary information**: Entry-level to experienced

### 📚 **Exam Preparation**
- **JEE Main**: Syllabus, tips, recommended books
- **TS EAMCET**: State-specific preparation guide
- **Study strategies**: Time management, practice tips
- **Best books**: Subject-wise recommendations

### 🧠 **Hybrid Intelligence**
- **Rule-based**: Accurate college suggestions
- **Natural conversation**: User-friendly interactions
- **Context awareness**: Remembers conversation history
- **Fallback logic**: Works even if backend is down

## 🏗️ Architecture

```
Frontend (Chat UI) → JavaScript (fetch API) → Flask Backend → Hybrid Logic
```

### **Frontend Components**
- `ai-chatbot.js` - Main chatbot engine
- `chatbot-integration.js` - Easy integration script
- Modern UI with animations and responsive design

### **Backend Components**
- `app_chatbot.py` - Flask API server
- Rule-based college matching algorithm
- Career and exam databases
- RESTful API endpoints

## 🚀 Quick Start

### 1. **Install Dependencies**
```bash
pip install -r requirements_chatbot.txt
```

### 2. **Start the Backend Server**
```bash
python start_chatbot.py
```
Server will start at: `http://localhost:5000`

### 3. **Add Chatbot to Your Pages**
```html
<!-- Add this before closing body tag -->
<script src="/static/js/chatbot-integration.js"></script>
```

### 4. **Test the Chatbot**
- Visit: `http://localhost:5000/chatbot-demo`
- Or open any page with the integration script

## 📱 Usage Examples

### **College Suggestions**
```
User: "My JEE rank is 5000, suggest colleges"
Bot: "Based on your rank 5000 in JEE Main, here are the best options:
     1. 🎓 NIT Warangal
        📍 Warangal, Telangana
        📊 Cutoff: Rank 1000-8000
        🔧 Specialties: Computer Science, Electronics, Mechanical
        💰 Fees: ₹1.5L/year
        💼 Placement: ₹8-25 LPA
        🏷️ Type: Government"
```

### **Career Guidance**
```
User: "Tell me about computer engineering"
Bot: "**Computer Science Engineering Career Path**
     📋 Overview: [Detailed description]
     🎯 Key Skills: Programming, Algorithms, Data Structures
     💰 Average Salary: ₹8-30 LPA
     📈 Growth Prospects: AI/ML, Cloud Computing, Cybersecurity
     🎓 Top Colleges: IITs, NITs, IIITs, BITS"
```

### **Exam Preparation**
```
User: "How to prepare for JEE Main?"
Bot: "**JEE Main Preparation Guide**
     📚 Subjects: Physics, Chemistry, Mathematics
     ⏱️ Duration: 3 hours
     📊 Total Marks: 300
     💡 Preparation Tips:
     • Focus on NCERT books for basics
     • Practice previous year papers
     • Time management is crucial"
```

## 🔧 Configuration

### **College Database**
```python
COLLEGE_DATABASE = {
    "jee_main": [
        {
            "name": "IIT Bombay",
            "max_rank": 1000,
            "specialties": ["Computer Science", "Electrical"],
            "fees": "₹2.5L/year",
            "placement": "₹20-50 LPA"
        }
        # ... more colleges
    ]
}
```

### **Adding New Colleges**
```python
# Add to COLLEGE_DATABASE in app_chatbot.py
{
    "name": "Your College",
    "location": "City, State",
    "max_rank": 5000,
    "min_rank": 1000,
    "specialties": ["Computer Science", "Mechanical"],
    "fees": "₹2L/year",
    "placement": "₹6-15 LPA",
    "type": "Private"
}
```

## 📊 API Endpoints

### **POST /chat**
Main chat endpoint for processing user messages.

**Request:**
```json
{
    "message": "My JEE rank is 5000"
}
```

**Response:**
```json
{
    "reply": "Based on your rank 5000 in JEE Main..."
}
```

### **GET /chatbot-demo**
Demo page showcasing chatbot features.

## 🎨 Customization

### **Chat Appearance**
Edit `ai-chatbot.js` styles section:
```css
.ai-chatbot {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    /* Customize colors, sizes, animations */
}
```

### **Quick Actions**
```javascript
quickActions: [
    { text: "Career Info", action: "career" },
    { text: "College Suggestions", action: "colleges" },
    { text: "Exam Help", action: "exams" }
]
```

## 🔍 Smart Features

### **Rank Extraction**
Automatically detects rank numbers from user messages:
- "My rank is 5000" → 5000
- "JEE rank 3500" → 3500
- "Score: 8000" → 8000

### **Exam Detection**
Identifies exam type from context:
- "JEE" → jee_main
- "TS EAMCET" → ts_eamcet
- "AP EAMCET" → ap_eamcet

### **Branch Matching**
Filters colleges based on branch preference:
- "Computer science" → CSE branches
- "Electronics" → ECE branches
- "Mechanical" → Mech branches

## 🛠️ Advanced Features

### **OpenAI Integration** (Optional)
```python
from openai import OpenAI

def ai_reply(prompt):
    client = OpenAI(api_key="YOUR_KEY")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

### **Conversation History**
- Automatically saves to localStorage
- Persists across page refreshes
- Maintains context for better responses

### **Keyboard Shortcuts**
- `Ctrl+Shift+C` - Open/close chatbot
- `Enter` - Send message
- `Escape` - Minimize chatbot

## 📱 Mobile Responsive

- **Adaptive UI**: Works on all screen sizes
- **Touch-friendly**: Optimized for mobile interaction
- **Performance**: Smooth animations on mobile

## 🔒 Security Features

- **CORS enabled**: Secure cross-origin requests
- **Input validation**: Prevents injection attacks
- **Error handling**: Graceful fallbacks
- **Rate limiting**: Can be added for production

## 🚀 Deployment

### **Production Setup**
```bash
# Install production server
pip install gunicorn

# Start with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app_chatbot:app
```

### **Environment Variables**
```bash
# .env file
OPENAI_API_KEY=your_key_here
FLASK_ENV=production
```

## 📈 Performance

- **Fast response**: < 1 second for rule-based queries
- **Efficient matching**: O(n) college filtering
- **Low memory**: Minimal database footprint
- **Scalable**: Easy to add more data

## 🎯 Use Cases

### **For Students**
- Get instant college suggestions
- Career path guidance
- Exam preparation help
- Branch selection advice

### **For Educational Institutions**
- Student counseling tool
- Admission guidance
- Course information
- FAQ automation

### **For Career Counselors**
- Assistant tool for counseling
- Quick information access
- Student engagement
- Data-driven insights

## 🔮 Future Enhancements

- **Voice chat**: Speech-to-text integration
- **File upload**: Resume analysis
- **Video calls**: Live counseling sessions
- **Analytics**: User behavior insights
- **Multi-language**: Support for regional languages

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add your improvements
4. Test thoroughly
5. Submit pull request

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Review API documentation
- Test with the demo page
- Check browser console for errors

---

## 🎉 Project Impact

This chatbot demonstrates:
- **Hybrid AI architecture**
- **Practical problem solving**
- **Real-world application**
- **User-centered design**
- **Scalable solution**

Perfect for:
- **College projects**
- **Hackathons**
- **Portfolio pieces**
- **Startup MVPs**
- **Educational tools**

---

**🚀 Your AI Career Counselor is ready to assist students!**
