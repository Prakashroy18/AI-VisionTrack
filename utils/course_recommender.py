"""
Course Recommendation System using ML
Provides personalized course recommendations based on user profile, skills, and career goals
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import joblib
import json

class CourseRecommender:
    def __init__(self):
        self.courses_db = self._load_courses_database()
        self.scaler = StandardScaler()
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        
    def _load_courses_database(self):
        """Load comprehensive course database"""
        return {
            'engineering': {
                'courses': [
                    {
                        'id': 'eng_001',
                        'title': 'Engineering Mathematics Fundamentals',
                        'provider': 'Coursera',
                        'duration': '8 weeks',
                        'level': 'Beginner',
                        'skills': ['calculus', 'linear algebra', 'differential equations'],
                        'career_path': 'engineering',
                        'rating': 4.8,
                        'enrollment': 'High',
                        'description': 'Master the mathematical foundations essential for engineering careers',
                        'url': 'https://www.coursera.org/learn/engineering-math'
                    },
                    {
                        'id': 'eng_002',
                        'title': 'Introduction to Programming',
                        'provider': 'edX',
                        'duration': '6 weeks',
                        'level': 'Beginner',
                        'skills': ['python', 'javascript', 'problem solving'],
                        'career_path': 'engineering',
                        'rating': 4.7,
                        'enrollment': 'Very High',
                        'description': 'Learn programming fundamentals for engineering applications',
                        'url': 'https://www.edx.org/course/introduction-programming'
                    },
                    {
                        'id': 'eng_003',
                        'title': 'Data Structures & Algorithms',
                        'provider': 'Udacity',
                        'duration': '10 weeks',
                        'level': 'Intermediate',
                        'skills': ['algorithms', 'data structures', 'complexity analysis'],
                        'career_path': 'engineering',
                        'rating': 4.9,
                        'enrollment': 'High',
                        'description': 'Master essential computer science concepts for software engineering',
                        'url': 'https://www.udacity.com/course/data-structures-algorithms'
                    }
                ]
            },
            'data_science': {
                'courses': [
                    {
                        'id': 'ds_001',
                        'title': 'Python for Data Science',
                        'provider': 'DataCamp',
                        'duration': '4 weeks',
                        'level': 'Beginner',
                        'skills': ['python', 'numpy', 'pandas', 'data analysis'],
                        'career_path': 'data_science',
                        'rating': 4.6,
                        'enrollment': 'High',
                        'description': 'Learn Python programming specifically for data science applications',
                        'url': 'https://www.datacamp.com/courses/python-data-science'
                    },
                    {
                        'id': 'ds_002',
                        'title': 'Machine Learning Fundamentals',
                        'provider': 'Coursera',
                        'duration': '12 weeks',
                        'level': 'Intermediate',
                        'skills': ['machine learning', 'scikit-learn', 'model evaluation'],
                        'career_path': 'data_science',
                        'rating': 4.8,
                        'enrollment': 'Very High',
                        'description': 'Understand core ML concepts and build predictive models',
                        'url': 'https://www.coursera.org/learn/machine-learning'
                    }
                ]
            },
            'web_development': {
                'courses': [
                    {
                        'id': 'web_001',
                        'title': 'HTML, CSS & JavaScript Basics',
                        'provider': 'freeCodeCamp',
                        'duration': '6 weeks',
                        'level': 'Beginner',
                        'skills': ['html', 'css', 'javascript', 'responsive design'],
                        'career_path': 'web_development',
                        'rating': 4.7,
                        'enrollment': 'Very High',
                        'description': 'Build modern websites with core web technologies',
                        'url': 'https://www.freecodecamp.org/learn/responsive-web-design'
                    },
                    {
                        'id': 'web_002',
                        'title': 'React.js Development',
                        'provider': 'Udemy',
                        'duration': '8 weeks',
                        'level': 'Intermediate',
                        'skills': ['react', 'components', 'state management', 'hooks'],
                        'career_path': 'web_development',
                        'rating': 4.5,
                        'enrollment': 'High',
                        'description': 'Build interactive web applications with React',
                        'url': 'https://www.udemy.com/course/react-js-development'
                    }
                ]
            },
            'business': {
                'courses': [
                    {
                        'id': 'biz_001',
                        'title': 'Business Analytics Fundamentals',
                        'provider': 'LinkedIn Learning',
                        'duration': '4 weeks',
                        'level': 'Beginner',
                        'skills': ['analytics', 'excel', 'data visualization', 'kpi'],
                        'career_path': 'business',
                        'rating': 4.4,
                        'enrollment': 'High',
                        'description': 'Learn data-driven decision making for business success',
                        'url': 'https://www.linkedin.com/learning/business-analytics'
                    },
                    {
                        'id': 'biz_002',
                        'title': 'Digital Marketing Strategy',
                        'provider': 'Google Digital Garage',
                        'duration': '6 weeks',
                        'level': 'Intermediate',
                        'skills': ['seo', 'social media', 'content marketing', 'analytics'],
                        'career_path': 'business',
                        'rating': 4.6,
                        'enrollment': 'Very High',
                        'description': 'Master digital marketing techniques for business growth',
                        'url': 'https://learndigital.withgoogle.com/digital-marketing'
                    }
                ]
            }
        }
    
    def analyze_user_profile(self, user_data):
        """Analyze user profile and extract features"""
        features = {}
        
        # Extract skills and interests
        skills = user_data.get('skills', [])
        interests = user_data.get('interests', [])
        education = user_data.get('education', '')
        work_type = user_data.get('work_type', '')
        
        # Create feature vector
        features['skills_count'] = len(skills)
        features['interests_count'] = len(interests)
        features['education_level'] = self._encode_education(education)
        features['work_preference'] = self._encode_work_type(work_type)
        
        # Combine all text features
        text_features = ' '.join(skills + interests + [education] + [work_type])
        
        return features, text_features
    
    def _encode_education(self, education):
        """Encode education level numerically"""
        education_map = {
            'high school': 1,
            'intermediate': 2,
            'bachelors': 3,
            'masters': 4,
            'phd': 5
        }
        return education_map.get(education.lower(), 2)
    
    def _encode_work_type(self, work_type):
        """Encode work preference numerically"""
        work_map = {
            'remote': 1,
            'office': 2,
            'hybrid': 3,
            'field': 4
        }
        return work_map.get(work_type.lower(), 2)
    
    def calculate_career_match(self, user_features, career_path):
        """Calculate how well user matches a career path"""
        career_keywords = {
            'engineering': ['programming', 'math', 'problem solving', 'technical', 'innovation'],
            'data_science': ['data', 'analytics', 'statistics', 'machine learning', 'python'],
            'web_development': ['web', 'javascript', 'html', 'css', 'frontend', 'backend'],
            'business': ['management', 'marketing', 'strategy', 'leadership', 'finance']
        }
        
        user_text = user_features.lower()
        career_keywords_list = career_keywords.get(career_path, [])
        
        # Calculate keyword match score
        match_score = 0
        for keyword in career_keywords_list:
            if keyword in user_text:
                match_score += 1
        
        return match_score / len(career_keywords_list) if career_keywords_list else 0
    
    def recommend_courses(self, user_data, num_recommendations=5):
        """Generate personalized course recommendations"""
        features, text_features = self.analyze_user_profile(user_data)
        
        recommendations = []
        
        # Calculate career path matches
        career_matches = {}
        for career_path in self.courses_db.keys():
            match_score = self.calculate_career_match(text_features, career_path)
            career_matches[career_path] = match_score
        
        # Sort career paths by match score
        sorted_careers = sorted(career_matches.items(), key=lambda x: x[1], reverse=True)
        
        # Get courses from best matching career paths
        for career_path, match_score in sorted_careers[:2]:  # Top 2 career paths
            if career_path in self.courses_db:
                courses = self.courses_db[career_path]['courses']
                
                # Score courses based on user features
                scored_courses = []
                for course in courses:
                    score = self._calculate_course_score(course, features, match_score)
                    scored_courses.append((course, score))
                
                # Sort by score and take top courses
                scored_courses.sort(key=lambda x: x[1], reverse=True)
                top_courses = scored_courses[:3]  # Top 3 from each career path
                
                for course, score in top_courses:
                    recommendations.append({
                        'course': course,
                        'score': score,
                        'career_match': match_score,
                        'career_path': career_path,
                        'recommendation_reason': self._get_recommendation_reason(course, features, match_score)
                    })
        
        # Sort all recommendations by overall score
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        return recommendations[:num_recommendations]
    
    def _calculate_course_score(self, course, user_features, career_match):
        """Calculate score for a specific course"""
        score = 0
        
        # Base score from rating and enrollment
        score += course['rating'] * 10  # Rating weight
        score += 5 if course['enrollment'] == 'Very High' else 3 if course['enrollment'] == 'High' else 1
        
        # Career path match bonus
        score += career_match * 20
        
        # Skill alignment bonus
        user_skills = user_features.get('skills', [])
        course_skills = course.get('skills', [])
        skill_matches = len(set(user_skills) & set(course_skills))
        score += skill_matches * 5
        
        # Level appropriateness
        education_level = user_features.get('education_level', 2)
        course_level_map = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3}
        course_level = course_level_map.get(course.get('level', 'Intermediate'), 2)
        level_diff = abs(education_level - course_level)
        score += max(0, 10 - level_diff * 3)  # Bonus for appropriate level
        
        return score
    
    def _get_recommendation_reason(self, course, user_features, career_match):
        """Generate explanation for recommendation"""
        reasons = []
        
        if career_match > 0.7:
            reasons.append("Strong match with your career interests")
        
        user_skills = user_features.get('skills', [])
        course_skills = course.get('skills', [])
        skill_matches = set(user_skills) & set(course_skills)
        if skill_matches:
            reasons.append(f"Aligns with your skills: {', '.join(skill_matches)}")
        
        if course['rating'] >= 4.5:
            reasons.append("Highly rated by other learners")
        
        if course['enrollment'] in ['Very High', 'High']:
            reasons.append("Popular choice among students")
        
        return " | ".join(reasons) if reasons else "Recommended based on your profile"
    
    def generate_learning_path(self, user_data, career_path):
        """Generate structured learning path for a career"""
        if career_path not in self.courses_db:
            return []
        
        courses = self.courses_db[career_path]['courses']
        
        # Sort by difficulty and prerequisites
        sorted_courses = sorted(courses, key=lambda x: (
            {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3}.get(x.get('level', 'Intermediate'), 2)
        ))
        
        learning_path = []
        for i, course in enumerate(sorted_courses):
            learning_path.append({
                'step': i + 1,
                'course': course,
                'estimated_time': course['duration'],
                'prerequisites': self._get_prerequisites(course, sorted_courses[:i]),
                'next_courses': [c['title'] for c in sorted_courses[i+1:i+2]]
            })
        
        return learning_path
    
    def _get_prerequisites(self, course, previous_courses):
        """Determine prerequisites for a course"""
        if course['level'] == 'Beginner':
            return "None - Start here!"
        
        prev_skills = set()
        for prev_course in previous_courses:
            prev_skills.update(prev_course.get('skills', []))
        
        course_skills = set(course.get('skills', []))
        missing_skills = course_skills - prev_skills
        
        if missing_skills:
            return f"Recommended: {', '.join(list(missing_skills)[:3])}"
        else:
            return "Ready to start!"
    
    def get_career_insights(self, user_data):
        """Generate career insights based on user profile"""
        insights = []
        
        skills = user_data.get('skills', [])
        education = user_data.get('education', '')
        
        # Advanced skill gap analysis
        skill_gaps = self._analyze_skill_gaps(skills, education)
        if skill_gaps:
            insights.append({
                'type': 'skill_gap',
                'message': f"Recommended skills to develop: {', '.join(skill_gaps[:5])}",
                'priority': 'high',
                'missing_skills': skill_gaps
            })
        
        # Education progression recommendations
        education_path = self._suggest_education_path(education)
        if education_path:
            insights.append({
                'type': 'education_path',
                'message': education_path,
                'priority': 'medium'
            })
        
        # Career market insights
        market_insights = self._get_market_insights(skills)
        if market_insights:
            insights.extend(market_insights)
        
        # Learning style recommendations
        learning_style = self._analyze_learning_style(skills)
        insights.append({
            'type': 'learning_style',
            'message': learning_style,
            'priority': 'low'
        })
        
        # Career path suggestions
        career_matches = {}
        for career_path in ['engineering', 'data_science', 'web_development', 'business']:
            match_score = self.calculate_career_match(' '.join(skills), career_path)
            career_matches[career_path] = match_score
        
        top_careers = sorted(career_matches.items(), key=lambda x: x[1], reverse=True)[:2]
        
        for career_path, score in top_careers:
            if score > 0.5:
                insights.append({
                    'type': 'career_suggestion',
                    'message': f"Strong potential in {career_path.replace('_', ' ').title()} based on your profile",
                    'priority': 'medium',
                    'career_path': career_path,
                    'confidence': round(score * 100, 1)
                })
        
        return insights
    
    def _analyze_skill_gaps(self, skills, education):
        """Analyze skill gaps based on career requirements"""
        required_skills = {
            'high school': ['basic computer skills', 'mathematics'],
            'intermediate': ['programming', 'data analysis', 'communication'],
            'bachelors': ['advanced programming', 'project management', 'technical writing'],
            'masters': ['machine learning', 'research methods', 'leadership']
        }
        
        user_skill_set = set(skill.lower() for skill in skills)
        required_set = set(required_skills.get(education.lower(), []))
        
        gaps = required_set - user_skill_set
        return list(gaps)[:10]  # Return top 10 missing skills
    
    def _suggest_education_path(self, current_education):
        """Suggest next education steps"""
        education_map = {
            'high school': 'Consider pursuing intermediate education to build technical foundation',
            'intermediate': 'Bachelors degree in engineering or computer science can open more opportunities',
            'bachelors': 'Masters degree can lead to senior positions and specialized roles',
            'masters': 'PhD or specialized certifications can lead to research and leadership roles'
        }
        return education_map.get(current_education.lower(), 'Continue learning and gaining experience')
    
    def _get_market_insights(self, skills):
        """Get market insights based on current skills"""
        insights = []
        
        # High-demand skills
        high_demand_skills = ['python', 'machine learning', 'data science', 'web development', 'cloud computing']
        user_high_demand = [skill for skill in skills if skill.lower() in high_demand_skills]
        
        if user_high_demand:
            insights.append({
                'type': 'market_demand',
                'message': f"Your high-demand skills: {', '.join(user_high_demand)}",
                'priority': 'medium'
            })
        
        # Salary potential insights
        salary_insights = self._get_salary_insights(skills)
        if salary_insights:
            insights.append(salary_insights)
        
        return insights
    
    def _get_salary_insights(self, skills):
        """Estimate salary potential based on skills"""
        skill_salary_map = {
            'machine learning': '$120,000 - $180,000',
            'data science': '$100,000 - $160,000',
            'web development': '$80,000 - $140,000',
            'cloud computing': '$110,000 - $170,000',
            'python': '$90,000 - $150,000'
        }
        
        max_salary = 0
        matching_skills = []
        for skill in skills:
            skill_lower = skill.lower()
            for key, salary in skill_salary_map.items():
                if key in skill_lower:
                    max_salary = max(max_salary, int(salary.split('-')[1].replace('$', '').replace(',', '')))
                    matching_skills.append(skill)
                    break
        
        if max_salary > 0:
            return {
                'type': 'salary_potential',
                'message': f"Potential salary range: ${skill_salary_map.get(matching_skills[0].lower(), '$80,000 - $120,000')}",
                'priority': 'medium'
            }
        
        return None
    
    def _analyze_learning_style(self, skills):
        """Analyze user's preferred learning style"""
        technical_skills = ['programming', 'coding', 'algorithms', 'data structures']
        creative_skills = ['design', 'writing', 'communication']
        analytical_skills = ['data analysis', 'statistics', 'research']
        
        technical_count = sum(1 for skill in skills if any(tech in skill.lower() for tech in technical_skills))
        creative_count = sum(1 for skill in skills if any(creative in skill.lower() for creative in creative_skills))
        analytical_count = sum(1 for skill in skills if any(analytical in skill.lower() for analytical in analytical_skills))
        
        if technical_count >= creative_count and technical_count >= analytical_count:
            return "Technical learner with balanced analytical and creative skills"
        elif technical_count > creative_count:
            return "Strong technical background - consider developing creative and communication skills"
        elif creative_count > analytical_count:
            return "Creative learner - strengthen technical and analytical foundations"
        else:
            return "Analytical learner - complement with technical and creative skills"
    
    def generate_personalized_learning_path(self, user_data, career_path):
        """Generate hyper-personalized learning path"""
        if career_path not in self.courses_db:
            return []
        
        courses = self.courses_db[career_path]['courses']
        user_skills = [skill.lower() for skill in user_data.get('skills', [])]
        user_education = user_data.get('education', 'intermediate')
        
        # Sort courses by personalized relevance score
        scored_courses = []
        for course in courses:
            score = self._calculate_personalized_score(course, user_skills, user_education)
            scored_courses.append((course, score))
        
        scored_courses.sort(key=lambda x: x[1], reverse=True)
        
        learning_path = []
        for i, (course, score) in enumerate(scored_courses):
            prerequisites = self._get_personalized_prerequisites(course, scored_courses[:i], user_skills)
            learning_path.append({
                'step': i + 1,
                'course': course,
                'estimated_time': course['duration'],
                'prerequisites': prerequisites,
                'next_courses': [c['title'] for c in scored_courses[i+1:i+2]],
                'personalization_score': score,
                'skill_alignment': self._calculate_skill_alignment(course, user_skills)
            })
        
        return learning_path
    
    def _calculate_personalized_score(self, course, user_skills, user_education):
        """Calculate personalized relevance score for a course"""
        score = 0
        
        # Base score from rating and enrollment
        score += course['rating'] * 10
        score += 5 if course['enrollment'] == 'Very High' else 3 if course['enrollment'] == 'High' else 1
        
        # Skill alignment bonus (enhanced)
        course_skills = course.get('skills', [])
        skill_alignment = self._calculate_skill_alignment(course, user_skills)
        score += skill_alignment * 15  # Increased weight for skill alignment
        
        # Level appropriateness with education consideration
        course_level_map = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3}
        user_level_map = {'high school': 1, 'intermediate': 2, 'bachelors': 3, 'masters': 4, 'phd': 5}
        course_level = course_level_map.get(course.get('level', 'Intermediate'), 2)
        user_level = user_level_map.get(user_education.lower(), 2)
        level_diff = abs(user_level - course_level)
        score += max(0, 15 - level_diff * 2)  # Enhanced level scoring
        
        # Career path match bonus
        career_match = self.calculate_career_match(' '.join(user_skills), course.get('career_path', ''))
        score += career_match * 25
        
        return score
    
    def _calculate_skill_alignment(self, course, user_skills):
        """Calculate percentage of course skills that match user skills"""
        course_skills = [skill.lower() for skill in course.get('skills', [])]
        user_skill_set = set(skill.lower() for skill in user_skills)
        
        if not course_skills:
            return 0
        
        matches = sum(1 for skill in course_skills if skill in user_skill_set)
        return (matches / len(course_skills)) * 100
    
    def _get_personalized_prerequisites(self, course, previous_courses, user_skills):
        """Generate personalized prerequisite recommendations"""
        if course['level'] == 'Beginner':
            return "Perfect starting point for your learning journey!"
        
        # Check skill gaps from user profile
        course_skills = set(course.get('skills', []))
        user_skill_set = set(skill.lower() for skill in user_skills)
        
        missing_skills = course_skills - user_skill_set
        if missing_skills:
            return f"Focus on: {', '.join(list(missing_skills)[:3])} before starting"
        else:
            return "You have the required skills - ready to start!"

# Initialize the recommender
course_recommender = CourseRecommender()

def get_personalized_recommendations(user_data, num_recommendations=5):
    """Get personalized course recommendations for a user"""
    return course_recommender.recommend_courses(user_data, num_recommendations)

def generate_learning_path(user_data, career_path):
    """Generate a complete learning path for a career"""
    return course_recommender.generate_learning_path(user_data, career_path)

def get_career_insights(user_data):
    """Get personalized career insights and recommendations"""
    return course_recommender.get_career_insights(user_data)
