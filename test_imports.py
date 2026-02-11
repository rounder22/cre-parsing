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

try:
    from app.routes import main_bp, upload_bp
    print("✓ Routes imported successfully")
except Exception as e:
    print(f"✗ Error importing routes: {e}")
    import traceback
    traceback.print_exc()

try:
    from app import create_app
    print("✓ create_app imported successfully")
    app = create_app()
    print("✓ create_app() executed successfully")
except Exception as e:
    print(f"✗ Error with create_app: {e}")
    import traceback
    traceback.print_exc()
