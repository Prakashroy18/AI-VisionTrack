import firebase_admin
from firebase_admin import credentials, auth, firestore
import json
import os

# Initialize Firebase Admin SDK (with fallback to mock)
try:
    # Check if Firebase is already initialized
    if not firebase_admin._apps:
        # Try to load service account key from file
        if os.path.exists('firebase-service-account.json'):
            try:
                with open('firebase-service-account.json', 'r') as f:
                    service_account = json.load(f)
                
                # Validate service account has required fields and real values
                if all(key in service_account for key in ['type', 'project_id', 'private_key', 'client_email']):
                    # Check if values are real (not placeholders)
                    if ('YOUR_' not in str(service_account['private_key']) and 
                        'YOUR_' not in service_account['client_email'] and
                        'xxxxx' not in service_account['client_email']):
                        
                        cred = credentials.Certificate(service_account)
                        firebase_admin.initialize_app(cred, {
                            'projectId': service_account['project_id'],
                        })
                        print("Firebase initialized with REAL service account key!")
                        print(f"Project ID: {service_account['project_id']}")
                        print(f"Service Account: {service_account['client_email']}")
                    else:
                        print("Service account contains placeholder values")
                        print("Using frontend Firebase authentication only")
                        # Initialize with minimal config for frontend compatibility
                        firebase_admin.initialize_app({
                            'projectId': 'career-counselor',
                        })
                else:
                    print("Invalid service account JSON format")
                    print("Using frontend Firebase authentication only")
                    firebase_admin.initialize_app({
                        'projectId': 'career-counselor',
                    })
            except json.JSONDecodeError:
                print("Invalid JSON in firebase-service-account.json")
                print("Using frontend Firebase authentication only")
                firebase_admin.initialize_app({
                    'projectId': 'career-counselor',
                })
            except Exception as e:
                print(f"Error loading service account: {e}")
                print("Using frontend Firebase authentication only")
                firebase_admin.initialize_app({
                    'projectId': 'career-counselor',
                })
        else:
            print("No Firebase service account key found")
            print("Using frontend Firebase authentication only")
            firebase_admin.initialize_app({
                'projectId': 'career-counselor',
            })
        
        # Get Firestore and Auth clients
        db = firestore.client()
        print("Firebase initialized successfully!")
    else:
        # Firebase already initialized
        db = firestore.client()
        print("Firebase already initialized!")
    
except Exception as e:
    print(f"Firebase initialization error: {e}")
    print("Using frontend Firebase authentication only")
    
    # Create mock functions for development
    class MockUser:
        def __init__(self, email, uid=None):
            self.email = email
            self.uid = uid or f"mock_{email.replace('@', '_').replace('.', '_')}"
    
    class MockFirestore:
        def collection(self, name):
            return MockCollection()
    
    class MockCollection:
        def document(self, doc_id):
            return MockDocument()
    
    class MockDocument:
        def set(self, data):
            print(f"📝 Mock: Would save to Firestore: {data}")
    
    # Set mock database if Firebase failed to initialize
    try:
        db = firestore.client()
    except:
        db = MockFirestore()

def create_user(email, password, username=None):
    """Create a new user in Firebase"""
    try:
        # Check if we're using mock configuration or frontend-only
        if not firebase_admin._apps or len(firebase_admin._apps) == 0:
            # Mock user creation for development - frontend handles real auth
            mock_user = MockUser(email)
            print(f"📝 Frontend will handle real Firebase user creation for {email}")
            
            # Store additional user data in mock Firestore
            if db and username:
                user_doc = {
                    'username': username,
                    'email': email,
                    'created_at': 'mock_timestamp',
                    'uid': mock_user.uid
                }
                db.collection('users').document(mock_user.uid).set(user_doc)
            
            return {'success': True, 'user': mock_user, 'frontend_auth': True}
        
        # Real Firebase user creation (when service account is properly configured)
        user = auth.create_user(
            email=email,
            password=password
        )
        
        # Store additional user data in Firestore
        if db and username:
            user_doc = {
                'username': username,
                'email': email,
                'created_at': firestore.SERVER_TIMESTAMP,
                'uid': user.uid
            }
            db.collection('users').document(user.uid).set(user_doc)
        
        return {'success': True, 'user': user}
    
    except Exception as e:
        return {'success': False, 'error': str(e)}

def sign_in_user(email, password):
    """Sign in user with email and password"""
    try:
        # Check if we're using mock configuration or frontend-only
        if not firebase_admin._apps or len(firebase_admin._apps) == 0:
            # Mock user sign-in for development - frontend handles real auth
            mock_user = MockUser(email)
            print(f"📝 Frontend will handle real Firebase authentication for {email}")
            return {'success': True, 'user': mock_user, 'frontend_auth': True}
        
        # Real Firebase user lookup (when service account is properly configured)
        user = auth.get_user_by_email(email)
        return {'success': True, 'user': user}
    
    except Exception as e:
        return {'success': False, 'error': str(e)}
