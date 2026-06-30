"""Diagnose the 500 error by testing the app startup and route rendering."""
import traceback
import sys

try:
    print("1. Importing create_app...")
    from app import create_app
    print("   OK")

    print("2. Creating app...")
    app = create_app()
    print("   OK")

    print("3. Listing registered routes...")
    with app.app_context():
        for rule in app.url_map.iter_rules():
            print(f"   {rule.rule} -> {rule.endpoint}")

    print("\n4. Testing GET /register/student/wizard ...")
    with app.test_client() as client:
        resp = client.get('/register/student/wizard')
        print(f"   Status: {resp.status_code}")
        if resp.status_code != 200:
            print(f"   Response data (first 2000 chars):")
            print(resp.data.decode('utf-8', errors='replace')[:2000])

    print("\nDone. If status was 200, the page loads fine.")

except Exception as e:
    print(f"\n*** ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)
