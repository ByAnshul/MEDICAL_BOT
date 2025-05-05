"""
Test Script for Prescription Integration with Medical Bot

This script tests the basic functionality of the prescription reminder system:
1. Tests that the /prescription route is accessible
2. Tests that the API endpoint for scheduling reminders works correctly
"""

import json
import requests
import unittest

# Base URL for testing - change if your app runs on a different port
BASE_URL = "http://localhost:5000"

class TestPrescriptionIntegration(unittest.TestCase):
    
    def test_prescription_page_loads(self):
        """Test that the prescription page loads successfully"""
        response = requests.get(f"{BASE_URL}/prescription")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Medication Reminder System", response.text)
    
    def test_api_schedule(self):
        """Test that the API endpoint for scheduling reminders works"""
        # Test data
        test_data = {
            "email": "test@example.com",
            "medicines": [
                {
                    "name": "Test Medicine",
                    "dosage": "1 tablet daily",
                    "time": "08:00",
                    "days": 1
                }
            ]
        }
        
        # Send request to API endpoint
        response = requests.post(
            f"{BASE_URL}/api/schedule",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_data)
        )
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json()["status"])
    
    def test_prescription_link_in_chat(self):
        """Test that the Med Alert link is present in the chat page"""
        response = requests.get(f"{BASE_URL}/chat-with-faq")
        self.assertEqual(response.status_code, 200)
        self.assertIn('<a class="dropdown-item" href="/prescription"', response.text)
        self.assertIn('Med Alert', response.text)


if __name__ == "__main__":
    print("Running prescription integration tests...")
    print("Make sure your Flask application is running at", BASE_URL)
    print("Press Ctrl+C to cancel or any key to continue...")
    input()
    
    unittest.main() 