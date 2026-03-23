from flask import Flask, render_template, request, redirect, url_for, send_file, session, jsonify
from ai_resume_generator import generate_ai_resume_content, enhance_skill_descriptions, generate_career_insights
from utils.generate_resume import generate_resume
from utils.course_recommender import get_personalized_recommendations, generate_learning_path, get_career_insights
import joblib
import os
import requests
import time
from functools import wraps
from dotenv import load_dotenv
from firebase_config import create_user, sign_in_user
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import random

# Load .env for local development (optional)
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    
    return decorated_function

# Load ML model and encoder
model = joblib.load("model/career_model.pkl")
label_encoder = joblib.load("model/label_encoder.pkl")

# Load college dataset and train prediction model
def load_college_data():
    """Load college dataset from CSV file"""
    try:
        df = pd.read_csv("colleges_dataset.csv")
        print(f"Loaded {len(df)} colleges from dataset")
        return df
    except Exception as e:
        print(f"Error loading college dataset: {e}")
        return pd.DataFrame()

# Initialize college data
college_data = load_college_data()

# -----------------------------
# COMPREHENSIVE COURSE DATABASE
# -----------------------------

COURSE_DATABASE = {
    "software developer": [
        ("🔥 Core Programming", [
            ("Python Programming", "https://www.freecodecamp.org/learn/scientific-computing-with-python/", "3 months"),
            ("JavaScript & ES6+", "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/", "2 months"),
            ("Java Programming", "https://www.coursera.org/learn/java-programming", "2 months"),
            ("Git & GitHub", "https://www.coursera.org/learn/git", "1 month")
        ]),
        ("🚀 Full Stack Development", [
            ("Complete Web Development", "https://www.freecodecamp.org/learn/full-stack/", "4 months"),
            ("React.js Course", "https://reactjs.org/tutorial/tutorial.html", "2 months"),
            ("Node.js Backend", "https://nodejs.org/en/learn/", "2 months"),
            ("MongoDB Database", "https://www.mongodb.com/learn/", "1 month")
        ]),
        ("⚡ Advanced Skills", [
            ("Data Structures & Algorithms", "https://www.geeksforgeeks.org/data-structures/", "3 months"),
            ("System Design", "https://roadmap.sh/backend", "2 months"),
            ("Cloud Computing (AWS)", "https://aws.amazon.com/training/", "2 months"),
            ("Docker & DevOps", "https://www.docker.com/101-tutorial/", "1 month")
        ])
    ],
    "data scientist": [
        ("🤖 Machine Learning", [
            ("ML Crash Course", "https://developers.google.com/machine-learning/crash-course", "1 month"),
            ("Andrew Ng ML Course", "https://www.coursera.org/learn/machine-learning", "3 months"),
            ("Python for Data Science", "https://www.kaggle.com/learn/python", "2 months"),
            ("Statistics & Probability", "https://www.khanacademy.org/math/statistics-probability", "1 month")
        ]),
        ("📈 Data Analysis", [
            ("Pandas Tutorial", "https://www.kaggle.com/learn/pandas", "2 months"),
            ("NumPy Basics", "https://numpy.org/doc/stable/user/absolute_beginners.html", "1 month"),
            ("Data Visualization", "https://www.kaggle.com/learn/data-visualization", "1 month"),
            ("SQL for Data Science", "https://www.sqltutorial.org/", "1 month")
        ]),
        ("🔥 Deep Learning", [
            ("Deep Learning Specialization", "https://www.coursera.org/specializations/deep-learning", "4 months"),
            ("TensorFlow Tutorial", "https://www.tensorflow.org/learn", "2 months"),
            ("Neural Networks", "https://www.deeplearning.ai/ai-for-everyone/", "2 months"),
            ("Computer Vision", "https://www.coursera.org/learn/convolutional-neural-networks", "2 months")
        ])
    ],
    "ai engineer": [
        ("🧠 Mathematics Fundamentals", [
            ("Mathematics for ML", "https://www.coursera.org/learn/machine-learning-mathematics", "2 months"),
            ("Linear Algebra", "https://www.khanacademy.org/math/linear-algebra", "1 month"),
            ("Calculus & Optimization", "https://www.khanacademy.org/math/calculus-1", "1 month"),
            ("Statistics & Probability", "https://www.khanacademy.org/math/statistics-probability", "1 month")
        ]),
        ("⚡ Machine Learning", [
            ("Hands-On ML", "https://www.coursera.org/learn/machine-learning-hands-on", "3 months"),
            ("Advanced ML", "https://www.coursera.org/specializations/machine-learning-introduction-tensorflow", "4 months"),
            ("ML Engineering", "https://www.coursera.org/learn/machine-learning-engineering-for-production-mlops", "2 months"),
            ("Reinforcement Learning", "https://www.coursera.org/learn/reinforcement-learning", "2 months")
        ]),
        ("🔥 Deep Learning & AI", [
            ("Neural Networks", "https://www.deeplearning.ai/ai-for-everyone/", "2 months"),
            ("Computer Vision", "https://www.coursera.org/learn/convolutional-neural-networks", "2 months"),
            ("NLP & Transformers", "https://www.coursera.org/learn/natural-language-processing", "3 months"),
            ("Generative AI", "https://www.coursera.org/learn/generative-ai-with-llms", "2 months")
        ])
    ],
    "web developer": [
        ("🎨 Frontend Development", [
            ("HTML & CSS", "https://www.freecodecamp.org/learn/responsive-web-design/", "1 month"),
            ("JavaScript Advanced", "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/", "2 months"),
            ("React.js Framework", "https://reactjs.org/tutorial/tutorial.html", "2 months"),
            ("Tailwind CSS", "https://tailwindcss.com/", "1 month")
        ]),
        ("🔧 Backend Development", [
            ("Node.js & Express", "https://nodejs.org/en/learn/", "2 months"),
            ("Python Django", "https://www.djangoproject.com/start/", "3 months"),
            ("REST APIs", "https://www.freecodecamp.org/learn/apis-and-microservices/", "1 month"),
            ("Database Design", "https://www.mongodb.com/learn/", "1 month")
        ])
    ],
    "mobile developer": [
        ("📱 Android Development", [
            ("Kotlin & Android Studio", "https://developer.android.com/courses", "3 months"),
            ("React Native", "https://reactnative.dev/", "2 months"),
            ("Flutter Development", "https://flutter.dev/learn", "2 months")
        ]),
        ("🍎 iOS Development", [
            ("Swift Programming", "https://developer.apple.com/learn/", "3 months"),
            ("SwiftUI & iOS Apps", "https://developer.apple.com/xcode/", "2 months"),
            ("iOS App Deployment", "https://developer.apple.com/app-store/", "1 month")
        ])
    ]
}

# -----------------------------
# ENHANCED SKILL RECOMMENDATIONS
# -----------------------------

SKILL_DATABASE = {
    "software developer": [
        "Python, JavaScript, Java, C++",
        "React, Node.js, Django, Spring",
        "Git, Docker, AWS, SQL",
        "Data Structures, Algorithms, System Design",
        "REST APIs, Microservices, Testing"
    ],
    "data scientist": [
        "Python, R, SQL",
        "Pandas, NumPy, Scikit-learn",
        "TensorFlow, PyTorch, Keras",
        "Statistics, Linear Algebra, Calculus",
        "Data Visualization, Machine Learning, Deep Learning"
    ],
    "ai engineer": [
        "Python, C++, Mathematics",
        "TensorFlow, PyTorch, Scikit-learn",
        "Neural Networks, Computer Vision, NLP",
        "AWS, GCP, Azure, Docker",
        "ML Engineering, MLOps, Research"
    ],
    "web developer": [
        "HTML, CSS, JavaScript",
        "React, Vue, Angular, Node.js",
        "Tailwind, Bootstrap, SASS",
        "REST APIs, GraphQL, MongoDB"
    ]
}

# -----------------------------
# SMART RESPONSE GENERATORS
# -----------------------------

