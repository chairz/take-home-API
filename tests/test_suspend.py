import unittest
import requests
import json
import pymongo
mgc = pymongo.MongoClient(host='localhost', port=27017)
db = mgc.test
suspend_student_table = db.suspend_student_table
suspend_student_table.drop()

URL = 'http://127.0.0.1:8082'
HEADER = {'Content-Type': 'application/json'} 
END_POINT = '/api/suspend'

class TestServer(unittest.TestCase):
	def suspend(self, student):
		return requests.post(url = URL + END_POINT, headers = HEADER, data = json.dumps(dict(student=student)))

	def suspend_invalid(self, student):
		return requests.post(url = URL + END_POINT, headers = HEADER, data = json.dumps(dict(teacher=student)))

	def test_normal_suspend(self):
		response = self.suspend("student3@gmail.com")
		self.assertEqual(response.status_code, 204)

	def test_normal_suspend_duplicated(self):
		response = self.suspend("student3@gmail.com")
		response_json = json.loads(response.text)
		self.assertEqual(response.status_code, 200)
		self.assertIn(response_json['message'], "student:student3@gmail.com is already on suspension")

	def test_invalid_httprequest(self):
		response = self.suspend_invalid(["invalidrequeststudent@gmail.com"])
		response_json = json.loads(response.text)
		self.assertEqual(response.status_code, 404)
		self.assertIn(response_json['message'], "Invalid Request!")


if __name__ == '__main__':
    unittest.main(verbosity=2)