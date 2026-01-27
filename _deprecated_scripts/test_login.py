import requests

BASE_URL = "http://localhost:5000"

def test_login(reg, password):
    print(f"\nTesting login for {reg}...")
    url = f"{BASE_URL}/api/auth/login"
    payload = {
        "registration_number": reg,
        "password": password
    }
    try:
        response = requests.post(url, json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Test with valid admin
    test_login("admin", "Admin")
    # Test with invalid admin
    test_login("admin", "WrongPass")
    # Test with malformed payload (empty json)
    print("\nTesting empty payload...")
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", headers={"Content-Type": "application/json"}, data="")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
