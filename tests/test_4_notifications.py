import unittest
import requests
import json

URL = 'http://127.0.0.1:8082'
HEADER = {'Content-Type': 'application/json'} 
END_POINT = '/api/retrievefornotifications'

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

mongodb suspend table after suspend
{
	"_id" : ObjectId("5f97cf403d114c95ba5b7e93"),
	"student" : "student3@gmail.com"
}
'''

class TestServer(unittest.TestCase):
	def notifications(self, teacher, notification):
		return requests.post(url = URL + END_POINT, headers = HEADER, data = json.dumps(dict(teacher=teacher, notification=notification)))

	def notifications_invalid(self, teacher, notification):
		return requests.post(url = URL + END_POINT, headers = HEADER, data = json.dumps(dict(invalid_key=teacher, notification=notification)))

	def test_normal_notifications(self):
		response = self.notifications("normalregisterteacher4@gmail.com","hello students! welcome to unit test! @student7@gmail.com")
		response_json = json.loads(response.text)
		expected = ["student7@gmail.com","student8@gmail.com","student9@gmail.com"]
		response_json['recipents'].sort()
		self.assertEqual(response.status_code, 200)
		self.assertListEqual(response_json['recipents'], expected)

	def test_suspend_student_notifications(self):
		response = self.notifications("normalregisterteacher1@gmail.com","hello students! welcome to unit test!")
		response_json = json.loads(response.text)
		expected = ["student1@gmail.com","student2@gmail.com"]
		response_json['recipents'].sort()
		self.assertEqual(response.status_code, 200)
		self.assertListEqual(response_json['recipents'], expected)

	def test_mention_student_notifications(self):
		response = self.notifications("normalregisterteacher1@gmail.com","hello students! welcome to unit test! @student7@gmail.com @student8@gmail.com")
		response_json = json.loads(response.text)
		expected = ["student1@gmail.com","student2@gmail.com", "student7@gmail.com", "student8@gmail.com"]
		response_json['recipents'].sort()
		self.assertEqual(response.status_code, 200)
		self.assertListEqual(response_json['recipents'], expected)

	def test_special_keyword_notifications(self):
		response = self.notifications("normalregisterteacher1@gmail.com","hello students! See me @ classroom @ 930am. @student7@gmail.com @student8@gmail.com")
		response_json = json.loads(response.text)
		expected = ["student1@gmail.com","student2@gmail.com", "student7@gmail.com", "student8@gmail.com"]
		response_json['recipents'].sort()
		self.assertEqual(response.status_code, 200)
		self.assertListEqual(response_json['recipents'], expected)

	def test_not_registered_teacher_notifications(self):
		response = self.notifications("notregisterteacher1@gmail.com","hello students! See me @ classroom @ 930am. @student7@gmail.com @student8@gmail.com")
		response_json = json.loads(response.text)
		expected = "teacher:notregisterteacher1@gmail.com has not been registered!"
		self.assertEqual(response.status_code, 404)
		self.assertIn(response_json['message'], expected)

	def test_invalid_httprequest(self):
		response = self.notifications_invalid("normalregisterteacher1@gmail.com","hello students! welcome to unit test!")
		response_json = json.loads(response.text)
		self.assertEqual(response.status_code, 404)
		self.assertIn(response_json['message'], "Invalid Request!")




if __name__ == '__main__':
    unittest.main(verbosity=2)