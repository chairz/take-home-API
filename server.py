from flask import Flask, request, jsonify
import pymongo
import json
import re

mgc = pymongo.MongoClient(host='localhost', port=27017)
db = mgc.test
teacher_student_table = db.teacher_student_table
suspend_student_table = db.suspend_student_table
teacher_student_table.drop()
suspend_student_table.drop()

app = Flask(__name__)

@app.route('/api/register', methods=['POST'])
def register():
	register_form = request.json
	if 'teacher' not in register_form or 'students' not in register_form or len(register_form) != 2 :
		return jsonify({'message':'Invalid Request!'}), 404 

	result = teacher_student_table.find_one({'teacher':register_form['teacher']})
	if not result:
		record = {'teacher': register_form['teacher'], 'students': register_form['students']}
		teacher_student_table.insert_one(record)
	else:
		current_student_info = result['students']

		#update in mongo replaces instead of append, therefore manual append and remove duplicates
		unique_student_info = set(current_student_info + register_form['students'])
		teacher_student_table.update_one({'students': current_student_info}, 
										 {"$set": {'students':list(unique_student_info)}})
	return jsonify({'message':'success'}), 204

@app.route('/api/commonstudents', methods=['GET'])
def retrieve():
	teacher_list = request.args.getlist('teacher')
	if not teacher_list:
		return jsonify({'message':'Invalid Request!'}), 404 

	common_students = []

	#given a list of teachers, find intersection using set to get common students
	for teacher in teacher_list:
		result = teacher_student_table.find_one({'teacher': teacher})
		if not result:
			return jsonify({'message':'teacher:{} has not been registered!'.format(teacher)}), 404
		if common_students == []:
			common_students = result['students']
		else:
			common_students = set(common_students) & set(result['students'])


	return jsonify({'students':list(common_students)}), 200

@app.route('/api/suspend', methods=['POST'])
def suspend():
	suspend_form = request.json
	if 'student' not in suspend_form:
		return jsonify({'message':'Invalid Request!'}), 404 

	#check if the student has already been suspended to avoid duplicate entries
	result = suspend_student_table.find_one({'student':suspend_form['student']})
	if result:
		return jsonify({'message':'student:{} is already on suspension'.format(suspend_form['student'])}), 200

	suspend_student_table.insert_one({'student':suspend_form['student']})
	return jsonify({'message':'success'}), 204

@app.route('/api/retrievefornotifications', methods=['POST'])
def notifications():
	notification_form = request.json
	if 'teacher' not in notification_form or 'notification' not in notification_form:
		return jsonify({'message':'Invalid Request!'}), 404

	result = teacher_student_table.find_one({'teacher':notification_form['teacher']})
	if not result:
		return jsonify({'message':'teacher:{} has not been registered!'.format(notification_form['teacher'])}), 404
	students = result['students']
	notification = notification_form['notification']

	#get mention from notifications and concentanate the list to the registered student list and remove suspended students
	metioned_list = handle_notification(notification)
	students = remove_suspended_student(students + metioned_list)

	#remove possible duplicates caused by mentioning and being in registered list of the teacher
	students = list(set(students))

	return jsonify({'recipents':students}), 200

def handle_notification(notification):
	matches = re.findall(r'\s+@[\w\.]+@[\w\.]+', notification)
	result = []
	for match in matches:
		result.append(match.lstrip()[1:])
	return result

def remove_suspended_student(students):
	for student in students:
		result = suspend_student_table.find_one({'student':student})
		if result:
			students.remove(student)
	return students

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=8082)