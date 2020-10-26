import unittest
import requests
import json

URL = 'http://127.0.0.1:8082'
HEADER = {'Content-Type': 'application/json'} 
END_POINT = '/api/commonstudents?'

'''
mongodb teacher_student table after test_register
{
	"_id" : ObjectId("5f96d17bff3e36e59c70d84a"),
	"teacher" : "normalregisterteacher1@gmail.com",
	"students" : [
		"student1@gmail.com",
		"student3@gmail.com",
		"student2@gmail.com"
	]
}
{
	"_id" : ObjectId("5f96d17bff3e36e59c70d84b"),
	"teacher" : "normalregisterteacher2@gmail.com",
	"students" : [
		"student3@gmail.com",
		"student4@gmail.com"
	]
}
{
	"_id" : ObjectId("5f96d17bff3e36e59c70d84c"),
	"teacher" : "normalregisterteacher3@gmail.com",
	"students" : [
		"student3@gmail.com",
		"student4@gmail.com",
		"student5@gmail.com"
	]
}
{
	"_id" : ObjectId("5f96d54560017378ca80f4c6"),
	"teacher" : "normalregisterteacher4@gmail.com",
	"students" : [
		"student7@gmail.com",
		"student8@gmail.com",
		"student9@gmail.com"
	]
}
'''

class TestServer(unittest.TestCase):
	def retrieve(self, teachers):
		query = ""
		for teacher in teachers:
			query += 'teacher=' + teacher + '&'
		query = query[:-1]
		return requests.get(url = URL + END_POINT + query)

	def retrieve_invalid(self, teachers):
		query = ""
		for teacher in teachers:
			query += 'principal=' + teacher + '&'
		query = query[:-1]
		return requests.get(url = URL + END_POINT + query)

	def test_retreive_one_common_students(self):
		response = self.retrieve(["normalregisterteacher1@gmail.com", "normalregisterteacher2@gmail.com", "normalregisterteacher3@gmail.com"])
		response_json = json.loads(response.text)
		self.assertEqual(response.status_code, 200)
		expected = ["student3@gmail.com"]
		response_json['students'].sort()
		self.assertListEqual(response_json['students'], expected)

	def test_retreive_two_common_students(self):
		response = self.retrieve(["normalregisterteacher2@gmail.com", "normalregisterteacher3@gmail.com"])
		response_json = json.loads(response.text)
		self.assertEqual(response.status_code, 200)
		expected = ["student3@gmail.com","student4@gmail.com"]
		response_json['students'].sort()
		self.assertListEqual(response_json['students'], expected)

	def test_retreive_zero_common_students(self):
		response = self.retrieve(["normalregisterteacher1@gmail.com", "normalregisterteacher2@gmail.com", "normalregisterteacher4@gmail.com", "normalregisterteacher4@gmail.com"])
		response_json = json.loads(response.text)
		self.assertEqual(response.status_code, 200)
		expected = []
		response_json['students'].sort()
		self.assertListEqual(response_json['students'], expected)

	def test_invalid_teacher(self):
		response = self.retrieve(["nosuchteacher@gmail.com"])
		response_json = json.loads(response.text)
		self.assertEqual(response.status_code, 404)
		self.assertIn(response_json['message'], "teacher:nosuchteacher@gmail.com has not been registered!")

	def test_invalid_httprequest(self):
		response = self.retrieve_invalid(["invalidrequestteacher@gmail.com"])
		response_json = json.loads(response.text)
		self.assertEqual(response.status_code, 404)
		self.assertIn(response_json['message'], "Invalid Request!")



if __name__ == '__main__':
    unittest.main(verbosity=2)