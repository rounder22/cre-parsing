from flask import Blueprint, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from app.parsers.extractor import DataExtractor
from app.config import Config
import json

main_bp = Blueprint('main', __name__)
upload_bp = Blueprint('upload', __name__, url_prefix='/api')

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_type(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    if ext == 'pdf':
        return 'pdf'
    elif ext == 'docx':
        return 'word'
    elif ext == 'xlsx':
        return 'excel'
    return None

@main_bp.route('/')
def index():
    return render_template('index.html')

@upload_bp.route('/config', methods=['GET'])
def get_config():
    """Get current extraction configuration"""
    return jsonify({
        'use_openai': Config.USE_OPENAI_EXTRACTION,
        'openai_configured': Config.validate_openai_config(),
        'openai_model': Config.OPENAI_MODEL,
        'enable_fallback': Config.ENABLE_FALLBACK
    }), 200

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and parsing"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not supported. Please upload PDF, Word, or Excel files.'}), 400
        
        # Check for use_openai parameter in request
        use_openai = request.args.get('use_openai', None)
        if use_openai is not None:
            use_openai = use_openai.lower() == 'true'
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        upload_folder = 'uploads'
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        # Parse the file with specified extraction method
        file_type = get_file_type(filename)
        extractor = DataExtractor(filepath, file_type, use_openai=use_openai)
        result = extractor.extract_all()
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@upload_bp.route('/batch-upload', methods=['POST'])
def batch_upload():
    """Handle multiple file uploads"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        results = []
        errors = []
        
        # Check for use_openai parameter in request
        use_openai = request.args.get('use_openai', None)
        if use_openai is not None:
            use_openai = use_openai.lower() == 'true'
        
        for file in files:
            try:
                if file.filename == '':
                    continue
                
                if not allowed_file(file.filename):
                    errors.append({'file': file.filename, 'error': 'File type not supported'})
                    continue
                
                filename = secure_filename(file.filename)
                upload_folder = 'uploads'
                os.makedirs(upload_folder, exist_ok=True)
                filepath = os.path.join(upload_folder, filename)
                file.save(filepath)
                
                file_type = get_file_type(filename)
                extractor = DataExtractor(filepath, file_type, use_openai=use_openai)
                result = extractor.extract_all()
                result['filename'] = filename
                results.append(result)
            
            except Exception as e:
                errors.append({'file': file.filename, 'error': str(e)})
        
        return jsonify({'results': results, 'errors': errors}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@upload_bp.route('/update', methods=['POST'])
def update_data():
    """Update extracted data"""
    try:
        data = request.get_json()
        # Here you could save to database or return the updated data
        # For now, we'll just return the updated data back
        return jsonify(data), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@upload_bp.route('/export', methods=['POST'])
def export_results():
    """Export extracted data as JSON"""
    try:
        data = request.get_json()
        
        # Create JSON file
        output_file = 'extracted_data.json'
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return send_file(output_file, as_attachment=True, download_name='extracted_data.json')
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

