"""
Static Recommendation Engine - Rule-based & Reliable
No ML complexity, no randomness, 100% working
"""

from static_courses import STATIC_COURSES, DEFAULT_COURSES

def get_recommendations(user_role, user_skills=None, max_recommendations=8):
    """
    Get course recommendations based on user role and skills
    
    Args:
        user_role (str): Career goal/role (e.g., "software_developer")
        user_skills (list): List of user skills
        max_recommendations (int): Maximum number of recommendations
    
    Returns:
        list: Recommended courses with recommendation reasons
    """
    recommendations = []
    
    # Get courses for the user's role
    role_courses = STATIC_COURSES.get(user_role, [])
    
    # If no skills provided, return top courses for the role
    if not user_skills:
        recommendations = [
            {
                "course": course,
                "recommendation_reason": "Matches your career goal",
                "match_score": 0.8
            }
            for course in role_courses[:max_recommendations]
        ]
    else:
        # Match courses based on skills
        user_skills_lower = [skill.lower() for skill in user_skills]
        
        for course in role_courses:
            course_skills_lower = [skill.lower() for skill in course.get("skills", [])]
            
            # Check if any user skill matches course skills
            skill_matches = set(user_skills_lower) & set(course_skills_lower)
            
            if skill_matches:
                # Calculate match score (more skills matched = higher score)
                match_score = len(skill_matches) / len(course_skills_lower)
                
                recommendations.append({
                    "course": course,
                    "recommendation_reason": f"Matches your skills: {', '.join(skill_matches)}",
                    "match_score": match_score
                })
        
        # Sort by match score (highest first)
        recommendations.sort(key=lambda x: x["match_score"], reverse=True)
        recommendations = recommendations[:max_recommendations]
    
    # Fallback: if no recommendations, return default courses
    if not recommendations:
        recommendations = [
            {
                "course": course,
                "recommendation_reason": "Popular course for your career path",
                "match_score": 0.5
            }
            for course in DEFAULT_COURSES[:max_recommendations]
        ]
    
    return recommendations

def get_all_career_paths():
    """
    Get all available career paths/roles
    
    Returns:
        list: Available career paths
    """
    return list(STATIC_COURSES.keys())

def get_courses_by_role(role):
    """
    Get all courses for a specific role
    
    Args:
        role (str): Career role
    
    Returns:
        list: All courses for the role
    """
    return STATIC_COURSES.get(role, [])

def search_courses(query, role=None):
    """
    Search courses by title or description
    
    Args:
        query (str): Search query
        role (str): Optional role filter
    
    Returns:
        list: Matching courses
    """
    query_lower = query.lower()
    results = []
    
    courses_to_search = get_courses_by_role(role) if role else []
    
    # If no role specified, search all courses
    if not courses_to_search:
        for role_courses in STATIC_COURSES.values():
            courses_to_search.extend(role_courses)
    
    for course in courses_to_search:
        # Search in title, description, and skills
        searchable_text = f"{course.get('title', '')} {course.get('description', '')} {' '.join(course.get('skills', []))}"
        
        if query_lower in searchable_text.lower():
            results.append({
                "course": course,
                "recommendation_reason": f"Matches your search: '{query}'"
            })
    
    return results[:10]  # Limit search results
