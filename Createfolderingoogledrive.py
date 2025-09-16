import requests
from inspect import getframeinfo, stack
from requests.auth import HTTPBasicAuth
import re
import datetime
import os
import sys
import json

ACCESS_TOKEN = re.sub(r'^"|"$', '', r'''[*ACCESS_TOKEN*]''')
FOLDER_NAME = re.sub(r'^"|"$', '', r'''[*FOLDER_NAME*]''') 

def LogMessage(ErrType, code, Message, RaisedExc=None):

    '''
        Function: LogMessage

        .SYNOPSIS:
            This module is used for printing error message on the screen

        .DESCRIPTION:
            This module will help in printing the verbose message or log error message on screen

        .DEPENDENCIES/ENVIRONMENT:
            + module required: 1. python module: inspect, datetime, os, sys
                               2. Summit ORCH Module: None
            + python version: 3


        .PARAMETER ALL:
            [string] (Mandatory) ErrType: type of error key word(Error/Exception:ERR, Information:INF)
            [string] (Mandatory) code: Specific code for the error message
            [string] (Mandatory) Message: Log Message
            [Object] (Optional) RaisedExc: Exception Object

        .OUTPUTS:
            no return value

        .EXAMPLE:
            LogMessage('INF',"[0-00-000-0000]", "Message to be logged")
            LogMessage('ERR',"[0-00-000-0000]", "Message to be logged")
            LogMessage('ERR',"[0-00-000-0000]", "Message to be logged", ExceptionObject)

        .NOTES: None

        .VERSION HISTORY:
            v1.0 - Initial Version
    '''

    # getting calling module details
    caller = getframeinfo(stack()[1][0])

    # Module_Name = caller.filename + "\\" + stack()[1][3]
    # Module_Name = stack()[1].function

    Module_Name = stack()[1][3]

    linenumber = str(caller.lineno)
    date = str(datetime.datetime.utcnow())[0:19]

    # information logging
    if (ErrType == 'INF'):
        print("\n[{0}] INF{1}: [{2}| Line {3}] : {4}".format(date, code, Module_Name, linenumber, Message))

    # information logging
    elif ErrType == 'ERR':
        # error with exception
        if RaisedExc is not None:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            linenumber = exc_tb.tb_lineno
            print("\n[{0}] ERR{1}: [{2}| Line {3}] : {4}, {5},{6}".format(date, code, Module_Name, linenumber, Message,
                                                                          str(RaisedExc), exc_type))
        # user defined error
        else:
            print("\n[{0}] ERR{1}: [{2}| Line {3}] : {4}".format(date, code, Module_Name, linenumber, Message))

    # information logging other than ERR and INF
    else:
        print("\n[{0}] {1}{2}: [{3}| Line {4}] : {5}".format(date, ErrType, code, Module_Name, linenumber, Message))
def main():
    try:  
        url = "https://www.googleapis.com/drive/v3/files"
        # Headers for authentication and content type
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        # Folder metadata
        data = {
            "name": FOLDER_NAME,
            "mimeType": "application/vnd.google-apps.folder"  # Important: This tells Google Drive it's a folder
        }

        # Make a POST request to create the folder
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            folder_id = response.json().get("id")
            print(folder_id)
            LogMessage('INF', "[0-00-0000-0000]",'Folder created successfully.')
            LogMessage('INF', "[0-00-0000-0000]","Script executed successfully.")
        else:
            LogMessage('ERR', "[1-01-000-9999]", "Failed to create folder.")
            print(f"Status Code: {response.status_code}")
            print("Error:", response.text)
            LogMessage('ERR', "[1-01-000-9999]", "Script Execution Failed")
            return
                
    except Exception as e:
            FailureMessage = f"Error - {str(e)}"
            LogMessage('ERR', "[1-01-000-9999]", FailureMessage)
            LogMessage('ERR', "[1-01-000-9999]", "Failed to create folder.")
            LogMessage('ERR', "[1-01-000-9999]", "Script Execution Failed unfortunatly.")
if __name__ == "__main__":
    main()

