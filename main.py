import datetime
import requests
import json


def getToken(userName, password):
    url = "https://developers.3dsignals.io/api/v1/security/getAPIToken"
    payload = json.dumps({
        "userEmail": userName,
        "password": password
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response


def getMachines(token):
    url = "https://developers.3dsignals.io/api/v1/machineInfo"
    payload = ""
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    return response


def getMachinesActivity(token, start_time, end_time, machine_id):
    url = "https://developers.3dsignals.io/api/v1/machineActivity"
    payload = json.dumps({
        "startTime": start_time.timestamp(),
        "endTime": end_time.timestamp(),
        "machineId": machine_id
    })
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response


if __name__ == '__main__':

    print("****** 3d Signals ***** \n Welcome to Machine activity Python script")

    # First- get the token access key
    token_response = getToken("*********", "**********")
    if token_response.status_code != 200:
        exit(1)

    token = json.loads(token_response.text)
    token = token['token']

    # get the permitted machines for that user
    machines_response = getMachines(token)
    if machines_response.status_code != 200:
        exit(1)
    machines = json.loads(machines_response.text)
    machines = machines["machines"]

    # select randomly one of the machines -> lets pick the first one
    machine_id = machines[0]["machineUniqueId"]

    # define the period of the query -> lets take the last 24 H
    start_time = datetime.datetime.now() - datetime.timedelta(days=1)
    end_time = datetime.datetime.now() - datetime.timedelta(minutes=5)

    machine_activity_response = getMachinesActivity(token, start_time, end_time, machine_id)
    if machine_activity_response.status_code != 200:
        exit(1)

print("****** 3d Signals ***** \n Machine activity Python script ended successful ")
