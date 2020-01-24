#!/usr/bin/env python
#
# The script is using Aruba Central APIs to extract AP information 
# and modify the AP name by user request.
#
# Pre-request: Installed Python 3.6+
#			   Install pip	(execute script get-pip.py)
#			   pip install requests
#
# Parameter Input: 
#		Token, AP Serial Number
#		AP Name prefix 
#
# Function:
#		To change the AP name	
#		


# Importing the requests library 
import requests
import json
import sys
import os

# User Token given here 
token = "SpAnkAZgIlY32hyyNLcTXRYxXLLYTH1k"

prefix = "AP-"

def getAPInfo(serialID):

	
	getURL = "https://apigw-ca.central.arubanetworks.com/monitoring/v1/aps/"

	# API-endpoint 
	getURL = getURL + serialID
	
	# Defining a params dict for the parameters to be sent to the API 
	PARAMS = {'access_token':token}
	
	# Sending get request and saving the response as response object 
	req = requests.get(url = getURL, params = PARAMS) 
	
	if (req.status_code != 200):
	
		Error_code = str (req.status_code)
		print ("Request AP Information Failed! Error Code: " + Error_code)
		
		## print (req.status_code)
		if req.status_code == 401 :
			print ("Unauthorized access, Please check your token!")
		
	# Extracting data in Json format 
	apData = req.json() 
	apInfo = {"name": apData['name'], "macaddr": apData['macaddr'], "ip_address": apData['ip_address']}

	# print (req)
	print ("")
	print ("Checking AP serial number " + serialID + ", found the info below:")
	
	print ("AP Name        : " + apInfo['name'])
	print ("AP Mac Address : " + apInfo['macaddr'])
	print ("AP IP Address  : " + apInfo['ip_address'])
	
	return apInfo
	
def changeAPName(serialID, hostname, ip_address, inputParam):

	postURL = "https://apigw-ca.central.arubanetworks.com/configuration/v1/ap_settings/"+serialID
	postURL = postURL + "?access_token=" + token

	apChanged = {}
	
	# hostName = prefix + ip_address.split('.')[3]

	if inputParam == 'file' :
	
		while 1:
			hostName = hostname
			
			print ("AP " + serialID + " with IP: " + ip_address + " will be renamed to: " + hostName)
			response = input ("Press 'y' to continue, press 'n' to change the name: ")
			
			if (response == 'y' or response =='n'):
				if response == 'y':
					hostName = hostname
				
				else:
					hostName = input("Please provide the name for " + serialID + ": ")
			
				newName = {"hostname": hostName, "ip_address": ip_address}
				newNameJson = json.dumps(newName)
				headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
				put = requests.post(postURL, data=json.dumps(newName), headers=headers)
			
				if put.status_code ==200:
					print ("The name of " + serialID + " changed to " + hostName)
					apChanged = {"serialID": serialID, "name": hostName, "ip_address": ip_address}					
				break
				
			else:
				print ("Please choose 'y' or 'n' ...")
				
	elif inputParam == 'manually':
	
		hostName = prefix + ip_address.split('.')[3]
		
		print ("AP " + serialID + " with IP: " + ip_address + " will be renamed to: " + hostName)
		response = input ("Press Enter to continue, press 'n' to change the name: ")
		
		if response == 'y':
			hostName = prefix + ip_address.split('.')[3]
		
		if response == 'n':
			hostName = input("Please provide the name for " + serialID + ": ")

		newName = {"hostname": hostName, "ip_address": ip_address}
		newNameJson = json.dumps(newName)
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		put = requests.post(postURL, data=json.dumps(newName), headers=headers)
		
		if put.status_code ==200:
			print ("The name of " + serialID + " changed to " + hostName)
			print ("")
			
			apChanged = {"serialID": serialID, "name": hostName, "ip_address": ip_address}			
	
	return apChanged
		
	
if __name__ == "__main__":
	
	print ("")
	print ("==========This Script is for changing AP Name==========")
	print ("Choose 1 to provide the AP List file ...")
	print ("Choose 2 to input AP serial ID manually ...")
	userInput = input("Please choose 1 or 2: ")
	
	if userInput == "1":		
	
		apFile = input ("Please provide AP file name: ") 
		# print (apFile)
		
		apList = open(apFile, "r")
		
		for line in apList:
			fields = line.strip('\n').split(",")
			
			serialNum = fields[0]            
			apNewName = fields[1]

			print ("... ... ... ... ....")
			print ("... ... ... ... ....")
			
			apDetails = {}
			apDetails = getAPInfo(serialNum.strip())
			# print (apDetails)
					
			apChangedDetails = changeAPName(serialNum.strip(), apNewName, apDetails['ip_address'], "file")

			with open ("original_AP_Info.txt","a") as orginalAPList:
				
				apInfoStr = (apDetails['name'] + ',' + apDetails['macaddr'] + ',' + apDetails['ip_address'])
				orginalAPList.write(apInfoStr + os.linesep)
				
			with open ("changed_AP_Info.txt","a") as changedAPList:
			
				apChangedStr = (apChangedDetails['serialID'] + ',' + apChangedDetails['name'] + ',' + apChangedDetails['ip_address'])
				changedAPList.write(apChangedStr + os.linesep)
				
			orginalAPList.close
			changedAPList.close
			
		apList.close
		
		print ("")
		print ("All the APs haven processed, the program has been terminated !!!")
	
	if userInput == "2":
		
		while 1:
			serialInput = input ("Please provide the AP serial ID, type 'quit' to exit: ") 	

			print ("... ... ... ... ....")
			print ("... ... ... ... ....")
			
			if serialInput == "quit":
				print ("")
				print ("The program has been terminated. Thanks")
				sys.exit()
				
			else:
				apDetails = {}
				apDetails = getAPInfo(serialInput.strip())	
				
				apChangedDetails = changeAPName(serialInput.strip(), apDetails['name'], apDetails['ip_address'], "manually")			
			
				with open ("originalMan_AP_Info.txt","a") as orginalAPList:
					
					apInfoStr = (apDetails['name'] + ',' + apDetails['macaddr'] + ',' + apDetails['ip_address'])
					orginalAPList.write(apInfoStr + os.linesep)
					
				with open ("changedMan_AP_Info_m.txt","a") as changedAPList:
				
					apChangedStr = (apChangedDetails['name'] + ',' + apChangedDetails['serialID'] + ',' + apChangedDetails['ip_address'])
					changedAPList.write(apChangedStr + os.linesep)
							
					## changeAPName(serialInput.strip(), apDetails['name'], apDetails['ip_address'])			
				
				orginalAPList.close
				changedAPList.close
	
