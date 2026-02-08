#!/usr/bin/env python
"""
Test Stage-1 ML Inference End-to-End
"""
import requests

BASE_URL = "http://localhost:5000"

def test_stage1():
    print("=" * 50)
    print("MirAI Stage-1 ML Inference Test")
    print("=" * 50)
    
    # 1. Register a new user
    print("\n1. Registering new user...")
    reg_response = requests.post(f"{BASE_URL}/api/auth/register", json={
        "email": "testuser@example.com",
        "password": "test123",
        "full_name": "Test User"
    })
    
    if reg_response.status_code == 201:
        print("   ✅ Registration successful!")
        data = reg_response.json()
        token = data['access_token']
    elif reg_response.status_code in [400, 409]:
        # User already exists, try login
        print("   User exists. Logging in...")
        login_response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "testuser@example.com",
            "password": "test123"
        })
        if login_response.status_code == 200:
            print("   ✅ Login successful!")
            data = login_response.json()
            token = data['access_token']
        else:
            print(f"   ❌ Login failed: {login_response.json()}")
            return
    else:
        print(f"   ❌ Registration failed: {reg_response.json()}")
        return
    
    # 2. Test Stage-1 Prediction
    print("\n2. Testing Stage-1 ML Inference...")
    print("   Input data:")
    stage1_data = {
        "age": 72,
        "gender": "Female",
        "education": 14,
        "faq": 8,
        "ecogMem": 2.5,
        "ecogTotal": 2.5
    }
    for k, v in stage1_data.items():
        print(f"     - {k}: {v}")
    
    headers = {"Authorization": f"Bearer {token}"}
    stage1_response = requests.post(
        f"{BASE_URL}/api/predict/stage1",
        json=stage1_data,
        headers=headers
    )
    
    if stage1_response.status_code == 200:
        result = stage1_response.json()
        print("\n   ✅ Stage-1 Inference SUCCESS!")
        print(f"   📊 Probability: {result['probability'] * 100:.1f}%")
        print(f"   🏷️  Risk Level: {result['risk_level']}")
        print(f"   💡 Factors: {result.get('factors', [])}")
        print(f"   📋 Assessment ID: {result['assessment_id']}")
        return result
    else:
        print(f"   ❌ Stage-1 Failed: {stage1_response.status_code}")
        print(f"   Response: {stage1_response.text}")
        return None

if __name__ == "__main__":
    test_stage1()
    print("\n" + "=" * 50)
    print("Test Complete!")
    print("=" * 50)
