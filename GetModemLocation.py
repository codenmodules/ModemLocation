import subprocess
import requests, json

GOOGLE_KEY = "COPY_N_PASTE_YOUR_KEY_HERE"

def getLocationFromGoogle(cellId, locationAreaCode, mobileCountryCode, mobileNetworkCode):
	payload = {'considerIp':'false','cellTowers':[{'cellId': cellId,'locationAreaCode': locationAreaCode,'mobileCountryCode': mobileCountryCode,'mobileNetworkCode':mobileNetworkCode}]}
	jsonPayload = json.dumps(payload)
	headers = {'content-type': 'application/json'}
	url = "https://www.googleapis.com/geolocation/v1/geolocate?key=" + GOOGLE_KEY
	r = requests.post(url,data=jsonPayload,headers=headers)
	r.raise_for_status()
	response = json.loads(r.text)
	lat = response['location']['lat']
	lng = response['location']['lng']
	return lat, lng

def getMobileCountryCode():
	proc = subprocess.Popen(["mmcli -m 0 --location-get | grep 'Mobile country code' | awk '{print $7}'"], stdout=subprocess.PIPE, shell=True)
	(mcc_raw, err) = proc.communicate()
	return parseCommandLineValue(mcc_raw)

def getMobileNetworkCode():
	proc = subprocess.Popen(["mmcli -m 0 --location-get | grep 'Mobile network code' | awk '{print $5}'"], stdout=subprocess.PIPE, shell=True)
	(mnc_raw, err) = proc.communicate()
	return parseCommandLineValue(mnc_raw)

def getLocationAreaCode():
	proc = subprocess.Popen(["mmcli -m 0 --location-get | grep 'Location area code' | awk '{print $5}'"], stdout=subprocess.PIPE, shell=True)
	(lac_raw, err) = proc.communicate()
	return parseCommandLineValue(lac_raw)

def getCellId():
	proc = subprocess.Popen(["mmcli -m 0 --location-get | grep 'Cell ID' | awk '{print $4}'"], stdout=subprocess.PIPE, shell=True)
	(cellId_raw, err) = proc.communicate()
	return parseCommandLineValue(cellId_raw)

def parseCommandLineValue(value_raw):
	value = str(value_raw)[3:-4]
	return value

mcc = getMobileCountryCode()
mnc = getMobileNetworkCode()
lac = getLocationAreaCode()
cid = getCellId()

lat, lng = getLocationFromGoogle(cid, lac, mcc, mnc)

print("Latitud: %s Longitud: %s" %(lat,lng))






