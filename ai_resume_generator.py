import requests
import json
import os
from typing import Dict, List

# AI API Configuration
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", "YOUR_API_KEY_HERE")

def generate_ai_resume_content(name: str, career: str, skills: List[str], projects: List[str]) -> Dict[str, str]:
    """
    Generate professional resume content using AI
    
    Args:
        name: User's full name
        career: Career path/field
        skills: List of technical skills
        projects: List of project titles
    
    Returns:
        Dictionary containing generated resume sections
    """
    
    # Prepare skills and projects for AI
    skills_text = ", ".join(skills) if skills else "Not specified"
    projects_text = ", ".join(projects) if projects else "Not specified"
    
    # Professional AI prompt for resume generation
    prompt = f"""
    You are an expert resume writer and career counselor. Generate professional resume content for:

    Name: {name}
    Career Path: {career}
    Technical Skills: {skills_text}
    Projects: {projects_text}

    Generate the following sections in a professional, ATS-friendly format:

    1. Professional Summary (3-4 lines, highlighting key strengths and career focus)
    2. Career Objective (2-3 lines, specific and goal-oriented)
    3. Enhanced Project Descriptions (convert each project title into 2-3 bullet points showing impact and technologies used)

    Format requirements:
    - Keep it professional and concise
    - Use action verbs (Developed, Built, Implemented, etc.)
    - Include technologies and measurable impacts where possible
    - Make it ATS-friendly with relevant keywords
    - Avoid generic phrases

    Return the response in this exact JSON format:
    {{
        "professional_summary": "Generated professional summary here...",
        "career_objective": "Generated career objective here...",
        "enhanced_projects": [
            {{
                "title": "Project 1 Title",
                "description": "• Bullet point 1\\n• Bullet point 2\\n• Bullet point 3"
            }},
            {{
                "title": "Project 2 Title", 
                "description": "• Bullet point 1\\n• Bullet point 2"
            }}
        ]
    }}
    """
    
    try:
        # Try Perplexity API first
        response = _call_perplexity_api(prompt)
        if response:
            return response
            
        # Fallback to mock generation if API fails
        return _generate_mock_content(name, career, skills, projects)
        
    except Exception as e:
        print(f"AI generation error: {e}")
        return _generate_mock_content(name, career, skills, projects)

def _call_perplexity_api(prompt: str) -> Dict[str, str]:
    """Call Perplexity API for content generation"""
    
    if PERPLEXITY_API_KEY == "YOUR_API_KEY_HERE":
        print("Perplexity API key not configured, using mock content")
        return None
    
    url = "https://api.perplexity.ai/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "sonar-small-online",
        "messages": [
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.3
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        
        # Parse JSON response
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            print("Failed to parse AI response as JSON")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None

def _generate_mock_content(name: str, career: str, skills: List[str], projects: List[str]) -> Dict[str, str]:
    """Generate mock AI content when API is not available"""
    
    # Professional summary based on career
    summaries = {
        "data science": f"Highly motivated Data Science professional with strong expertise in {', '.join(skills[:3]) if skills else 'data analysis'}. Passionate about leveraging machine learning and statistical analysis to drive data-driven decision making and solve complex business problems.",
        "software developer": f"Results-oriented Software Developer with proficiency in {', '.join(skills[:3]) if skills else 'full-stack development'}. Experienced in building scalable applications and delivering high-quality software solutions that meet business requirements.",
        "ai engineer": f"Innovative AI Engineer with deep knowledge of {', '.join(skills[:3]) if skills else 'machine learning and AI'}. Skilled in developing intelligent systems and deploying machine learning models to automate processes and enhance user experiences.",
        "web developer": f"Creative Web Developer with expertise in {', '.join(skills[:3]) if skills else 'modern web technologies'}. Passionate about building responsive, user-friendly web applications that deliver exceptional user experiences.",
        "default": f"Motivated {career} professional with strong technical skills and a passion for innovation. Committed to delivering high-quality solutions and continuously learning new technologies to stay current in the field."
    }
    
    professional_summary = summaries.get(career.lower(), summaries["default"])
    
    # Career objective based on career
    objectives = {
        "data science": "To secure a challenging Data Scientist position where I can apply my analytical skills and machine learning expertise to extract valuable insights and drive data-informed business decisions.",
        "software developer": "To obtain a Software Developer role that allows me to utilize my programming skills and problem-solving abilities to create innovative software solutions and contribute to technological advancement.",
        "ai engineer": "To work as an AI Engineer where I can leverage my machine learning knowledge to develop intelligent systems and contribute to cutting-edge AI initiatives.",
        "web developer": "To secure a Web Developer position where I can apply my frontend and backend skills to build engaging web applications and enhance user experiences.",
        "default": f"To pursue a challenging career as a {career} where I can apply my technical skills and contribute to organizational success while growing professionally."
    }
    
    career_objective = objectives.get(career.lower(), objectives["default"])
    
    # Enhanced project descriptions
    enhanced_projects = []
    for project in projects[:5]:  # Limit to first 5 projects
        enhanced_projects.append({
            "title": project,
            "description": f"• Developed and implemented {project} using modern technologies and best practices\n• Focused on performance optimization and user experience\n• Successfully delivered project meeting all requirements and deadlines"
        })
    
    return {
        "professional_summary": professional_summary,
        "career_objective": career_objective,
        "enhanced_projects": enhanced_projects
    }

def enhance_skill_descriptions(skills: List[str], career: str) -> List[str]:
    """Enhance skill descriptions with AI-powered context"""
    
    skill_templates = {
        "python": "Python - Advanced proficiency in data analysis, automation, and web development",
        "java": "Java - Strong object-oriented programming skills for enterprise applications",
        "sql": "SQL - Expertise in database design, querying, and optimization",
        "machine learning": "Machine Learning - Deep understanding of algorithms and model deployment",
        "react": "React - Modern frontend development with component-based architecture",
        "node.js": "Node.js - Backend development with RESTful APIs and microservices",
        "aws": "AWS - Cloud computing and scalable infrastructure management"
    }
    
    enhanced_skills = []
    for skill in skills:
        skill_lower = skill.lower().strip()
        enhanced = skill_templates.get(skill_lower, f"{skill} - Proficient in {skill} for professional applications")
        enhanced_skills.append(enhanced)
    
    return enhanced_skills

def generate_career_insights(skills: List[str], interests: List[str], education: str, cgpa: float) -> Dict[str, str]:
    """Generate AI-powered career insights and recommendations"""
    
    insights = {
        "career_match": "Based on your profile, Software Development or Data Science would be excellent career paths.",
        "skill_gaps": "Consider learning Cloud Computing (AWS/Azure) and DevOps practices to enhance your marketability.",
        "salary_range": "Entry-level positions in your field typically range from ₹6-12 LPA depending on skills and location.",
        "growth_path": "With your technical foundation, you can progress to Senior Developer → Tech Lead → Architect roles.",
        "recommended_certifications": "Consider AWS Certified Developer, Google Cloud certification, or specialized ML certifications."
    }
    
    return insights
