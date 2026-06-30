from app import create_app
app = create_app()
client = app.test_client()
resp = client.post('/login/staff', data={'email': 'staff@bcwd.in', 'password': 'staff123'}, follow_redirects=True)
with open('e:\\bcwd\\scratch\\staff_dashboard_test.html', 'w', encoding='utf-8') as f:
    f.write(resp.data.decode('utf-8'))
