#
# The original code for this example is credited to S. Subramanian,
# from this post on DZone: https://dzone.com/articles/restful-web-services-with-python-flask
#

from flask import Flask
from flask import jsonify
from flask import request
from flask import abort
import requests
from const import *
import atexit

app = Flask(__name__)

empDB=[
 {
 'id':'101',
 'name':'Arício Segundo',
 'title':'Technical Leader',
 'salary': '2000'
 },
 {
 'id':'201',
 'name':'Geraldo Rusmão',
 'title':'Sr Software Engineer',
 'salary': '3000'
 }
 ]

@app.route('/empdb/employee',methods=['GET'])
def getAllEmp():
    return jsonify({'emps':empDB})

@app.route('/empdb/employee/<empId>',methods=['GET'])
def getEmp(empId):
    usr = [ emp for emp in empDB if (emp['id'] == empId) ] 
    return jsonify({'emp':usr})

@app.route('/empdb/employee/salary/mean', methods=['GET'])
def getSalaryMean():
    salaries = list(map(lambda x: float(x['salary']), empDB))
    salaryMean = sum(salaries) / len(salaries)
    return jsonify({'salaryMean': salaryMean})

@app.route('/empdb/employee/<empId>',methods=['PUT'])
def updateEmp(empId):

    em = [ emp for emp in empDB if (emp['id'] == empId) ]

    if len(em) > 0:
        if 'name' in request.json : 
            em[0]['name'] = request.json['name']

        if 'title' in request.json:
            em[0]['title'] = request.json['title']

    return jsonify(em)

@app.route('/empdb/employee/<empId>/<empSal>',methods=['PUT'])
def updateEmpSal(empId,empSal):
    em = [ emp for emp in empDB if (emp['id'] == empId) ]
    em[0]['salary'] = empSal
    return jsonify(em)

@app.route('/empdb/employee/salary/raise', methods=['PUT'])
def giveSalaryRaise():
    args = request.args
    percentage = float(args.get('percentage'))
    for emp in empDB:
        emp['salary'] = str(float(emp['salary']) * (1 + (percentage/100)))
    return ('', 204)
   
@app.route('/empdb/employee',methods=['POST'])
def createEmp():

    dat = {
    'id':request.json['id'],
    'name':request.json['name'],
    'title':request.json['title']
    }
    empDB.append(dat)
    return jsonify(dat)

@app.route('/empdb/employee/<empId>',methods=['DELETE'])
def deleteEmp(empId):
    em = [ emp for emp in empDB if (emp['id'] == empId) ]

    if len(em) > 0:
        empDB.remove(em[0])
        return jsonify({'response':'Success'})
    else:
        return jsonify({'response':'Failure'})
    
def register_service():
    requests.post(DNS_IP + '/register', json={'serviceName': SERVICE_NAME, 'url': get_ip() + ':4567'}) 

def unregister_service():
    payload = {'serviceName': SERVICE_NAME}
    requests.delete(DNS_IP + '/unregister', params=payload)

def get_ip():
    response = requests.get('https://httpbin.org/get')
    return response.json()['origin']

atexit.register(unregister_service)

if __name__ == '__main__':
 with app.app_context():
    register_service()
 app.run(host='0.0.0.0', port=PORT)
     
