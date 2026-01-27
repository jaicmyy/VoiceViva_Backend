import requests
import os

BASE_URL = "http://localhost:5000"

print("=" * 50)
print("Testing Voice Viva Backend Endpoints")
print("=" * 50)

# Test 1: Health Check
print("\n1. Testing health check...")
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   ERROR: {e}")

# Test 2: Get Subjects
print("\n2. Testing GET /api/admin/subjects...")
try:
    response = requests.get(f"{BASE_URL}/api/admin/subjects")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        subjects = response.json()
        print(f"   Found {len(subjects)} subjects")
        if subjects:
            print(f"   Sample: {subjects[0]}")
    else:
        print(f"   Error: {response.text}")
except Exception as e:
    print(f"   ERROR: {e}")

# Test 3: Add Subject (with dummy PDF)
print("\n3. Testing POST /api/admin/subjects...")
try:
    # Create a dummy PDF file
    dummy_pdf_path = "test_dummy.pdf"
    with open(dummy_pdf_path, "wb") as f:
        f.write(b"%PDF-1.4\n%Test PDF\n")
    
    with open(dummy_pdf_path, "rb") as pdf_file:
        files = {"syllabus": ("test.pdf", pdf_file, "application/pdf")}
        data = {
            "name": "Test Subject",
            "code": f"TEST{os.urandom(3).hex()}"
        }
        response = requests.post(f"{BASE_URL}/api/admin/subjects", files=files, data=data)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    
    # Clean up
    if os.path.exists(dummy_pdf_path):
        os.remove(dummy_pdf_path)
        
except Exception as e:
    print(f"   ERROR: {e}")
    if os.path.exists("test_dummy.pdf"):
        os.remove("test_dummy.pdf")

print("\n" + "=" * 50)
print("Testing Complete")
print("=" * 50)
