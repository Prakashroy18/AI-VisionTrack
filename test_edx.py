#!/usr/bin/env python3
"""
Test script for Open edX API integration
Run this after adding your credentials to .env
"""

import os
from dotenv import load_dotenv
import sys
sys.path.append('.')
from app import get_edx_courses, get_edx_access_token

def test_edx_integration():
    """Test Open edX API integration"""
    print("Testing Open edX API Integration...")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check credentials
    client_id = os.environ.get('EDX_CLIENT_ID')
    client_secret = os.environ.get('EDX_CLIENT_SECRET')
    access_token = os.environ.get('EDX_ACCESS_TOKEN')
    api_url = os.environ.get('EDX_API_URL', 'https://api.openedx.org')
    
    print(f"API URL: {api_url}")
    print(f"Client ID: {'Set' if client_id and client_id != 'your_client_id_here' else 'Not set or placeholder'}")
    print(f"Client Secret: {'Set' if client_secret else 'Not set'}")
    print(f"Access Token: {'Set' if access_token else 'Not set'}")
    
    if not client_id or client_id == 'your_client_id_here':
        print("\nPlease add your Open edX API credentials to .env file")
        print("   See EDX_SETUP_INSTRUCTIONS.md for details")
        print("   Go to: https://sandbox.openedx.org/admin")
        print("   Then look for OAuth2 section -> Clients")
        return False
    
    # Test access token
    print("\nTesting access token...")
    token = get_edx_access_token()
    if token:
        print(f"Access token obtained (length: {len(token)})")
    else:
        print("Failed to get access token")
        return False
    
    # Test course search
    print("\nTesting course search...")
    test_queries = ['python', 'data science', 'web development']
    
    for query in test_queries:
        print(f"\nSearching for: {query}")
        courses = get_edx_courses(query, max_results=3)
        
        if courses:
            print(f"Found {len(courses)} courses:")
            for i, course in enumerate(courses, 1):
                title = course.get('title', 'No title')
                provider = course.get('provider', 'Unknown')
                print(f"  {i}. {title} - {provider}")
        else:
            print("No courses found")
    
    print("\nOpen edX integration test completed!")
    return True

if __name__ == "__main__":
    test_edx_integration()