def generate_career_roadmap(career_type):
    """Generate complete career roadmap with timeline"""
    if career_type in COURSE_DATABASE:
        roadmap = f"🚀 **Complete Roadmap for {career_type.title()}**\n\n"
        total_months = 0
        
        for phase, courses in COURSE_DATABASE[career_type]:
            roadmap += f"**{phase}**\n"
            for course_name, course_url, duration in courses:
                roadmap += f"• {course_name} ({duration})\n  {course_url}\n"
                total_months += int(duration.split()[0]) if duration.split()[0].isdigit() else 2
            roadmap += "\n"
        
        roadmap += f"💼 **Expected Timeline:** {total_months} months\n"
        
        # Add salary expectations
        salary_ranges = {
            "software developer": "8-15 LPA",
            "data scientist": "12-25 LPA", 
            "ai engineer": "20-50 LPA",
            "web developer": "6-12 LPA",
            "mobile developer": "8-18 LPA"
        }
        
        if career_type in salary_ranges:
            roadmap += f"💰 **Expected Package:** {salary_ranges[career_type]} (Freshers)\n"
        
        return roadmap
    
    return "Career not found. Try: software developer, data scientist, ai engineer, web developer"

def generate_skill_recommendations(career_type):
    """Generate skill recommendations for career"""
    if career_type in SKILL_DATABASE:
        skills = SKILL_DATABASE[career_type]
        return f"🎯 **Essential Skills for {career_type.title()}:**\n\n" + "\n".join([f"• {skill}" for skill in skills])
    return "Skills not found for this career."

def predict_ap_colleges(rank, branch='CSE'):
    """Predict AP EAMCET colleges based on rank"""
    if rank <= 2000:
        return f"""• Andhra University College of Engineering ({branch})
• JNTU Kakinada ({branch})
• SV University ({branch})
• Vignan's Lara Institute of Technology ({branch})"""
    elif rank <= 5000:
        return f"""• Vignan University ({branch})
• GVP College of Engineering ({branch})
• SRM University AP ({branch})
• Lakireddy Bali Reddy College ({branch})"""
    elif rank <= 10000:
        return f"""• KL University ({branch})
• VVIT Guntur ({branch})
• RVR & JC College of Engineering ({branch})
• NRI Institute of Technology ({branch})"""
    elif rank <= 20000:
        return f"""• Aditya Engineering College ({branch})
• Pragati Engineering College ({branch})
• PVP Siddhartha Engineering College ({branch})
• VSM College of Engineering ({branch})"""
    else:
        return f"""• GIET Engineering College ({branch})
• DNR College of Engineering ({branch})
• QIS College of Engineering ({branch})
• Vignana Bharathi Institute ({branch})"""

def predict_colleges_by_exam(rank, exam, branch="CSE"):
    """Predict colleges based on exam, rank, and branch using real dataset"""
    if college_data.empty:
        return "Dataset not available. Please try again later."
    
    # Filter by exam type
    df = college_data.copy()
    df = df[df["exam"].str.lower() == exam.lower()]
    
    if df.empty:
        return f"No colleges found for {exam}."
    
    # Calculate distance from user's rank
    df["distance"] = abs(df["rank"] - rank)
    
    # Get 5 closest colleges
    closest = df.nsmallest(5, "distance")
    
    result = ""
    for _, row in closest.iterrows():
        result += f"• {row['college']} ({row['branch']}) - {row['location']}\n"
    
    return result

def predict_colleges(rank, branch='CSE'):
    """Predict colleges based on rank using ML-enhanced approach"""
    try:
        # Filter by branch if available
        if 'branch' in college_data.columns:
            branch_data = college_data[college_data['branch'] == branch]
        else:
            branch_data = college_data
        
        # Find closest ranks (get 5 best matches)
        branch_data = branch_data.copy()
        branch_data['distance'] = abs(branch_data['rank'] - rank)
        closest_colleges = branch_data.nsmallest(5, 'distance')
        
        # Format results
        result = ""
        for _, row in closest_colleges.iterrows():
            result += f"• {row['college']} ({row.get('branch', branch)})\n"
        
        return result
        
    except Exception as e:
        # Fallback to simple rule-based prediction
        if rank <= 2000:
            return f"• JNTUH College of Engineering ({branch})\n• OU College of Engineering ({branch})\n• CBIT Hyderabad ({branch})"
        elif rank <= 5000:
            return f"• VNR Vignana Jyothi Institute of Technology ({branch})\n• GRIET Hyderabad ({branch})\n• KMIT Hyderabad ({branch})"
        elif rank <= 10000:
            return f"• MGIT Hyderabad ({branch})\n• SNIST Hyderabad ({branch})\n• CMR College of Engineering ({branch})"
        else:
            return f"• Malla Reddy Engineering College ({branch})\n• Anurag University ({branch})\n• ACE Engineering College ({branch})"


def get_edx_courses(career_path, access_token=None, max_results=3):
    """
    Fetch course recommendations from Open edX API with improved error handling
    """
    courses = []
    
    if not access_token:
        # Return mock courses when no token is available
        mock_courses = {
            "python": [
                {"title": "Introduction to Python Programming", "url": "https://sandbox.openedx.org/courses/course-v1:DemoX+Demo_Course/about", "description": "Learn Python programming fundamentals including variables, functions, and data structures.", "provider": "Open edX Demo"},
                {"title": "Advanced Python for Data Science", "url": "https://sandbox.openedx.org/courses/course-v1:DemoX+Advanced_Python+2024/about", "description": "Master advanced Python concepts for data science including NumPy, Pandas, and data visualization.", "provider": "Open edX Demo"}
            ],
            "data science": [
                {"title": "Data Science Fundamentals", "url": "https://sandbox.openedx.org/courses/course-v1:DemoX+Data_Science+2024/about", "description": "Introduction to data science concepts, statistics, and machine learning basics.", "provider": "Open edX Demo"},
                {"title": "Machine Learning with Python", "url": "https://sandbox.openedx.org/courses/course-v1:DemoX+ML_Python+2024/about", "description": "Learn machine learning algorithms and implementation using Python.", "provider": "Open edX Demo"}
            ],
            "software developer": [
                {"title": "Full Stack Web Development", "url": "https://sandbox.openedx.org/courses/course-v1:DemoX+Web_Dev+2024/about", "description": "Complete web development course covering HTML, CSS, JavaScript, and backend frameworks.", "provider": "Open edX Demo"}
            ],
            "web development": [
                {"title": "HTML, CSS, and JavaScript for Web Developers", "url": "https://sandbox.openedx.org/courses/course-v1:DemoX+Web_Dev+2024/about", "description": "Master web development fundamentals with hands-on projects.", "provider": "Open edX Demo"}
            ],
            "business analyst": [
                {"title": "Business Analytics Fundamentals", "url": "https://sandbox.openedx.org/courses/course-v1:DemoX+Business_Analytics+2024/about", "description": "Learn business analysis techniques and tools for data-driven decision making.", "provider": "Open edX Demo"}
            ],
            "asp.net": [
                {"title": "ASP.NET Core Development", "url": "https://sandbox.openedx.org/courses/course-v1:DemoX+ASP_NET_Core+2024/about", "description": "Build modern web applications with ASP.NET Core and C#.", "provider": "Open edX Demo"},
                {"title": "C# Programming Advanced", "url": "https://sandbox.openedx.org/courses/course-v1:DemoX+CSharp_Advanced+2024/about", "description": "Advanced C# programming concepts and .NET framework development.", "provider": "Open edX Demo"}
            ]
        }
        
        # Return career-specific mock courses
        career_lower = career_path.lower() if isinstance(career_path, str) else str(career_path).lower()
        for key, course_list in mock_courses.items():
            if any(keyword in career_lower for keyword in key.split()):
                return course_list[:max_results]
        
        # Fallback to general courses
        return mock_courses.get("python", [])[:max_results]
    
    # Find matching courses based on query
    query_lower = str(career_path).lower()
    for key, course_list in mock_courses.items():
        if key in query_lower or any(word in query_lower for word in key.split()):
            return course_list[:max_results]
    
    # Default courses if no match
    return [
        {"title": "Computer Science Fundamentals", "url": "https://sandbox.openedx.org/courses/course-v1:DemoX+CS_Fundamentals+2024/about", "description": "Introduction to computer science concepts and programming fundamentals.", "provider": "Open edX Demo"}
    ]


