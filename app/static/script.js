// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const processingStatus = document.getElementById('processingStatus');
const resultsSection = document.getElementById('resultsSection');
const fileResults = document.getElementById('fileResults');
const errorContainer = document.getElementById('errorContainer');
const exportBtn = document.getElementById('exportBtn');
const clearBtn = document.getElementById('clearBtn');

let uploadedFiles = [];
let extractedData = [];

// File Upload Handlers
uploadArea.addEventListener('click', () => fileInput.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    handleFiles(e.dataTransfer.files);
});

fileInput.addEventListener('change', (e) => {
    handleFiles(e.target.files);
});

uploadBtn.addEventListener('click', () => {
    fileInput.click();
});

function handleFiles(files) {
    uploadedFiles = Array.from(files);
    if (uploadedFiles.length > 0) {
        processFiles();
    }
}

async function processFiles() {
    if (uploadedFiles.length === 0) return;

    // Clear previous results
    fileResults.innerHTML = '';
    errorContainer.innerHTML = '';
    errorContainer.classList.add('hidden');
    resultsSection.classList.add('hidden');

    // Show processing status
    processingStatus.classList.remove('hidden');

    const formData = new FormData();
    uploadedFiles.forEach(file => {
        formData.append('files', file);
    });

    try {
        const response = await fetch('/api/batch-upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            extractedData = result.results;
            displayResults(result.results, result.errors);
        } else {
            showError('Upload Error', result.error);
        }
    } catch (error) {
        showError('Network Error', error.message);
    } finally {
        processingStatus.classList.add('hidden');
        uploadedFiles = [];
        fileInput.value = '';
    }
}

function displayResults(results, errors) {
    // Display errors if any
    if (errors && errors.length > 0) {
        displayErrors(errors);
    }

    // Display successful results
    if (results && results.length > 0) {
        results.forEach((result, index) => {
            const fileCard = createFileCard(result, index);
            fileResults.appendChild(fileCard);
        });
        resultsSection.classList.remove('hidden');
    }
}

function createFileCard(result, index) {
    const card = document.createElement('div');
    card.className = 'file-result';

    const { file_info, extracted_metrics } = result;

    // File Header
    const header = document.createElement('div');
    header.className = 'file-result-header';
    header.innerHTML = `
        <h3>${file_info.file_path}</h3>
        <div class="file-info">
            <strong>Type:</strong> ${file_info.file_type} | 
            <strong>Pages/Sheets:</strong> ${file_info.pages}
        </div>
    `;
    card.appendChild(header);

    // Create tabs for different metric groups
    const metricsGroups = createMetricsGroups(extracted_metrics);
    card.appendChild(metricsGroups);

    return card;
}

function createMetricsGroups(metrics) {
    const container = document.createElement('div');

    const categories = [
        { key: 'property_details', label: '🏢 Property Details' },
        { key: 'financial_metrics', label: '💰 Financial Metrics' },
        { key: 'loan_details', label: '💳 Loan Details' },
        { key: 'tenant_info', label: '👥 Tenant Information' },
        { key: 'market_analysis', label: '📊 Market Analysis' },
        { key: 'risk_factors', label: '⚠️ Risk Factors' }
    ];

    categories.forEach(({ key, label }) => {
        const data = metrics[key];
        if (data && Object.keys(data).length > 0) {
            const group = document.createElement('div');
            group.className = 'metrics-group';
            group.innerHTML = `<h4>${label}</h4>`;

            if (key === 'tenant_info' && data.major_tenants) {
                const ul = document.createElement('ul');
                ul.className = 'metrics-list';
                data.major_tenants.forEach(tenant => {
                    const li = document.createElement('li');
                    li.textContent = tenant;
                    ul.appendChild(li);
                });
                group.appendChild(ul);
            } else if (key === 'risk_factors' && data.risks) {
                const ul = document.createElement('ul');
                ul.className = 'metrics-list';
                data.risks.forEach(risk => {
                    const li = document.createElement('li');
                    li.textContent = risk;
                    ul.appendChild(li);
                });
                group.appendChild(ul);
            } else {
                Object.entries(data).forEach(([metricKey, value]) => {
                    if (Array.isArray(value)) return; // Skip arrays
                    const item = document.createElement('div');
                    item.className = 'metric-item';
                    const displayKey = metricKey.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                    item.innerHTML = `
                        <span class="metric-label">${displayKey}:</span>
                        <span class="metric-value ${!value ? 'empty' : ''}">${value || 'Not found'}</span>
                    `;
                    group.appendChild(item);
                });
            }

            container.appendChild(group);
        }
    });

    return container;
}

function displayErrors(errors) {
    if (errors.length === 0) return;

    errorContainer.innerHTML = '<h3>Processing Errors</h3>';
    errors.forEach(error => {
        const errorItem = document.createElement('div');
        errorItem.className = 'error-item';
        errorItem.innerHTML = `
            <div class="error-file">${error.file}</div>
            <div class="error-message">${error.error}</div>
        `;
        errorContainer.appendChild(errorItem);
    });
    errorContainer.classList.remove('hidden');
}

function showError(title, message) {
    errorContainer.innerHTML = `
        <h3>${title}</h3>
        <div class="error-item">
            <div class="error-message">${message}</div>
        </div>
    `;
    errorContainer.classList.remove('hidden');
}

// Export Results
exportBtn.addEventListener('click', () => {
    if (extractedData.length === 0) {
        alert('No data to export');
        return;
    }

    const dataToExport = {
        exportDate: new Date().toISOString(),
        files: extractedData
    };

    const json = JSON.stringify(dataToExport, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `cre_extraction_${new Date().getTime()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
});

// Clear Results
clearBtn.addEventListener('click', () => {
    fileResults.innerHTML = '';
    resultsSection.classList.add('hidden');
    errorContainer.innerHTML = '';
    errorContainer.classList.add('hidden');
    extractedData = [];
    uploadedFiles = [];
    fileInput.value = '';
});
