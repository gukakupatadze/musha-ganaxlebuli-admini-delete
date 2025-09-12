#!/usr/bin/env python3
"""
Contact Messages API Testing - Focused Test
Tests the specific contact message functionality reported by user
"""

import requests
import json
from datetime import datetime

# Configuration
BACKEND_URL = "https://968cb362-65f1-44dd-8f2c-7082d694f9fb.preview.emergentagent.com/api"
TIMEOUT = 30

class ContactTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = TIMEOUT
        self.results = []
    
    def log_result(self, test_name, success, details="", response_data=None):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        if details:
            print(f"    Details: {details}")
        if response_data:
            print(f"    Response: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
        
        self.results.append({
            "test": test_name,
            "success": success,
            "details": details,
            "response": response_data
        })
    
    def test_get_contact_messages(self):
        """Test getting all contact messages"""
        print("\n=== Testing Contact Messages Retrieval ===")
        
        try:
            response = self.session.get(f"{BACKEND_URL}/contact/")
            if response.status_code == 200:
                messages = response.json()
                if isinstance(messages, list):
                    self.log_result(
                        "Get all contact messages", 
                        True, 
                        f"Found {len(messages)} messages"
                    )
                    return messages
                else:
                    self.log_result(
                        "Get all contact messages", 
                        False, 
                        "Response is not a list"
                    )
            else:
                self.log_result(
                    "Get all contact messages", 
                    False, 
                    f"Status code: {response.status_code}, Response: {response.text}"
                )
        except Exception as e:
            self.log_result(
                "Get all contact messages", 
                False, 
                f"Exception: {str(e)}"
            )
        
        return []
    
    def test_update_message_status(self, message_id, new_status):
        """Test updating a specific message status"""
        print(f"\n=== Testing Status Update: {message_id} -> {new_status} ===")
        
        try:
            # Test the correct endpoint that frontend uses
            response = self.session.put(
                f"{BACKEND_URL}/contact/{message_id}", 
                json={"status": new_status}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_result(
                        f"Update status to '{new_status}'", 
                        True, 
                        f"Status updated successfully",
                        data
                    )
                    return True
                else:
                    self.log_result(
                        f"Update status to '{new_status}'", 
                        False, 
                        f"Update failed: {data}",
                        data
                    )
            else:
                self.log_result(
                    f"Update status to '{new_status}'", 
                    False, 
                    f"Status code: {response.status_code}, Response: {response.text}"
                )
        except Exception as e:
            self.log_result(
                f"Update status to '{new_status}'", 
                False, 
                f"Exception: {str(e)}"
            )
        
        return False
    
    def test_contact_workflow(self):
        """Test the complete contact message workflow"""
        print("🚀 Starting Contact Messages API Tests")
        print(f"📍 Testing against: {BACKEND_URL}")
        print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Get all messages
        messages = self.test_get_contact_messages()
        
        if not messages:
            print("❌ No messages found to test status updates")
            return
        
        # Find messages with different statuses to test
        new_messages = [m for m in messages if m.get('status') == 'new']
        read_messages = [m for m in messages if m.get('status') == 'read']
        
        print(f"\n📊 Message Status Summary:")
        print(f"   Total messages: {len(messages)}")
        print(f"   New messages: {len(new_messages)}")
        print(f"   Read messages: {len(read_messages)}")
        
        # Test updating a 'new' message to 'read'
        if new_messages:
            message = new_messages[0]
            print(f"\n🔄 Testing 'წაკითხვა' (read) button functionality")
            print(f"   Message ID: {message['id']}")
            print(f"   From: {message['name']} ({message['email']})")
            print(f"   Subject: {message['subject']}")
            
            success = self.test_update_message_status(message['id'], 'read')
            
            if success:
                # Verify the update by fetching messages again
                updated_messages = self.test_get_contact_messages()
                updated_message = next((m for m in updated_messages if m['id'] == message['id']), None)
                
                if updated_message and updated_message['status'] == 'read':
                    self.log_result(
                        "Verify status update", 
                        True, 
                        f"Status correctly updated to 'read'"
                    )
                else:
                    self.log_result(
                        "Verify status update", 
                        False, 
                        f"Status not updated correctly. Current: {updated_message['status'] if updated_message else 'Message not found'}"
                    )
        
        # Test updating a message to 'replied'
        test_message = new_messages[1] if len(new_messages) > 1 else (read_messages[0] if read_messages else messages[0])
        
        if test_message:
            print(f"\n🔄 Testing 'პასუხი' (reply) button functionality")
            print(f"   Message ID: {test_message['id']}")
            print(f"   From: {test_message['name']} ({test_message['email']})")
            print(f"   Subject: {test_message['subject']}")
            
            success = self.test_update_message_status(test_message['id'], 'replied')
            
            if success:
                # Verify the update by fetching messages again
                updated_messages = self.test_get_contact_messages()
                updated_message = next((m for m in updated_messages if m['id'] == test_message['id']), None)
                
                if updated_message and updated_message['status'] == 'replied':
                    self.log_result(
                        "Verify reply status update", 
                        True, 
                        f"Status correctly updated to 'replied'"
                    )
                else:
                    self.log_result(
                        "Verify reply status update", 
                        False, 
                        f"Status not updated correctly. Current: {updated_message['status'] if updated_message else 'Message not found'}"
                    )
        
        # Test invalid message ID
        print(f"\n🔄 Testing invalid message ID")
        self.test_update_message_status("invalid-id-123", "read")
        
        # Print summary
        print("\n" + "="*60)
        print("📊 CONTACT TEST SUMMARY")
        print("="*60)
        
        passed = sum(1 for r in self.results if r['success'])
        total = len(self.results)
        
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {total - passed}")
        print(f"Success Rate: {(passed/total*100):.1f}%")
        
        failed_tests = [r for r in self.results if not r['success']]
        if failed_tests:
            print("\n🚨 FAILED TESTS:")
            for test in failed_tests:
                print(f"  • {test['test']}: {test['details']}")
        
        print(f"\n⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    tester = ContactTester()
    tester.test_contact_workflow()