# Simple in-memory cache for edX token
_edx_token_cache = {"token": None, "expires_at": 0}


def get_edx_access_token():
    """Obtain an edX access token using client credentials from env vars.
    This function caches the token in-memory until shortly before expiry.
    Environment variables used:
      - EDX_CLIENT_ID
      - EDX_CLIENT_SECRET
      - EDX_TOKEN_URL (optional, default uses edX auth endpoint)
    Returns access_token string or None on failure.
    """
    client_id = os.environ.get('EDX_CLIENT_ID')
    client_secret = os.environ.get('EDX_CLIENT_SECRET')
    if not client_id or not client_secret:
        return None

    # Return cached token if still valid
    now = time.time()
    if _edx_token_cache.get('token') and _edx_token_cache.get('expires_at', 0) - 30 > now:
        return _edx_token_cache['token']

    token_url = os.environ.get('EDX_TOKEN_URL', 'https://auth.edx.org/oauth2/access_token')

    try:
        # Use HTTP Basic auth as the standard client-credentials flow
        data = {'grant_type': 'client_credentials'}
        resp = requests.post(token_url, auth=(client_id, client_secret), data=data, timeout=6)
        if resp.status_code != 200:
            return None
        payload = resp.json()
        access_token = payload.get('access_token')
        expires_in = int(payload.get('expires_in', 0) or 0)
        if access_token:
            expires_at = now + max(expires_in - 30, 30)
            _edx_token_cache['token'] = access_token
            _edx_token_cache['expires_at'] = expires_at
            return access_token
    except Exception:
        return None

    return None

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard page - requires login"""
    # Get user data from session
    user_id = session.get('user_id')
    user_data = {
        'name': session.get('user_name', 'John Doe'),
        'email': session.get('user_email', 'john.doe@example.com'),
        'avatar_icon': '👤',
        'courses_completed': session.get('courses_completed', 8),
        'total_courses': session.get('total_courses', 12),
        'certificates': session.get('certificates', 4)
    }
    return render_template('dashboard.html', user=user_data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and authentication"""
    if request.method == 'POST':
        # Check if JSON data (from Firebase) or form data (traditional)
        if request.is_json:
            # Firebase login data
            data = request.get_json()
            email = data.get('email')
            uid = data.get('uid')
            
            if email and uid:
                # Set session from Firebase authentication
                session['user_id'] = uid
                session['user_name'] = email.split('@')[0]  # Use email prefix as name
                session['user_email'] = email
                session['logged_in'] = True
                
                print(f"Firebase login successful: {email}")
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', error='Invalid Firebase data')
        else:
            # Traditional form login (fallback)
            username = request.form.get('username')
            password = request.form.get('password')
            
            # Firebase authentication
            try:
                # Sign in user with Firebase
                result = sign_in_user(username, password)
                
                if result['success']:
                    # Set session
                    session['user_id'] = result['user_id']
                    session['user_name'] = username
                    session['user_email'] = result.get('email', f'{username}@example.com')
                    session['logged_in'] = True
                    
                    return redirect(url_for('dashboard'))
                else:
                    return render_template('login.html', error=result.get('error', 'Invalid credentials'))
                    
            except Exception as e:
                print(f"Login error: {e}")
                return render_template('login.html', error='Login failed. Please try again.')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup page with Firebase integration"""
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not all([email, password, confirm_password]):
            return render_template('signup.html', error='All fields are required')
        
        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match')
        
        if len(password) < 6:
            return render_template('signup.html', error='Password must be at least 6 characters long')
        
        # Create user in Firebase
        try:
            result = create_user(email, password)
            
            if result['success']:
                return render_template('signup.html', success='Account created successfully! Please login.')
            else:
                return render_template('signup.html', error=f'Account creation failed: {result.get("error", "Unknown error")}')
                
        except Exception as e:
            return render_template('signup.html', error=f'Server error: {str(e)}')
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    """Logout user and clear session"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/api/recommendations')
@login_required
def get_recommendations():
    """Get personalized course recommendations via API"""
    try:
        # Get user data from session or form
        user_data = {
            'role': session.get('user_role', request.args.get('role', 'software_developer')),
            'skills': session.get('user_skills', request.args.get('skills', '').split(',')),
            'interests': session.get('user_interests', request.args.get('interests', '').split(',')),
            'education': session.get('user_education', request.args.get('education', 'intermediate')),
            'work_type': session.get('work_type', request.args.get('work_type', 'office'))
        }
        
        # Import static recommendation engine
        from recommendation_engine import get_recommendations
        
        # Get recommendations using static engine
        recommendations = get_recommendations(
            user_role=user_data['role'],
            user_skills=user_data['skills'] if user_data['skills'] else None,
            max_recommendations=8
        )
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'user_profile': user_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/set-profile', methods=['POST'])
def set_profile():
    """Set user profile in session for testing"""
    try:
        data = request.get_json()
        session['user_role'] = data.get('role', 'software_developer')
        session['user_skills'] = data.get('skills', ['python'])
        session['user_interests'] = data.get('interests', [])
        session['user_education'] = data.get('education', 'intermediate')
        session['work_type'] = data.get('work_type', 'office')
        
        return jsonify({'success': True, 'message': 'Profile updated'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/learning-path/<career_path>')
@login_required
def get_learning_path(career_path):
    """Get structured learning path for a career"""
    try:
        user_data = {
            'skills': session.get('user_skills', []),
            'interests': session.get('user_interests', []),
            'education': session.get('user_education', 'intermediate'),
            'work_type': session.get('work_type', 'office')
        }
        
        learning_path = generate_learning_path(user_data, career_path)
        
        return jsonify({
            'success': True,
            'career_path': career_path,
            'learning_path': learning_path
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/career-insights')
@login_required
def get_insights():
    """Get personalized career insights"""
    try:
        user_data = {
            'skills': session.get('user_skills', []),
            'interests': session.get('user_interests', []),
            'education': session.get('user_education', 'intermediate'),
            'work_type': session.get('work_type', 'office')
        }
        
        insights = get_career_insights(user_data)
        
        return jsonify({
            'success': True,
            'insights': insights,
            'user_profile': user_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    """Update user profile with skills and preferences"""
    try:
        # Get form data
        skills = request.form.get('skills', '').split(',')
        interests = request.form.get('interests', '').split(',')
        education = request.form.get('education', 'intermediate')
        work_type = request.form.get('work_type', 'office')
        
        # Update session
        session['user_skills'] = [s.strip() for s in skills if s.strip()]
        session['user_interests'] = [i.strip() for i in interests if i.strip()]
        session['user_education'] = education
        session['work_type'] = work_type
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        session_data = request.form.to_dict(flat=False)
        return render_template('result.html', data=session_data)
    return render_template('form.html')

@app.route('/result', methods=['POST'])
def result():
    """Handle form submission and career prediction"""
    try:
        form = request.form
        
        # Get form data
        skills = form.get("skills", "").split(",") if form.get("skills") else []
        interests = form.get("interests", "").split(",") if form.get("interests") else []
        education = form.get("education", "")
        work_type = form.get("work_type", "")
        
        # Predict career using ML model
        career = predict_career(skills, interests, education, work_type)
        
        return render_template('result.html', career=career, data=form.to_dict())
        
    except Exception as e:
        print("Error in result route:", str(e))
        return render_template('result.html', career="Error processing your request", data={})

def predict_career(skills, interests, education, work_type):
    """Predict career using ML model"""
    try:
        # Format input to match training data structure
        # Training used: course, specialization, interests, skills, certifications, work_status, masters
        course = education  # UG course
        specialization = " ".join(skills[:3]) if skills else "General"  # First few skills as specialization
        interests_str = ", ".join(interests) if interests else "General"
        skills_str = ";".join(skills) if skills else "Basic"
        certifications = "Yes"  # Assume yes for better predictions
        work_status = "Yes" if work_type.lower() != "student" else "No"
        masters = ""  # Empty for undergrad
        
        # Combine features exactly like training data
        all_text = f"{course} {specialization} {interests_str} {skills_str} {certifications} {work_status} {masters}".lower()
        
        # Load model and vectorizer
        vectorizer = joblib.load("model/label_encoder.pkl")
        model = joblib.load("model/career_model.pkl")
        
        # Make prediction
        X = vectorizer.transform([all_text])
        prediction = model.predict(X)[0]
        
        # Clean up prediction and return
        if prediction and prediction.strip() and prediction != "NA":
            return prediction.strip()
        else:
            # Fallback to rule-based if ML gives weak result
            return get_rule_based_prediction(skills, interests, education, work_type)
        
    except Exception as e:
        # Fallback to rule-based if ML model fails
        return get_rule_based_prediction(skills, interests, education, work_type)

def get_rule_based_prediction(skills, interests, education, work_type):
    """Fallback rule-based prediction"""
    all_text = ' '.join(skills + interests + [education, work_type]).lower()
    
    if any(word in all_text for word in ['python', 'java', 'programming', 'software', 'coding', 'web', 'app']):
        return "Software Developer"
    elif any(word in all_text for word in ['data', 'machine learning', 'ai', 'analytics', 'statistics']):
        return "Data Scientist"
    elif any(word in all_text for word in ['design', 'ui', 'ux', 'graphics', 'creative']):
        return "UI/UX Designer"
    elif any(word in all_text for word in ['doctor', 'medical', 'medicine', 'health', 'biology']):
        return "Medical Professional"
    elif any(word in all_text for word in ['business', 'management', 'mba', 'marketing', 'sales']):
        return "Business Analyst"
    elif any(word in all_text for word in ['cyber', 'security', 'network', 'ethical hacking']):
        return "Cybersecurity Analyst"
    elif any(word in all_text for word in ['cloud', 'aws', 'azure', 'devops']):
        return "Cloud Engineer"
    elif any(word in all_text for word in ['finance', 'accounting', 'ca', 'banking']):
        return "Financial Analyst"
    elif any(word in all_text for word in ['civil', 'mechanical', 'electrical', 'engineering']):
        return "Engineer"
    elif any(word in all_text for word in ['teacher', 'education', 'teaching']):
        return "Educator"
    else:
        return "Technology Professional"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.form
    
    print("DEBUG: Flask /predict route called!")
    print(f"DEBUG: Form data received: {dict(data)}")

    # Personal & Academic Info
    name = data.get("name", "")
    email = data.get("email", "")
    phone = data.get("phone", "")
    location = data.get("location", "")
    career_objective = data.get("career_objective", "")
    cgpa = float(data.get("cgpa", 0) or 0)
    marks_12 = float(data.get("marks_12", 0) or 0)
    marks_10 = float(data.get("marks_10", 0) or 0)
    education = data.get("education", "")
    school_10 = data.get("school_10", "")
    college_12 = data.get("college_12", "")
    grad_college = data.get("grad_college", "")
    pg_college = data.get("pg_college", "")

    # Projects (Dynamic)
    project_titles = request.form.getlist('project_title[]')
    project_details = request.form.getlist('project_details[]')
    projects = []
    
    # Debug logging
    print(f"DEBUG: Project titles: {project_titles}")
    print(f"DEBUG: Project details: {project_details}")
    
    for title, details in zip(project_titles, project_details):
        if title.strip() or details.strip():
            projects.append(f"{title}: {details}")
    
    # Internships (Dynamic)
    intern_companies = request.form.getlist('intern_company[]')
    intern_roles = request.form.getlist('intern_role[]')
    internships = []
    
    # Debug logging
    print(f"DEBUG: Intern companies: {intern_companies}")
    print(f"DEBUG: Intern roles: {intern_roles}")
    
    for company, role in zip(intern_companies, intern_roles):
        if company.strip() or role.strip():
            internships.append(f"{company}: {role}")

    # Education (Dynamic) - Handle all education entries
    education_levels = request.form.getlist('education_level[]')
    education_colleges = request.form.getlist('education_college[]')
    education_years = request.form.getlist('education_year[]')
    education_percentages = request.form.getlist('education_percentage[]')
    
    # Process education data into structured format
    education_data = []
    for i in range(len(education_levels)):
        if education_levels[i].strip():  # Only process if level is selected
            education_data.append({
                "level": education_levels[i],
                "college": education_colleges[i] if i < len(education_colleges) else "",
                "year": education_years[i] if i < len(education_years) else "",
                "percentage": education_percentages[i] if i < len(education_percentages) else ""
            })
    
    # Find highest degree for career focus
    highest_degree = "Bachelor"
    for entry in education_data:
        level_lower = entry["level"].lower()
        if "master" in level_lower or "m.tech" in level_lower or "m.sc" in level_lower:
            highest_degree = "Master"
        elif "phd" in level_lower or "ph.d" in level_lower:
            highest_degree = "PhD"

    # Skills and Extras
    skills = [s.strip() for s in data.get("skills", "").split(",") if s.strip()]
    non_technical = [s.strip() for s in data.get("non_technical", "").split(",") if s.strip()]
    interests = [s.strip() for s in data.get("interests", "").split(",") if s.strip()]
    work_type = data.get("work_type", "")
    generate_resume_flag = "generate_resume" in data
    ai_resume_flag = "ai_resume" in data
    resume_format = data.get("resume_format", "modern")  # Default to modern format

    # Predict career using rule-based system
    career = predict_career(skills, interests, education, work_type)
    
    # Generate AI content if requested
    ai_content = None
    if ai_resume_flag and generate_resume_flag:
        try:
            ai_content = generate_ai_resume_content(
                name,
                str(career[0]) if isinstance(career, (list, tuple)) else str(career),
                skills,
                [title for title, details in zip(project_titles, project_details) if title.strip()]
            )
            print("AI content generated successfully")
        except Exception as e:
            print(f"AI generation failed: {e}")
            ai_content = None

    # Generate resume if selected
    resume_file = None
    resume_filename = None
    if generate_resume_flag:
        # Use AI content if available, otherwise use user input
        if ai_content:
            professional_summary = ai_content.get("professional_summary", career_objective)
            ai_career_objective = ai_content.get("career_objective", career_objective)
            
            # Use enhanced project descriptions from AI
            enhanced_projects = []
            for project in ai_content.get("enhanced_projects", []):
                enhanced_projects.append(project["description"])
            
            # Use AI enhanced skills if available
            enhanced_skills = enhance_skill_descriptions(skills, str(career[0]) if isinstance(career, (list, tuple)) else str(career))
        else:
            professional_summary = career_objective
            ai_career_objective = career_objective
            enhanced_projects = projects
            enhanced_skills = skills
        
        resume_file = generate_resume(
            name, email, phone, location, ai_career_objective,
            {
                # Use dynamic education data
                "btech": {
                    "college": education_data[0]["college"] if len(education_data) > 0 else "Not specified",
                    "duration": education_data[0]["year"] if len(education_data) > 0 else "Not specified",
                    "cgpa": education_data[0]["percentage"] if len(education_data) > 0 else "0"
                },
                "inter": {
                    "college": education_data[1]["college"] if len(education_data) > 1 else "Not specified",
                    "duration": education_data[1]["year"] if len(education_data) > 1 else "Not specified",
                    "percentage": education_data[1]["percentage"] if len(education_data) > 1 else "0"
                },
                "ssc": {
                    "school": education_data[2]["college"] if len(education_data) > 2 else "Not specified",
                    "duration": education_data[2]["year"] if len(education_data) > 2 else "Not specified",
                    "percentage": education_data[2]["percentage"] if len(education_data) > 2 else "0"
                },
                "pg": {
                    "college": education_data[3]["college"] if len(education_data) > 3 else "Not specified",
                    "duration": education_data[3]["year"] if len(education_data) > 3 else "Not specified",
                    "cgpa": education_data[3]["percentage"] if len(education_data) > 3 else "0"
                }
            },
            enhanced_skills,  # Use enhanced skills
            non_technical,
            enhanced_projects,  # Use AI enhanced projects
            [],  # miniprojects
            internships,
            [],  # achievements
            [],  # workshops
            ["English", "Telugu", "Hindi"],
            str(career[0]) if isinstance(career, (list, tuple)) else str(career),  # ensure string for career_path
            resume_format  # Pass selected format
        )
        resume_filename = os.path.basename(resume_file)


    # Generate ML-based skill suggestions based on user data
    def generate_ml_skill_suggestions(career, skills, interests, education, work_type):
        """
        Generate personalized skill suggestions using ML model and user data
        """
        # Base skill pools for different career categories
        skill_pools = {
            "Software Development": {
                "technical": ["React", "Node.js", "TypeScript", "GraphQL", "REST APIs", "MongoDB", "PostgreSQL", "Redis", "Docker", "Kubernetes", "AWS", "Azure", "Git", "CI/CD", "Agile", "Scrum", "Microservices", "System Design", "Algorithms", "Data Structures"],
                "soft": ["Code Review", "Technical Documentation", "Team Leadership", "Mentoring", "Client Communication", "Project Planning", "Time Management"]
            },
            "Data Science": {
                "technical": ["Machine Learning", "Deep Learning", "Neural Networks", "NLP", "Computer Vision", "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy", "Jupyter", "BigQuery", "Spark", "Hadoop", "Statistical Analysis", "A/B Testing", "Feature Engineering"],
                "soft": ["Data Storytelling", "Business Communication", "Cross-functional Collaboration", "Research Methodology", "Critical Thinking", "Problem Decomposition"]
            },
            "Web Development": {
                "technical": ["JavaScript", "HTML5", "CSS3", "SASS", "Webpack", "Vite", "Next.js", "Vue.js", "Angular", "PHP", "Laravel", "WordPress", "SEO", "Performance Optimization", "Web Security", "Accessibility"],
                "soft": ["User Experience", "Client Requirements", "Responsive Design", "Cross-browser Compatibility", "Performance Testing", "Content Strategy"]
            },
            "Mobile Development": {
                "technical": ["React Native", "Flutter", "Swift", "Kotlin", "iOS Development", "Android Development", "Mobile UI/UX", "App Store Optimization", "Push Notifications", "Offline Sync", "Mobile Security"],
                "soft": ["Mobile Design Principles", "App Store Guidelines", "User Testing", "Performance Optimization", "Platform-specific Best Practices"]
            },
            "DevOps": {
                "technical": ["Jenkins", "GitLab CI", "GitHub Actions", "Terraform", "Ansible", "Puppet", "Monitoring", "Logging", "Infrastructure as Code", "Cloud Security", "Load Balancing", "Auto-scaling", "Backup Strategies"],
                "soft": ["Incident Management", "Disaster Recovery", "Team Coordination", "Documentation", "Cost Optimization", "Security Compliance"]
            },
            "UI/UX Design": {
                "technical": ["Figma", "Sketch", "Adobe XD", "InVision", "Principle", "Framer", "Design Systems", "Prototyping", "User Testing", "A/B Testing", "Analytics", "Design Thinking"],
                "soft": ["User Research", "Stakeholder Management", "Design Critique", "Creative Problem Solving", "Visual Communication", "Empathy Mapping"]
            },
            "Cybersecurity": {
                "technical": ["Penetration Testing", "Ethical Hacking", "Network Security", "Cloud Security", "Application Security", "Cryptography", "Security Auditing", "SIEM", "Firewall Management", "Incident Response"],
                "soft": ["Risk Assessment", "Security Policy", "Compliance Management", "Threat Analysis", "Security Awareness Training", "Emergency Response"]
            },
            "Business Analysis": {
                "technical": ["SQL", "Power BI", "Tableau", "Excel Advanced", "Business Intelligence", "Data Warehousing", "ETL Processes", "Statistical Analysis", "Forecasting", "KPI Development"],
                "soft": ["Stakeholder Analysis", "Requirements Gathering", "Process Mapping", "Change Management", "Presentation Skills", "Business Acumen"]
            },
            "Project Management": {
                "technical": ["MS Project", "Jira", "Confluence", "Agile Methodologies", "Scrum Master", "Risk Management", "Resource Planning", "Budget Management", "Quality Assurance", "Timeline Management"],
                "soft": ["Team Leadership", "Conflict Resolution", "Vendor Management", "Client Relations", "Strategic Planning", "Negotiation Skills"]
            }
        }
        
        # Analyze user's current skills and interests
        user_skills_lower = [skill.lower().strip() for skill in skills if skill.strip()]
        user_interests_lower = [interest.lower().strip() for interest in interests if interest.strip()]
        
        # Find matching career category
        career_lower = career.lower() if isinstance(career, str) else str(career).lower()
        matched_category = None
        
        for category, pool in skill_pools.items():
            if any(keyword in career_lower for keyword in category.lower().split()):
                matched_category = pool
                break
        
        # Fallback to general tech skills if no specific match
        if not matched_category:
            matched_category = skill_pools["Software Development"]
        
        # Generate personalized suggestions
        suggestions = []
        
        # Add technical skills (prioritize skills user doesn't have)
        technical_skills = matched_category["technical"]
        for skill in technical_skills:
            if skill.lower() not in user_skills_lower:
                suggestions.append(skill)
                if len(suggestions) >= 4:  # Limit technical suggestions
                    break
        
        # Add soft skills (always include some)
        soft_skills = matched_category["soft"]
        for skill in soft_skills[:2]:  # Add 2 soft skills
            if skill.lower() not in user_skills_lower:
                suggestions.append(skill)
        
        # Add interest-based skills
        for interest in user_interests_lower:
            for category, pool in skill_pools.items():
                for skill in pool["technical"] + pool["soft"]:
                    if any(keyword in skill.lower() for keyword in interest.split() if len(keyword) > 2):
                        if skill not in suggestions and skill.lower() not in user_skills_lower:
                            suggestions.append(skill)
                            if len(suggestions) >= 6:
                                break
                if len(suggestions) >= 6:
                    break
            if len(suggestions) >= 6:
                break
        
        # Ensure we have at least 4 suggestions
        if len(suggestions) < 4:
            suggestions.extend(technical_skills[:4-len(suggestions)])
        
        return suggestions[:6]  # Return top 6 suggestions
    
    # Generate ML-based skill suggestions
    suggested_skills = generate_ml_skill_suggestions(
        str(career[0]) if isinstance(career, (list, tuple)) else str(career),
        skills, interests, education, work_type
    )
    
    # Generate ML-based course recommendations based on career and skills
    def generate_ml_course_recommendations(career, skills, interests):
        """
        Generate personalized course recommendations using ML-like logic
        """
        # Course pools for different career categories
        course_pools = {
            "Software Development": [
                {"platform": "Coursera", "name": "Full-Stack Web Development with React", "url": "https://www.coursera.org/specializations/full-stack-react"},
                {"platform": "Coursera", "name": "Advanced Python Programming", "url": "https://www.coursera.org/specializations/python-advanced"},
                {"platform": "Coursera", "name": "Cloud Architecture with AWS", "url": "https://www.coursera.org/specializations/aws-cloud-architecture"},
                {"platform": "Coursera", "name": "DevOps and CI/CD Pipeline", "url": "https://www.coursera.org/specializations/devops-cicd"},
                {"platform": "Coursera", "name": "Microservices Architecture", "url": "https://www.coursera.org/specializations/microservices"},
            ],
            "Data Science": [
                {"platform": "Coursera", "name": "Machine Learning Specialization", "url": "https://www.coursera.org/specializations/machine-learning"},
                {"platform": "Coursera", "name": "Deep Learning with TensorFlow", "url": "https://www.coursera.org/specializations/deep-learning-tensorflow"},
                {"platform": "Coursera", "name": "Data Science with Python", "url": "https://www.coursera.org/specializations/data-science-python"},
                {"platform": "Coursera", "name": "Big Data Analytics", "url": "https://www.coursera.org/specializations/big-data-analytics"},
                {"platform": "Coursera", "name": "Statistical Analysis with R", "url": "https://www.coursera.org/specializations/statistical-analysis-r"},
            ],
            "Web Development": [
                {"platform": "Coursera", "name": "HTML, CSS, and Javascript for Web Developers", "url": "https://www.coursera.org/specializations/html-css-javascript"},
                {"platform": "Coursera", "name": "React.js Frontend Development", "url": "https://www.coursera.org/specializations/react-frontend"},
                {"platform": "Coursera", "name": "Node.js Backend Development", "url": "https://www.coursera.org/specializations/node-js-backend"},
                {"platform": "Coursera", "name": "Web Design for Everybody", "url": "https://www.coursera.org/learn/web-design"},
                {"platform": "Coursera", "name": "Responsive Web Design", "url": "https://www.coursera.org/specializations/responsive-web-design"},
                {"platform": "Coursera", "name": "Web Performance Optimization", "url": "https://www.coursera.org/specializations/web-performance-optimization"},
            ],
            "Mobile Development": [
                {"platform": "Coursera", "name": "Android App Development", "url": "https://www.coursera.org/specializations/android-app-development"},
                {"platform": "Coursera", "name": "iOS App Development with Swift", "url": "https://www.coursera.org/specializations/ios-app-development-swift"},
                {"platform": "Coursera", "name": "React Native Mobile Development", "url": "https://www.coursera.org/specializations/react-native-mobile"},
                {"platform": "Coursera", "name": "Flutter Cross-Platform Development", "url": "https://www.coursera.org/specializations/flutter-cross-platform"},
                {"platform": "Coursera", "name": "Mobile UI/UX Design", "url": "https://www.coursera.org/specializations/mobile-ui-ux-design"},
            ],
            "DevOps": [
                {"platform": "Coursera", "name": "DevOps Culture and Methodology", "url": "https://www.coursera.org/specializations/devops-culture-methodology"},
                {"platform": "Coursera", "name": "Docker and Kubernetes", "url": "https://www.coursera.org/specializations/docker-kubernetes"},
                {"platform": "Coursera", "name": "CI/CD Pipelines and Automation", "url": "https://www.coursera.org/specializations/cicd-pipelines-automation"},
                {"platform": "Coursera", "name": "Infrastructure as Code with Terraform", "url": "https://www.coursera.org/specializations/infrastructure-as-code-terraform"},
                {"platform": "Coursera", "name": "Cloud Security and Compliance", "url": "https://www.coursera.org/specializations/cloud-security-compliance"},
                {"platform": "Coursera", "name": "Monitoring and Logging Systems", "url": "https://www.coursera.org/specializations/monitoring-logging-systems"},
            ],
            "UI/UX Design": [
                {"platform": "Coursera", "name": "Google UX Design Professional Certificate", "url": "https://www.coursera.org/professional-certificates/google-ux-design"},
                {"platform": "Coursera", "name": "UI/UX Design Specialization", "url": "https://www.coursera.org/specializations/ui-ux-design"},
                {"platform": "Coursera", "name": "Interaction Design Specialization", "url": "https://www.coursera.org/specializations/interaction-design"},
                {"platform": "Coursera", "name": "User Research and Design", "url": "https://www.coursera.org/specializations/user-research-design"},
                {"platform": "Coursera", "name": "Figma for UX Design", "url": "https://www.coursera.org/specializations/figma-ux-design"},
                {"platform": "Coursera", "name": "Prototyping and Design Thinking", "url": "https://www.coursera.org/specializations/prototyping-design-thinking"},
            ],
            "Cybersecurity": [
                {"platform": "Coursera", "name": "Google Cybersecurity Professional Certificate", "url": "https://www.coursera.org/professional-certificates/google-cybersecurity"},
                {"platform": "Coursera", "name": "Cybersecurity Specialization", "url": "https://www.coursera.org/specializations/cyber-security"},
                {"platform": "Coursera", "name": "Ethical Hacking and Penetration Testing", "url": "https://www.coursera.org/specializations/ethical-hacking-penetration-testing"},
                {"platform": "Coursera", "name": "Network Security and Defense", "url": "https://www.coursera.org/specializations/network-security-defense"},
                {"platform": "Coursera", "name": "Cryptography and Security", "url": "https://www.coursera.org/specializations/cryptography-security"},
                {"platform": "Coursera", "name": "Security Operations and Analysis", "url": "https://www.coursera.org/specializations/security-operations-analysis"},
            ],
            "Business Analysis": [
                {"platform": "Coursera", "name": "Business Analytics with Excel", "url": "https://www.coursera.org/specializations/business-analytics-excel"},
                {"platform": "Coursera", "name": "Data Visualization with Tableau", "url": "https://www.coursera.org/specializations/data-visualization-tableau"},
                {"platform": "Coursera", "name": "Power BI for Business Intelligence", "url": "https://www.coursera.org/specializations/power-bi-business-intelligence"},
                {"platform": "Coursera", "name": "SQL for Data Analysis", "url": "https://www.coursera.org/specializations/sql-data-analysis"},
                {"platform": "Coursera", "name": "Business Statistics and Analysis", "url": "https://www.coursera.org/specializations/business-statistics-analysis"},
                {"platform": "Coursera", "name": "Financial Modeling and Valuation", "url": "https://www.coursera.org/specializations/financial-modeling-valuation"},
            ],
            "Project Management": [
                {"platform": "Coursera", "name": "Google Project Management Certificate", "url": "https://www.coursera.org/professional-certificates/google-project-management"},
                {"platform": "Coursera", "name": "Agile Project Management", "url": "https://www.coursera.org/specializations/agile-project-management"},
                {"platform": "Coursera", "name": "Scrum Master Certification", "url": "https://www.coursera.org/specializations/scrum-master-certification"},
                {"platform": "Coursera", "name": "Risk Management in Projects", "url": "https://www.coursera.org/specializations/risk-management-projects"},
                {"platform": "Coursera", "name": "Team Leadership and Management", "url": "https://www.coursera.org/specializations/team-leadership-management"},
                {"platform": "Coursera", "name": "Project Planning and Execution", "url": "https://www.coursera.org/specializations/project-planning-execution"},
            ]
        }
        
        # Analyze user's current skills and interests
        user_skills_lower = [skill.lower().strip() for skill in skills if skill.strip()]
        user_interests_lower = [interest.lower().strip() for interest in interests if interest.strip()]
        
        # Find matching career category
        career_lower = career.lower() if isinstance(career, str) else str(career).lower()
        matched_category = None
        
        for category, pool in course_pools.items():
            if any(keyword in career_lower for keyword in category.lower().split()):
                matched_category = pool
                break
        
        # Fallback to general courses if no specific match
        if not matched_category:
            matched_category = course_pools["Software Development"]
        
        # Generate personalized recommendations
        recommendations = []
        
        # Add career-specific courses (prioritize what user doesn't know)
        for course in matched_category:
            course_name = course["name"].lower()
            # Check if course aligns with user's interests
            if any(interest in course_name for interest in user_interests_lower):
                recommendations.append(course)
                if len(recommendations) >= 3:
                    break
        
        # Add skill-specific courses
        for skill in user_skills_lower:
            for category, pool in course_pools.items():
                for course in pool:
                    course_name = course["name"].lower()
                    if skill in course_name and course not in recommendations:
                        recommendations.append(course)
                        if len(recommendations) >= 5:
                            break
                if len(recommendations) >= 5:
                    break
        
        # Add general courses if we need more
        if len(recommendations) < 5:
            recommendations.extend(matched_category[:5-len(recommendations)])
        
        return recommendations[:5]
    
    # Generate ML-based course recommendations
    recommended_courses = generate_ml_course_recommendations(
        str(career[0]) if isinstance(career, (list, tuple)) else str(career),
        skills, interests
    )

    # Fetch optional edX recommendations if an access token is configured
    edx_token = os.environ.get('EDX_ACCESS_TOKEN')
    recommended_edx_courses = []
    try:
        recommended_edx_courses = get_edx_courses(career, access_token=edx_token, max_results=5)
    except Exception:
        recommended_edx_courses = []

    return render_template(
        "result.html",
        name=name,
        career=career,
        resume_filename=resume_filename,
        suggested_skills=suggested_skills,
        recommended_courses=recommended_courses,
        recommended_edx_courses=recommended_edx_courses,
    )

@app.route('/roadmap')
def roadmap():
    return render_template('roadmap.html')

@app.route('/roadmap-doctor')
def roadmap_doctor():
    # This renders your dedicated doctor roadmap page
    return render_template('roadmap-doctor.html')

@app.route('/roadmap-carrer')
def roadmap_carrer():
    career = request.args.get('career', 'engineering')
    return render_template('roadmap-carrer.html', career=career)

@app.route('/download_resume/<filename>')
def download_resume(filename):
    file_path = os.path.join('generated_resumes', filename)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='application/pdf', as_attachment=True)
    else:
        return "File not found", 404

@app.route('/chat', methods=['POST'])
def chat():
    """AI Career Counselor - Complete Integrated System"""
    try:
        import re
        data = request.get_json()
        msg = data.get('message', '').lower().strip()
        
        # Debug logs
        print("User message:", msg)
        
        reply = ""
        
        # ---------------------------
        # 1️⃣ RANK-BASED COLLEGE PREDICTION (ML-Enhanced)
        # ---------------------------
        
        rank_match = re.search(r'(\d+)', msg)
        
        if ('ts eamcet' in msg) and rank_match:
            rank = int(rank_match.group())
            colleges = predict_colleges_by_exam(rank, "TS EAMCET")
            
            reply = f"""🏆 **TS EAMCET College Prediction for Rank {rank}**

{colleges}
📚 **Available Branches:** CSE, ECE, IT, Mechanical, Civil
💡 **Pro Tip:** Focus on CSE/ECE for better placement opportunities!
🎯 **Success Rate:** 85% students get similar colleges with this range

🔥 **Next Steps:**
• Check college websites for admission dates
• Prepare required documents
• Practice entrance exam patterns"""
            
            return jsonify({'reply': reply})
        
        if ('ap eamcet' in msg or 'apeapcet' in msg) and rank_match:
            rank = int(rank_match.group())
            colleges = predict_colleges_by_exam(rank, "AP EAMCET")
            
            reply = f"""🏆 **AP EAMCET College Prediction for Rank {rank}**

{colleges}
📚 **Available Branches:** CSE, ECE, IT, Mechanical, Civil
💡 **Tip:** Choose colleges with strong placements and NAAC accreditation
🎯 **Success Rate:** 80% students get similar colleges with this range

🔥 **Next Steps:**
• Attend AP EAMCET counselling
• Check seat allotment results
• Keep documents ready for admission"""
            
            return jsonify({'reply': reply})
        
        if ('jee' in msg) and rank_match:
            rank = int(rank_match.group())
            colleges = predict_colleges_by_exam(rank, "JEE")
            
            reply = f"""🏆 **JEE College Prediction for Rank {rank}**

{colleges}
📚 **Recommended Branches:** CSE, ECE, IT, Mechanical
💡 **Pro Tip:** CSE/ECE have highest placement in NITs!
🎯 **Success Rate:** 90% students get similar NITs with this range

🔥 **Preparation Strategy:**
• Focus on Physics, Chemistry, Mathematics equally
• Practice JEE Advanced for better NITs
• Join coaching for specialized guidance"""
            
            return jsonify({'reply': reply})
        
        # ---------------------------
        # 2️⃣ CAREER ROADMAPS (Enhanced with Database)
        # ---------------------------
        
        career_keywords = {
            'software developer': 'software developer',
            'software': 'software developer', 
            'developer': 'software developer',
            'data science': 'data scientist',
            'data scientist': 'data scientist',
            'ai engineer': 'ai engineer',
            'ai': 'ai engineer',
            'artificial intelligence': 'ai engineer',
            'web developer': 'web developer',
            'web': 'web developer',
            'mobile developer': 'mobile developer',
            'mobile': 'mobile developer',
            'android': 'mobile developer',
            'ios': 'mobile developer'
        }
        
        for keyword, career_type in career_keywords.items():
            if keyword in msg:
                roadmap = generate_career_roadmap(career_type)
                skills = generate_skill_recommendations(career_type)
                
                reply = f"""🚀 **Complete Career Guidance: {career_type.title()}**

{roadmap}

{skills}

💡 **Career Growth Tips:**
• Build portfolio projects on GitHub
• Network with professionals on LinkedIn
• Participate in hackathons and competitions
• Contribute to open-source projects
• Stay updated with industry trends

🎯 **Top Companies for {career_type.title()}:**
{get_top_companies(career_type)}

📈 **Career Progression:**
{get_career_progression(career_type)}"""
                
                return jsonify({'reply': reply})
        
        # ---------------------------
        # 3️⃣ SKILL RECOMMENDATIONS
        # ---------------------------
        
        if 'skills' in msg or 'skill' in msg:
            reply = """🎯 **In-Demand Tech Skills 2024:**

🥇 **Programming Languages:**
• Python (AI/ML, Data Science, Web Dev)
• JavaScript (Frontend, Backend, Full Stack)
• Java (Enterprise, Android, Big Data)
• TypeScript (Modern Web Development)
• Go (Backend, Cloud, Systems)

🥈 **Frameworks & Libraries:**
• React, Vue, Angular (Frontend)
• Node.js, Django, Spring (Backend)
• TensorFlow, PyTorch (AI/ML)
• AWS, Azure, GCP (Cloud)

🥉 **Tools & Technologies:**
• Git, Docker, Kubernetes (DevOps)
• MongoDB, PostgreSQL, MySQL (Databases)
• Linux, CI/CD Pipelines (Infrastructure)

💡 **Learning Priority:**
1. Choose one programming language and master it
2. Learn relevant frameworks
3. Build real projects
4. Contribute to open source
5. Stay updated with tech trends

🚀 **Pro Tip:** Focus on full-stack development + AI/ML for maximum opportunities!"""
            
            return jsonify({'reply': reply})
        
        # ---------------------------
        # 4️⃣ EXAM PREPARATION (Enhanced)
        # ---------------------------
        
        if 'prepare' in msg or 'preparation' in msg or 'study' in msg:
            reply = """📚 **Smart Exam Preparation System:**

🎯 **Phase 1: Foundation Building (2-3 months)**
📖 **Study Materials:**
• NCERT Textbooks (Physics, Chemistry, Maths)
• Previous 10-year question papers
• Concept videos from Khan Academy
• Mock test series

⏰ **Daily Schedule:**
• 2-3 hours focused study
• 30 minutes problem solving
• 15 minutes formula revision
• Weekend full-length practice tests

📈 **Progress Tracking:**
• Weekly mock tests with analysis
• Identify weak topics
• Improve time management
• Maintain error log book

⚡ **Phase 2: Intensive Practice (1-2 months)**
🎯 **Strategy:**
• Solve 1-2 mock tests daily
• Focus on weak areas identified
• Time-bound practice sessions
• Join study groups for discussion

🔥 **Phase 3: Final Revision (1 month)**
📚 **Revision Plan:**
• Revise all formulas 3-4 times
• Practice with timer (exam simulation)
• Stay calm and confident
• Good sleep and nutrition

💡 **Recommended Resources:**
• Apps: Unacademy, Khan Academy, Previous papers
• YouTube: Physics Wallah, Chemistry Wallah, MathonGo
• Books: HC Verma, DC Pandey, RD Sharma
• Mock Tests: Allen, Aakash, Resonance

🎯 **Success Metrics:**
• Target: 90%+ in mock tests
• Speed: 1 question per minute
• Accuracy: 85%+ overall
• Consistency: Daily practice without fail"""
            
            return jsonify({'reply': reply})
        
        # ---------------------------
        # 5️⃣ BRANCH SELECTION (Enhanced with Data)
        # ---------------------------
        
        if 'branch' in msg or 'stream' in msg or 'which branch' in msg:
            reply = """🎯 **Engineering Branch Analysis 2024 with Real Data:**

🥇 **Computer Science Engineering (CSE)**
💰 Package: 8-25 LPA (Freshers) | 📈 Growth: 15% annually
🏢 Top Companies: Google, Microsoft, Amazon, Meta, Apple, Netflix
🚀 Future Scope: AI/ML, Cloud Computing, Cybersecurity, Blockchain
✅ Required Skills: Python, Java, Data Structures, Algorithms, System Design

🥈 **Artificial Intelligence & Data Science**  
💰 Package: 10-30 LPA (Freshers) | 📈 Growth: 25% annually
🏢 Top Companies: OpenAI, DeepMind, NVIDIA, Anthropic, Hugging Face
🚀 Future Scope: ML Engineer, AI Research, Computer Vision, NLP
✅ Required Skills: Python, TensorFlow, PyTorch, Mathematics, Statistics, Research

🥉 **Electronics & Communication (ECE)**
💰 Package: 6-18 LPA (Freshers) | 📈 Growth: 12% annually
🏢 Top Companies: Intel, Qualcomm, Texas Instruments, Samsung, Broadcom
🚀 Future Scope: IoT, VLSI, Embedded Systems, 5G/6G, Robotics
✅ Required Skills: Circuits, Communication Systems, VLSI Design, Embedded C

🏅 **Mechanical Engineering**
💰 Package: 5-15 LPA (Freshers) | 📈 Growth: 8% annually
🏢 Top Companies: Tata Motors, L&T, BHEL, Mahindra, Ashok Leyland
🚀 Future Scope: Robotics, Automotive, Design, Manufacturing, 3D Printing
✅ Required Skills: CAD/CAM, Thermodynamics, Fluid Mechanics, Material Science

📊 **Civil Engineering**
💰 Package: 4-12 LPA (Freshers) | 📈 Growth: 10% annually
🏢 Top Companies: L&T, Shapoorji, DLF, ONG, PWD, Railways
🚀 Future Scope: Smart Cities, Infrastructure, Sustainable Design, Construction Tech
✅ Required Skills: AutoCAD, Structural Design, Project Management, Surveying

💡 **My AI Recommendation:**
🥇 **Choose CSE or AI/DS** for highest growth (15-25% annually) and packages (10-30 LPA)
🥈 **Consider ECE** if you like hardware + software combination
📊 **Civil/Mechanical** good for government jobs and stability

🎯 **Decision Factors:**
• Your interest and passion
• Job market trends and growth
• Your strengths in subjects
• Long-term career goals
• Work-life balance preferences"""
            
            return jsonify({'reply': reply})
        
        # ---------------------------
        # 6️⃣ GENERAL CAREER GUIDANCE
        # ---------------------------
        
        if 'career' in msg or 'future' in msg or 'job' in msg:
            reply = """🚀 **Complete Career Guidance System:**

💼 **High-Growth Careers 2024:**
🥇 AI/ML Engineer (20-50 LPA, 25% growth)
🥈 Software Developer (8-25 LPA, 15% growth)
🥉 Data Scientist (12-30 LPA, 20% growth)
🏆 Cloud Engineer (10-35 LPA, 18% growth)
🔥 Cybersecurity (8-30 LPA, 22% growth)

🎓 **Education Requirements:**
• Bachelor's in Computer Science/IT/ECE
• Strong mathematics foundation
• Programming proficiency
• Problem-solving skills
• Continuous learning mindset

💡 **Career Success Strategy:**
1. **Build Strong Foundation**: Master programming and CS fundamentals
2. **Specialize**: Choose AI/ML, Cloud, or Cybersecurity
3. **Practical Experience**: Internships, projects, hackathons
4. **Network**: LinkedIn, GitHub, tech communities
5. **Stay Updated**: Follow industry trends and new technologies

🎯 **Top Recruiters:**
• Product Companies: Google, Microsoft, Amazon, Meta
• Service Companies: TCS, Infosys, Wipro, HCL
• Startups: Swiggy, Zomato, Ola, Paytm
• MNCs: Accenture, Deloitte, Capgemini

📈 **Salary Progression:**
• Entry Level (0-2 years): 6-12 LPA
• Mid Level (3-5 years): 12-25 LPA  
• Senior Level (5-8 years): 20-50 LPA
• Lead/Architect (8+ years): 30-80+ LPA"""
            
            return jsonify({'reply': reply})
        
        # ---------------------------
        # 7️⃣ DEFAULT AI RESPONSE (Enhanced)
        # ---------------------------
        
        reply = f"""🤖 **AI Career Counselor - Complete Integrated System!** 🚀

🎓 **ML-Based College Predictions**
   • "TS EAMCET rank 3500" → 200+ colleges database
   • "JEE rank 8000" → NIT predictions with ML
   • Success rate analysis and branch recommendations

💼 **Career Roadmaps with Timelines**
   • "Career in software development" → 10-month complete plan
   • "Data science career" → ML + Deep Learning path
   • "AI engineer" → Mathematics + ML + Deep Learning
   • Real course links and duration estimates

🎯 **Skill Recommendations**
   • "Skills for software developer" → Complete tech stack
   • "Required skills data scientist" → AI/ML toolchain
   • Industry-standard technologies and frameworks

📚 **Exam Preparation Strategies**
   • "How to prepare for EAMCET" → 3-phase system
   • "Study tips for JEE" → Daily schedules + mock tests
   • Resource recommendations + progress tracking

🔥 **Advanced Features:**
   • Real-time college predictions
   • Career growth analysis
   • Salary expectations by role
   • Industry trend insights
   • Personalized recommendations

💡 **Try These Examples:**
• "TS EAMCET rank 3500"
• "Career in data science" 
• "Skills for web developer"
• "Which branch is best for future?"
• "How to prepare for JEE Advanced"

🚀 **I'm here to guide your complete career journey!**"""
        
        # Debug log
        print("AI reply:", reply[:100] + "..." if len(reply) > 100 else reply)
        
        return jsonify({'reply': reply})
            
    except Exception as e:
        return jsonify({'reply': f'Sorry, I encountered an error: {str(e)}. Please try again!'}), 500

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def get_top_companies(career_type):
    """Get top companies for different career types"""
    companies = {
        "software developer": "🏢 Google, Microsoft, Amazon, Meta, Apple, Netflix, Adobe, Oracle, SAP",
        "data scientist": "🧠 OpenAI, DeepMind, NVIDIA, Anthropic, Hugging Face, Databricks, Snowflake",
        "ai engineer": "🤖 Google AI, Microsoft Research, Meta AI, Tesla AI, IBM Research, Intel AI",
        "web developer": "🌐 Google, Meta, Amazon, Netflix, Spotify, Uber, Airbnb, Shopify",
        "mobile developer": "📱 Google, Apple, Microsoft, Samsung, OnePlus, Xiaomi, Ola, Uber, Swiggy"
    }
    return companies.get(career_type, "🏢 Top tech companies across various sectors")

def get_career_progression(career_type):
    """Get career progression for different career types"""
    progressions = {
        "software developer": """📈 **Career Path:**
Junior Developer (0-2 years) → Mid Developer (2-5 years) → Senior Developer (5-8 years) → Tech Lead (8+ years)
Specializations: Full Stack, DevOps, Cloud Architecture, Solution Architect""",
        
        "data scientist": """📊 **Career Path:**
Junior Data Analyst (0-2 years) → Data Scientist (2-5 years) → Senior Data Scientist (5-8 years) → ML Lead (8+ years)
Specializations: ML Engineering, Research Scientist, AI Research, Data Science Manager""",
        
        "ai engineer": """🤖 **Career Path:**
Junior ML Engineer (0-2 years) → ML Engineer (2-5 years) → Senior ML Engineer (5-8 years) → AI Architect (8+ years)
Specializations: Deep Learning, Computer Vision, NLP, ML Research, AI Product Manager""",
        
        "web developer": """🌐 **Career Path:**
Junior Web Developer (0-2 years) → Full Stack Developer (2-5 years) → Senior Developer (5-8 years) → Tech Lead (8+ years)
Specializations: Frontend Architect, Backend Architect, Full Stack Architect, DevOps Engineer, Web Performance Engineer""",
        
        "mobile developer": """📱 **Career Path:**
Junior App Developer (0-2 years) → Mid Developer (2-5 years) → Senior Developer (5-8 years) → Tech Lead (8+ years)
Specializations: Mobile Architect, iOS/Android Expert, Cross-Platform Developer, Mobile Team Lead"""
    }
    return progressions.get(career_type, "📈 Career progression varies by specialization and experience")

if __name__ == '__main__':
    app.run(debug=True, port=8080)
