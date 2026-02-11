// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const processingStatus = document.getElementById('processingStatus');
const resultsSection = document.getElementById('resultsSection');
const fileResults = document.getElementById('fileResults');
const errorContainer = document.getElementById('errorContainer');
const saveBtn = document.getElementById('saveBtn');
const exportBtn = document.getElementById('exportBtn');
const clearBtn = document.getElementById('clearBtn');

let uploadedFiles = [];
let extractedData = [];
let dataModified = false;

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
    card.dataset.index = index;

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

    // Create MOIC display section
    const moicSection = createMOICSection(extracted_metrics, index);
    card.appendChild(moicSection);

    // Create tabs for different metric groups
    const metricsGroups = createMetricsGroups(extracted_metrics, index);
    card.appendChild(metricsGroups);

    return card;
}

function createMOICSection(metrics, index) {
    const section = document.createElement('div');
    section.className = 'moic-section';
    
    const financialMetrics = metrics.financial_metrics || {};
    const projectCostMetric = financialMetrics.project_cost || financialMetrics.purchase_price;
    const exitValuationMetric = financialMetrics.expected_exit_valuation;
    const projectCost = getMetricValue(projectCostMetric);
    const exitValuation = getMetricValue(exitValuationMetric);
    const projectCostSource = getMetricSource(projectCostMetric);
    const exitValuationSource = getMetricSource(exitValuationMetric);
    
    const moic = calculateMOIC(projectCost, exitValuation);
    
    section.innerHTML = `
        <div class="moic-header">
            <h4>📈 Investment Metrics & MOIC</h4>
        </div>
        <div class="moic-inputs">
            <div class="moic-input-group">
                <label>Project Cost ($)</label>
                <input type="number" class="editable-input" data-index="${index}" 
                       data-category="financial_metrics" data-field="project_cost" 
                       value="${projectCost || ''}" placeholder="Enter project cost">
                ${projectCostSource ? `<div class="metric-citation">📄 ${projectCostSource}</div>` : ''}
            </div>
            <div class="moic-input-group">
                <label>Expected Exit Valuation ($)</label>
                <input type="number" class="editable-input" data-index="${index}" 
                       data-category="financial_metrics" data-field="expected_exit_valuation" 
                       value="${exitValuation || ''}" placeholder="Enter exit valuation">
                ${exitValuationSource ? `<div class="metric-citation">📄 ${exitValuationSource}</div>` : ''}
            </div>
        </div>
        <div class="moic-display">
            <div class="moic-result">
                <span class="moic-label">MOIC:</span>
                <span class="moic-value" data-index="${index}">${moic}</span>
            </div>
        </div>
    `;
    
    return section;
}

function getMetricValue(metric) {
    if (!metric) return null;
    if (typeof metric === 'object' && metric.value !== undefined) {
        return metric.value;
    }
    return metric;
}

function getMetricUnit(metric) {
    if (!metric || typeof metric !== 'object') return null;
    return metric.unit || null;
}

function getMetricSource(metric) {
    if (!metric || typeof metric !== 'object') return null;
    return metric.source_text || metric.citation || null;
}

function calculateMOIC(projectCost, exitValuation) {
    if (!projectCost || !exitValuation || projectCost === 0) {
        return 'N/A';
    }
    const moic = exitValuation / projectCost;
    return moic.toFixed(2) + 'x';
}

