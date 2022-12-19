
from flask import Flask, render_template, request, session, jsonify
import re
import mysql.connector as connection
import json
from datetime import date, datetime
from decimal import Decimal


mydb= connection.connect(host="localhost", database = 'Corteva',user="root", passwd="password@mysql",use_pure=True)
cur=mydb.cursor()

app = Flask(__name__)

@app.route('/api/weather',methods=['GET'])
def form1():
    return render_template('weather.html')

@app.route('/api/yield',methods=['GET'])
def form2():
    return render_template('yield.html')

@app.route('/api/weather/stats',methods=['GET'])
def form3():
    return render_template('weatherstats.html')


@app.route('/api/weather', methods = ['POST'])
def function1():

	if request.method == 'POST':
		station_id=request.form['Stationid']
		year=request.form['year']
		cur.execute("SELECT * FROM Weather where StationId= %s and YEAR(date)=%s", (station_id, year))
		row_headers=[x[0] for x in cur.description]	#Obtain the column names
		rv = cur.fetchall()
		json_data=[]
		for result in rv:
			json_data.append(dict(zip(row_headers,result)))

		#Converts the date format to json string to avoid serializability error
		#iterate throught the list and in each dictionary check if the values are date format if yes then covert to json string else continue
		for i in json_data:
			for k, v in i.items():
				if isinstance(v, date):
					i[k]=str(v)

		return jsonify(json_data)

@app.route('/api/yield', methods = ['POST'])
def function2():

	if request.method == 'POST':
		year=request.form['year']
		cur.execute("SELECT * FROM Yield where year=%s", (year,))
		row_headers=[x[0] for x in cur.description]	#Obtain the column names
		rv = cur.fetchall()
		json_data=[]
		for result in rv:
			json_data.append(dict(zip(row_headers,result)))
		
		return jsonify(json_data)

@app.route('/api/weather/stats', methods = ['POST'])
def function3():

	if request.method == 'POST':
		station_id=request.form['Stationid']
		year=request.form['year']
		cur.execute("SELECT * FROM Statistics where StationId= %s and year=%s", (station_id, year))
		row_headers=[x[0] for x in cur.description] #Obtain the column names
		rv = cur.fetchall()
		json_data=[]
		for result in rv:
			json_data.append(dict(zip(row_headers,result)))

		#Converts the date format to json string to avoid serializability error
		#iterate throught the list and in each dictionary check if the values are Decimal format 
		#if yes then covert to json float else continue
		
		for i in json_data:
			for k, v in i.items():
				if isinstance(v, Decimal):
					i[k]=float(v)

		return jsonify(json_data)


if __name__ == '__main__':
   app.run(debug=True)

