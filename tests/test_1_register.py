import unittest
import requests
import json

URL = 'http://127.0.0.1:8082'
HEADER = {'Content-Type': 'application/json'} 
END_POINT = '/api/register'

class TestServer(unittest.TestCase):
	def register(self, teacher, students):
		return requests.post(url = URL + END_POINT, headers = HEADER, data = json.dumps(dict(teacher=teacher, students=students)))

	def invalid_key_register(self, teacher, students):
		return requests.post(url = URL + END_POINT, headers = HEADER, data = json.dumps(dict(teachers=teacher, student=students)))

	def invalid_len_register(self, teacher, students):
		return requests.post(url = URL + END_POINT, headers = HEADER, data = json.dumps(dict(teachers=teacher, student=students, extra="")))


	def test_normal_register(self):
		response = self.register("normalregisterteacher1@gmail.com",["student1@gmail.com","student2@gmail.com"])
		self.assertEqual(response.status_code, 204)
		response = self.register("normalregisterteacher2@gmail.com",["student3@gmail.com","student4@gmail.com"])
		self.assertEqual(response.status_code, 204)
		response = self.register("normalregisterteacher3@gmail.com",["student3@gmail.com","student4@gmail.com","student5@gmail.com"])
		self.assertEqual(response.status_code, 204)
		response = self.register("normalregisterteacher4@gmail.com",["student7@gmail.com","student8@gmail.com","student9@gmail.com"])
		self.assertEqual(response.status_code, 204)

	def test_normal_register_duplicate_teacher(self):
		response = self.register("normalregisterteacher1@gmail.com",["student3@gmail.com"])
		self.assertEqual(response.status_code, 204)

	def test_normal_register_duplicate_student(self):
		response = self.register("normalregisterteacher1@gmail.com",["student3@gmail.com","student3@gmail.com","student3@gmail.com"])
		self.assertEqual(response.status_code, 204)

	def test_invalid_httprequest(self):
		response = self.invalid_key_register("invalidrequestteacher@gmail.com",["student1@gmail.com","student2@gmail.com"])
		self.assertEqual(response.status_code, 404)
		response_json = json.loads(response.text)
		self.assertIn(response_json['message'], "Invalid Request!")
		response = self.invalid_len_register("invalidrequestteacher@gmail.com",["student1@gmail.com","student2@gmail.com"])
		self.assertEqual(response.status_code, 404)
		response_json = json.loads(response.text)
		self.assertIn(response_json['message'], "Invalid Request!")


		
if __name__ == '__main__':
    unittest.main(verbosity=2)