function createMetricsGroups(metrics, index) {
    const container = document.createElement('div');
    container.className = 'metrics-container';

    const categories = [
        { key: 'property_details', label: '🏢 Property Details' },
        { key: 'financial_metrics', label: '💰 Financial Metrics' },
        { key: 'loan_details', label: '💳 Loan Details' },
        { key: 'tenant_info', label: '👥 Tenant Information' },
        { key: 'tenant_information', label: '👥 Tenant Information' },
        { key: 'market_analysis', label: '📊 Market Analysis' },
        { key: 'risk_factors', label: '⚠️ Risk Factors' },
        { key: 'risk_assessment', label: '⚠️ Risk Assessment' }
    ];

    categories.forEach(({ key, label }) => {
        const data = metrics[key];
        if (data && Object.keys(data).length > 0) {
            const group = document.createElement('div');
            group.className = 'metrics-group collapsible';
            
            const groupHeader = document.createElement('div');
            groupHeader.className = 'metrics-group-header';
            groupHeader.innerHTML = `<h4>${label}</h4><span class="collapse-icon">▼</span>`;
            groupHeader.onclick = () => {
                group.classList.toggle('collapsed');
            };
            group.appendChild(groupHeader);
            
            const groupContent = document.createElement('div');
            groupContent.className = 'metrics-group-content';

            if ((key === 'tenant_info' || key === 'tenant_information') && data.major_tenants) {
                const ul = document.createElement('ul');
                ul.className = 'metrics-list';
                const tenants = Array.isArray(data.major_tenants) ? data.major_tenants : [];
                tenants.forEach(tenant => {
                    const li = document.createElement('li');
                    const tenantName = typeof tenant === 'object' ? tenant.name : tenant;
                    const tenantSource = typeof tenant === 'object' ? (tenant.source_text || tenant.citation) : null;
                    li.innerHTML = `
                        <div class="metric-list-item">${tenantName}</div>
                        ${tenantSource ? `<div class="metric-citation">📄 ${tenantSource}</div>` : ''}
                    `;
                    ul.appendChild(li);
                });
                groupContent.appendChild(ul);
            } else if ((key === 'risk_factors' || key === 'risk_assessment') && (data.risks || data.identified_risks)) {
                const ul = document.createElement('ul');
                ul.className = 'metrics-list';
                const risks = data.risks || data.identified_risks || [];
                const riskArray = Array.isArray(risks) ? risks : [];
                riskArray.forEach(risk => {
                    const li = document.createElement('li');
                    const riskText = typeof risk === 'object' ? (risk.risk || risk.strategy || risk.name) : risk;
                    const riskSource = typeof risk === 'object' ? (risk.source_text || risk.citation) : null;
                    li.innerHTML = `
                        <div class="metric-list-item">${riskText}</div>
                        ${riskSource ? `<div class="metric-citation">📄 ${riskSource}</div>` : ''}
                    `;
                    ul.appendChild(li);
                });
                groupContent.appendChild(ul);
                if (Array.isArray(data.mitigation_strategies) && data.mitigation_strategies.length > 0) {
                    const mitigationList = document.createElement('ul');
                    mitigationList.className = 'metrics-list';
                    data.mitigation_strategies.forEach(strategy => {
                        const strategyText = typeof strategy === 'object' ? (strategy.strategy || strategy.name) : strategy;
                        const strategySource = typeof strategy === 'object' ? (strategy.source_text || strategy.citation) : null;
                        const li = document.createElement('li');
                        li.innerHTML = `
                            <div class="metric-list-item">${strategyText}</div>
                            ${strategySource ? `<div class="metric-citation">📄 ${strategySource}</div>` : ''}
                        `;
                        mitigationList.appendChild(li);
                    });
                    groupContent.appendChild(mitigationList);
                }
            } else {
                if (key === 'financial_metrics' && Array.isArray(data.expected_rents)) {
                    const ul = document.createElement('ul');
                    ul.className = 'metrics-list';
                    data.expected_rents.forEach(rent => {
                        const rentType = rent.type ? `${rent.type}: ` : '';
                        const rentValue = rent.value !== undefined && rent.value !== null ? rent.value : '';
                        const rentUnit = rent.unit ? ` ${rent.unit}` : '';
                        const rentSource = rent.source_text || rent.citation || null;
                        const li = document.createElement('li');
                        li.innerHTML = `
                            <div class="metric-list-item">${rentType}${rentValue}${rentUnit}</div>
                            ${rentSource ? `<div class="metric-citation">📄 ${rentSource}</div>` : ''}
                        `;
                        ul.appendChild(li);
                    });
                    groupContent.appendChild(ul);
                }
                if (key === 'market_analysis' && Array.isArray(data.comparable_properties)) {
                    const compsList = document.createElement('ul');
                    compsList.className = 'metrics-list';
                    data.comparable_properties.forEach(comp => {
                        const compText = typeof comp === 'object' ? (comp.property || comp.name) : comp;
                        const compSource = typeof comp === 'object' ? (comp.source_text || comp.citation) : null;
                        const li = document.createElement('li');
                        li.innerHTML = `
                            <div class="metric-list-item">${compText}</div>
                            ${compSource ? `<div class="metric-citation">📄 ${compSource}</div>` : ''}
                        `;
                        compsList.appendChild(li);
                    });
                    groupContent.appendChild(compsList);
                }
                if (key === 'market_analysis' && Array.isArray(data.market_trends)) {
                    const trendsList = document.createElement('ul');
                    trendsList.className = 'metrics-list';
                    data.market_trends.forEach(trend => {
                        const trendText = typeof trend === 'object' ? (trend.trend || trend.name) : trend;
                        const trendSource = typeof trend === 'object' ? (trend.source_text || trend.citation) : null;
                        const li = document.createElement('li');
                        li.innerHTML = `
                            <div class="metric-list-item">${trendText}</div>
                            ${trendSource ? `<div class="metric-citation">📄 ${trendSource}</div>` : ''}
                        `;
                        trendsList.appendChild(li);
                    });
                    groupContent.appendChild(trendsList);
                }
                Object.entries(data).forEach(([metricKey, metricData]) => {
                    if (Array.isArray(metricData)) return; // Skip arrays handled above
                    
                    const value = getMetricValue(metricData);
                    const unit = getMetricUnit(metricData);
                    const source = getMetricSource(metricData);
                    const item = document.createElement('div');
                    item.className = 'metric-item';
                    const displayKey = metricKey.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                    
                    // Skip project_cost and expected_exit_valuation as they're in MOIC section
                    if (metricKey === 'project_cost' || metricKey === 'expected_exit_valuation') {
                        return;
                    }
                    
                    // Determine if field should be editable
                    const isNumeric = typeof value === 'number' || !isNaN(parseFloat(value));
                    const inputType = isNumeric ? 'number' : 'text';
                    
                    item.innerHTML = `
                        <span class="metric-label">${displayKey}:</span>
                        <input type="${inputType}" class="metric-value editable-input" 
                               data-index="${index}" data-category="${key}" data-field="${metricKey}" 
                               value="${value || ''}" placeholder="Not found">
                        ${unit ? `<div class="metric-unit">Unit: ${unit}</div>` : ''}
                        ${source ? `<div class="metric-citation">📄 ${source}</div>` : ''}
                    `;
                    groupContent.appendChild(item);
                });
            }
            
            group.appendChild(groupContent);
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

// Save Changes
saveBtn.addEventListener('click', async () => {
    if (!dataModified) {
        alert('No changes to save');
        return;
    }
    
    // Update extractedData from UI
    updateExtractedDataFromUI();
    
    try {
        const response = await fetch('/api/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(extractedData)
        });
        
        if (response.ok) {
            alert('Changes saved successfully!');
            dataModified = false;
            saveBtn.style.background = '#757575';
        } else {
            alert('Error saving changes');
        }
    } catch (error) {
        alert('Network error: ' + error.message);
    }
});

function updateExtractedDataFromUI() {
    document.querySelectorAll('.editable-input').forEach(input => {
        const index = parseInt(input.dataset.index);
        const category = input.dataset.category;
        const field = input.dataset.field;
        const value = input.value;
        
        if (extractedData[index] && extractedData[index].extracted_metrics) {
            if (!extractedData[index].extracted_metrics[category]) {
                extractedData[index].extracted_metrics[category] = {};
            }
            
            // Handle both simple values and citation objects
            const currentValue = extractedData[index].extracted_metrics[category][field];
            if (typeof currentValue === 'object' && currentValue !== null && 'value' in currentValue) {
                extractedData[index].extracted_metrics[category][field].value = 
                    input.type === 'number' ? parseFloat(value) || null : value;
            } else {
                extractedData[index].extracted_metrics[category][field] = 
                    input.type === 'number' ? parseFloat(value) || null : value;
            }
        }
    });
}

// Add event delegation for input changes
document.addEventListener('input', (e) => {
    if (e.target.classList.contains('editable-input')) {
        dataModified = true;
        saveBtn.style.background = '#4CAF50';
        
        // If it's a MOIC-related field, recalculate MOIC
        if (e.target.dataset.field === 'project_cost' || e.target.dataset.field === 'expected_exit_valuation') {
            recalculateMOIC(e.target.dataset.index);
        }
    }
});

function recalculateMOIC(index) {
    const projectCostInput = document.querySelector(
        `input[data-index="${index}"][data-field="project_cost"]`
    );
    const exitValuationInput = document.querySelector(
        `input[data-index="${index}"][data-field="expected_exit_valuation"]`
    );
    const moicDisplay = document.querySelector(
        `.moic-value[data-index="${index}"]`
    );
    
    if (projectCostInput && exitValuationInput && moicDisplay) {
        const projectCost = parseFloat(projectCostInput.value);
        const exitValuation = parseFloat(exitValuationInput.value);
        const moic = calculateMOIC(projectCost, exitValuation);
        moicDisplay.textContent = moic;
    }
}

// Clear Results
clearBtn.addEventListener('click', () => {
    fileResults.innerHTML = '';
    resultsSection.classList.add('hidden');
    errorContainer.innerHTML = '';
    errorContainer.classList.add('hidden');
    extractedData = [];
    uploadedFiles = [];
    fileInput.value = '';
    dataModified = false;
    saveBtn.style.background = '#757575';
});
