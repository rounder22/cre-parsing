import sys
sys.path.insert(0, 'C:\\Github\\cre-parsing')

print("Starting imports...")
try:
    from app.parsers.extractor import DataExtractor
    print("✓ DataExtractor imported successfully")
except Exception as e:
    print(f"✗ Error importing DataExtractor: {e}")
    import traceback
    traceback.print_exc()

try:
    from app.config import Config
    print("✓ Config imported successfully")
except Exception as e:
    print(f"✗ Error importing Config: {e}")
    import traceback
    traceback.print_exc()

try:
    from app.routes import main_bp, upload_bp
    print("✓ Routes imported successfully")
except Exception as e:
    print(f"✗ Error importing routes: {e}")
    import traceback
    traceback.print_exc()

print("\nAttempting to create app...")
try:
    from app import create_app
    print("✓ create_app imported successfully")
    app = create_app()
    print("✓ create_app() executed successfully")
    
    print("\nTesting routes...")
    with app.test_client() as client:
        print("Testing GET /")
        response = client.get('/')
        print(f"  Status: {response.status_code}")
        if response.status_code != 200:
            print(f"  Response: {response.data[:500]}")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
