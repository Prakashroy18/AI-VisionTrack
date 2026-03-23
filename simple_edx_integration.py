#!/usr/bin/env python3
"""
Simple Open edX Course Catalog Integration (No OAuth Required)
This uses public course catalog APIs that don't require authentication.
"""

import requests
import json

def get_openedx_courses_direct(query, max_results=5):
    """
    Get courses from Open edX using direct API access (no OAuth required).
    This works with public course catalog endpoints.
    """
    
    # Try different Open edX instances with public APIs
    api_endpoints = [
        "https://sandbox.openedx.org/api/courses/v1/courses/",
        "https://courses.openedx.org/api/courses/v1/courses/",
        "https://api.openedx.org/courses/"
    ]
    
    courses = []
    
    for endpoint in api_endpoints:
        try:
            # Add search parameter if supported
            if "?" in endpoint:
                url = f"{endpoint}&search={query}&page_size={max_results}"
            else:
                url = f"{endpoint}?search={query}&page_size={max_results}"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', []) if isinstance(data, dict) else []
                
                for course in results[:max_results]:
                    course_info = {
                        "title": course.get('name', course.get('title', 'Untitled Course')),
                        "url": course.get('course_url', course.get('url', '#')),
                        "description": course.get('short_description', course.get('description', ''))[:200],
                        "provider": "Open edX"
                    }
                    courses.append(course_info)
                
                if courses:
                    break  # Found courses, stop trying other endpoints
                    
        except Exception as e:
            continue  # Try next endpoint
    
    return courses

def get_mock_courses(query, max_results=5):
    """
    Fallback: Return mock course data when APIs are not available.
    This is perfect for project demos and testing.
    """
    
    mock_courses = {
        "python": [
            {
                "title": "Introduction to Python Programming",
                "url": "https://sandbox.openedx.org/courses/course-v1:DemoX+Demo_Course+2024/about",
                "description": "Learn Python programming fundamentals including variables, functions, and data structures.",
                "provider": "Open edX Demo"
            },
            {
                "title": "Advanced Python for Data Science",
                "url": "https://sandbox.openedx.org/courses/course-v1:DemoX+Advanced_Python+2024/about",
                "description": "Master advanced Python concepts for data science including NumPy, Pandas, and data visualization.",
                "provider": "Open edX Demo"
            }
        ],
        "data science": [
            {
                "title": "Data Science Fundamentals",
                "url": "https://sandbox.openedx.org/courses/course-v1:DemoX+Data_Science+2024/about",
                "description": "Introduction to data science concepts, statistics, and machine learning basics.",
                "provider": "Open edX Demo"
            },
            {
                "title": "Machine Learning with Python",
                "url": "https://sandbox.openedx.org/courses/course-v1:DemoX+ML_Python+2024/about",
                "description": "Learn machine learning algorithms and implementation using Python.",
                "provider": "Open edX Demo"
            }
        ],
        "web development": [
            {
                "title": "Full Stack Web Development",
                "url": "https://sandbox.openedx.org/courses/course-v1:DemoX+Web_Dev+2024/about",
                "description": "Complete web development course covering HTML, CSS, JavaScript, and backend frameworks.",
                "provider": "Open edX Demo"
            }
        ]
    }
    
    # Find matching courses based on query
    query_lower = query.lower()
    for key, course_list in mock_courses.items():
        if key in query_lower or any(word in query_lower for word in key.split()):
            return course_list[:max_results]
    
    # Default courses if no match
    return [
        {
            "title": "Computer Science Fundamentals",
            "url": "https://sandbox.openedx.org/courses/course-v1:DemoX+CS_Fundamentals+2024/about",
            "description": "Introduction to computer science concepts and programming fundamentals.",
            "provider": "Open edX Demo"
        }
    ]

def get_courses_fallback(query, max_results=5):
    """
    Get courses using multiple fallback strategies:
    1. Try direct API access
    2. Use mock data for demo purposes
    """
    
    # Try direct API first
    courses = get_openedx_courses_direct(query, max_results)
    
    # If no courses found, use mock data
    if not courses:
        courses = get_mock_courses(query, max_results)
    
    return courses

# Test the integration
if __name__ == "__main__":
    print("Testing Simple Open edX Integration...")
    print("=" * 50)
    
    test_queries = ["python", "data science", "web development", "artificial intelligence"]
    
    for query in test_queries:
        print(f"\nSearching for: {query}")
        courses = get_courses_fallback(query, max_results=3)
        
        if courses:
            print(f"Found {len(courses)} courses:")
            for i, course in enumerate(courses, 1):
                print(f"  {i}. {course['title']}")
                print(f"     Provider: {course['provider']}")
                print(f"     Description: {course['description'][:100]}...")
        else:
            print("No courses found")
    
    print("\nIntegration test completed!")
