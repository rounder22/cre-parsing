#!/usr/bin/env python3
"""
CRE Parser - Verification & Health Check Script
Verifies that all components are properly installed and configured
"""

import sys
import os

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("✗ Python 3.7+ required")
        return False
    return True

def check_imports():
    """Check all required imports"""
    packages = {
        'Flask': 'flask',
        'Flask-CORS': 'flask_cors',
        'python-docx': 'docx',
        'openpyxl': 'openpyxl',
        'pdfplumber': 'pdfplumber',
        'pandas': 'pandas',
        'Werkzeug': 'werkzeug',
    }
    
    all_good = True
    for name, module in packages.items():
        try:
            __import__(module)
            print(f"✓ {name}")
        except ImportError:
            print(f"✗ {name} - NOT INSTALLED")
            all_good = False
    
    return all_good

def check_file_structure():
    """Check project file structure"""
    required_files = [
        'app/__init__.py',
        'app/routes.py',
        'app/parsers/base_parser.py',
        'app/parsers/pdf_parser.py',
        'app/parsers/word_parser.py',
        'app/parsers/excel_parser.py',
        'app/parsers/extractor.py',
        'app/templates/index.html',
        'app/static/style.css',
        'app/static/script.js',
        'run.py',
        'requirements.txt',
        'README.md',
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - MISSING")
            all_exist = False
    
    return all_exist

def check_sample_files():
    """Check sample files"""
    samples = [
        'samples/Sample_CRE_Investment.docx',
        'samples/Sample_Financial_Model.xlsx',
    ]
    
    all_exist = True
    for sample in samples:
        if os.path.exists(sample):
            size = os.path.getsize(sample) / 1024
            print(f"✓ {sample} ({size:.1f} KB)")
        else:
            print(f"✗ {sample} - MISSING")
            all_exist = False
    
    return all_exist

def check_directories():
    """Check required directories"""
    dirs = [
        'uploads',
        'samples',
        'app',
        'app/parsers',
        'app/templates',
        'app/static',
    ]
    
    all_exist = True
    for dir in dirs:
        if os.path.isdir(dir):
            print(f"✓ {dir}/")
        else:
            print(f"✗ {dir}/ - MISSING")
            all_exist = False
    
    return all_exist

def check_app_initialization():
    """Test app initialization"""
    try:
        from app import create_app
        app = create_app()
        print("✓ Flask app initializes successfully")
        return True
    except Exception as e:
        print(f"✗ Flask app initialization failed: {str(e)}")
        return False

def check_parsers():
    """Test parser imports"""
    try:
        from app.parsers.pdf_parser import PDFParser
        from app.parsers.word_parser import WordParser
        from app.parsers.excel_parser import ExcelParser
        from app.parsers.extractor import DataExtractor
        print("✓ All parsers import correctly")
        return True
    except Exception as e:
        print(f"✗ Parser import failed: {str(e)}")
        return False

def main():
    print("\n" + "="*50)
    print("CRE PARSER - VERIFICATION SCRIPT")
    print("="*50 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Packages", check_imports),
        ("File Structure", check_file_structure),
        ("Required Directories", check_directories),
        ("Sample Files", check_sample_files),
        ("Parser Modules", check_parsers),
        ("Flask Application", check_app_initialization),
    ]
    
    results = {}
    for check_name, check_func in checks:
        print(f"\n{check_name}:")
        print("-" * 40)
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"✗ Error during check: {str(e)}")
            results[check_name] = False
    
    # Summary
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for check_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {check_name}")
    
    print(f"\nTotal: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n✓✓✓ All checks passed! Ready to run application ✓✓✓")
        print("\nStart the application with: python run.py")
        print("Access at: http://localhost:5000")
        return 0
    else:
        print(f"\n✗ {total - passed} check(s) failed. Please fix issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
