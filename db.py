import requests

base_path = "http://127.0.0.1:5000/api/"

def login(data):
    result = {}
    url = f"{base_path}login"
    response = requests.post(url, data=data)
    parsed_response = response.json()
    if response.status_code == 200:
        result["data"] = parsed_response.get('data')
    else:
        result["error_message"] = parsed_response.get('message')
    return result

def logout():
    url = f"{base_path}logout"
    response = requests.get(url)
    parsed_response = response.json()
    return parsed_response

def fetch_login_history(username=None, sort_order='Ascending'):
    result = {}
    url = f"{base_path}login_history"
    if username is not None:
        url += f"?search={username}&ordering={sort_order}"
    try:
        response = requests.get(url)
        parsed_response = response.json()
        if response.status_code == 200:
            result["data"] = parsed_response.get('data')
        else:
            result["error_message"] = parsed_response.get('message')
    except requests.exceptions.RequestException as e:
        result["error_message"] = f"Error in the request: {e}"
    return result

def create_customer(data):
    result = {}
    url = f"{base_path}create_customer"
    response = requests.post(url, data=data)
    parsed_response = response.json()
    if response.status_code == 201:
        result["data"] = parsed_response
    else:
        result["error_message"] = parsed_response.get('message')
    return result

def create_order(data):
    result = {}
    url = f"{base_path}create_order"
    response = requests.post(url, data=data)
    parsed_response = response.json()
    if response.status_code == 201:
        result["data"] = parsed_response
    else:
        result["error_message"] = parsed_response.get('message')
    return result

def fetch_all_services():
    result = {}
    url = f"{base_path}get_services"
    try:
        response = requests.get(url)
        parsed_response = response.json()
        if response.status_code == 200:
            result["data"] = parsed_response.get('data')
        else:
            result["error_message"] = parsed_response.get('message')
    except requests.exceptions.RequestException as e:
        result["error_message"] = f"Error in the request: {e}"
    return result

def fetch_customers_by_name(name = None):
    result = {}
    url = f"{base_path}get_customers_by_name?search={name}"
    try:
        response = requests.get(url)
        parsed_response = response.json()
        if response.status_code == 200:
            result["data"] = parsed_response.get('data')
        else:
            result["error_message"] = parsed_response.get('message')
    except requests.exceptions.RequestException as e:
        result["error_message"] = f"Error in the request: {e}"
    return result

def fetch_last_order_id():
    result = {}
    url = f"{base_path}get_last_order"
    response = requests.get(url)
    parsed_response = response.json()
    if response.status_code == 200:
        result["data"] = parsed_response.get('data') + 1
    elif response.status_code == 404:
        result["data"] = 1
    else:
        result["error_message"] = parsed_response.get('message')
    return result

def fetch_company_by_name(name = None):
    result = {}
    url = f"{base_path}get_company_by_name?name={name}"
    try:
        response = requests.get(url)
        parsed_response = response.json()
        if response.status_code == 200:
            result["data"] = parsed_response.get('data')
        else:
            result["error_message"] = parsed_response.get('message')
    except requests.exceptions.RequestException as e:
        result["error_message"] = f"Error in the request: {e}"
    return result

def fetch_services_by_period_and_customer(start_period, end_period, customer_id, company_name=None):
    result = {}
    url = f"{base_path}get_services_by_period_and_customer?start_period={start_period}&end_period={end_period}&customer_id={customer_id}&company_name={company_name}"
    try:
        response = requests.get(url)
        parsed_response = response.json()
        if response.status_code == 200:
            result["data"] = parsed_response.get('data')
        else:
            result["error_message"] = parsed_response.get('message')
    except requests.exceptions.RequestException as e:
        result["error_message"] = f"Error in the request: {e}"
    return result

def fetch_all_orders():
    result = {}
    url = f"{base_path}get_all_orders"
    response = requests.get(url)
    parsed_response = response.json()
    if response.status_code == 200:
        result["data"] = parsed_response.get('data')
    else:
        result["error_message"] = parsed_response.get('message')
    return result