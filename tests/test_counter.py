"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app 

# we need to import the file that contains the status codes
from src import status 

class CounterTest(TestCase):
    """Counter tests"""

    def setUp(self):
      self.client = app.test_client()

    def test_create_a_counter(self):
        """It should create a counter"""
        client = app.test_client()
        result = client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """It should update a counter"""
        result = self.client.post('/counters/generic')                  # Create a counter
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)   # Ensure successful return code
        counterValue = result.get_json()['generic']                     # Save baseline value

        result = self.client.put('/counters/generic')                   # Update the counter
        self.assertEqual(result.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT], True)   # Ensure successful return code
        counterValueUpdate = result.get_json()['generic']               # Save new value

        self.assertEqual(counterValueUpdate, (counterValue + 1))        # Ensure counter was updated

        result = self.client.put('/counters/newCounter')                # Should create a new counter if it doesnt exist
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)   # Check if counter was created

    def test_read_a_counter(self):
        """It should read a counter"""
        self.client.post('/counters/bob')                               # Create a counter
        read = self.client.get('/counters/bob')                         # Read a counter
        self.assertEqual(read.status_code, status.HTTP_200_OK)          # Ensure successful return code
        result = self.client.get('/counters/unrealCounter')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND) # If object doesn't exist, should return error

    def test_delete_a_counter(self):
        """It should delete a counter"""
        self.client.post('/counters/dave')                              # Create a counter
        result = self.client.delete('/counters/dave')                   # Delete the counter
        self.assertEqual(result.status_code, status.HTTP_204_NO_CONTENT)# Ensure successful return code for delete
        result = self.client.delete('/counters/dave')                   # Try to delete the deleted counter
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND) # Ensure correct error appears


