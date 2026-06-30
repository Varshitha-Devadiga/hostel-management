import requests
from bs4 import BeautifulSoup

session = requests.Session()
# Get registration page to fetch CSRF token
url = 'http://127.0.0.1:5000/register/student'
resp = session.get(url)
resp.raise_for_status()
# Parse CSRF token
soup = BeautifulSoup(resp.text, 'html.parser')
csrf_input = soup.find('input', {'name': 'csrf_token'})
csrf_token = csrf_input['value'] if csrf_input else ''
# Prepare form data
data = {
    'email': 'test_student@example.com',
    'password': 'TestPass123',
    'confirm_password': 'TestPass123',
    'csrf_token': csrf_token,
    'submit': 'Register'
}
post_resp = session.post(url, data=data)
print('Status Code:', post_resp.status_code)
print('Redirected to:', post_resp.url)
print('Response Text (first 500 chars):', post_resp.text[:500])
