from flask import Flask, request, jsonify, current_app, make_response, send_file, copy_current_request_context
import pymongo
import json


mgc = pymongo.MongoClient(host='localhost', port=27017)
db = mgc.test
teacher_student_table = db.teacher_student_table
suspend_student_table = db.suspend_student_table
#teacher_student_table.drop()
#suspend_student_table.drop()

app = Flask(__name__)

@app.route('/api/register', methods=['POST'])
def register():
	register_form = request.json
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
	return json.dumps({'message':'success'}), 204

@app.route('/api/commonstudents', methods=['GET'])
def retrieve():
	teacher_list = request.args.getlist('teacher')
	common_students = []

	#given a list of teachers, find intersection using set to get common students
	for teacher in teacher_list:
		result = teacher_student_table.find_one({'teacher': teacher})
		if not result:
			return json.dumps({'message':'No such teacher:{} is registered!'.format(teacher)}), 404
		if common_students == []:
			common_students = result['students']
		else:
			common_students = set(common_students) & set(result['students'])

	if len(list(common_students)) == 0:
		return json.dumps({'message':'No common students found!'.format(teacher)}), 200

	return json.dumps({'students':list(common_students)}), 200

@app.route('/api/suspend', methods=['POST'])
def suspend():
	suspend_form = request.json

	#check if the student has already been suspended to avoid duplicate entries
	result = suspend_student_table.find_one({'student':suspend_form['student']})
	if result:
		return json.dumps({'message':'student:{} has already been suspended before'.format(suspend_form['student'])}), 204

	suspend_student_table.insert_one({'student':suspend_form['student']})
	return json.dumps({'message':'success'}), 204

@app.route('/api/retrievefornotifications', methods=['POST'])
def notifications():
	pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8082)