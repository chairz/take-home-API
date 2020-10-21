from flask import Flask, request, jsonify, current_app, make_response, send_file, copy_current_request_context
import pymongo
import json


mgc = pymongo.MongoClient(host='localhost', port=27017)
db = mgc.test
teacher_student_table = db.teacher_student_table
#teacher_student_table.drop()

app = Flask(__name__)

@app.route('/api/register', methods=['POST'])
def register():
	register_form = request.json
	result = teacher_student_table.find_one({'teacher':register_form['teacher']})
	print(result)
	if not result:
		record = {'teacher': register_form['teacher'], 'students': register_form['students']}
		teacher_student_table.insert_one(record)
	else:
		print(result['_id'])
		current_student_info = result['students']
		#update in mongo replaces instead of append, therefore manual append and remove duplicates
		unique_student_info = set(current_student_info + register_form['students'])
		print(unique_student_info)
		teacher_student_table.update_one({'students': current_student_info}, 
										 {"$set": {'students':list(unique_student_info)}})
	return 'success', 204

@app.route('/api/commonstudents', methods=['GET'])
def retrieve():
	pass

@app.route('/api/suspend', methods=['POST'])
def suspend():
	pass

@app.route('/api/retrievefornotifications', methods=['POST'])
def notifications():
	pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8082)