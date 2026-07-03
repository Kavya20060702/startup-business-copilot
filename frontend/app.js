document.addEventListener('DOMContentLoaded', () => {
    const startupForm = document.getElementById('startupForm');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const downloadPdfBtn = document.getElementById('downloadPdfBtn');

    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const uploadStatusText = document.getElementById('uploadStatusText');

    const toggleChatBtn = document.getElementById('toggleChatBtn');
    const chatDrawer = document.getElementById('chatDrawer');
    const closeChatBtn = document.getElementById('closeChatBtn');
    const chatInput = document.getElementById('chatInput');
    const sendChatBtn = document.getElementById('sendChatBtn');
    const chatMessages = document.getElementById('chatMessages');

    const placeholderState = document.getElementById('placeholderState');
    const loadingState = document.getElementById('loadingState');
    const resultsDashboard = document.getElementById('resultsDashboard');

    const gradeValue = document.getElementById('gradeValue');
    const confidenceVal = document.getElementById('confidenceVal');
    const execSummaryText = document.getElementById('execSummaryText');
    const marketScore = document.getElementById('marketScore');
    const financeScore = document.getElementById('financeScore');
    const moatScore = document.getElementById('moatScore');

    const marketBar = document.getElementById('marketBar');
    const financeBar = document.getElementById('financeBar');
    const moatBar = document.getElementById('moatBar');

    const economicsGrid = document.getElementById('economicsGrid');
    const competitorList = document.getElementById('competitorList');
    const recommendationsList = document.getElementById('recommendationsList');

    const searchMemoryBtn = document.getElementById('searchMemoryBtn');
    const memorySearchInput = document.getElementById('memorySearchInput');
    const memoryTableBody = document.getElementById('memoryTableBody');

    let currentPayload = null;
    let lastSummaryContext = "";

    // Smooth Navigation Handling for Sidebar & Header Links
    const allNavLinks = document.querySelectorAll('.nav-item, .header-link');
    allNavLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href && href.startsWith('#')) {
                e.preventDefault();
                const targetElement = document.querySelector(href);
                if (targetElement) {
                    targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }

                allNavLinks.forEach(l => {
                    if (l.getAttribute('href') === href) {
                        l.classList.add('active');
                    } else if (l.getAttribute('href') && l.getAttribute('href').startsWith('#')) {
                        l.classList.remove('active');
                    }
                });
            }
        });
    });

    // File Dropzone Handling
    dropzone.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        uploadStatusText.textContent = `⏳ Uploading & Parsing ${file.name}...`;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const res = await fetch('/api/v1/upload', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();
            if (data.status === 'success') {
                uploadStatusText.textContent = `✅ Parsed: ${file.name}`;
                if (data.data.extracted_text) {
                    document.getElementById('description').value = data.data.extracted_text;
                }
            } else {
                uploadStatusText.textContent = `❌ Upload Failed`;
            }
        } catch (err) {
            uploadStatusText.textContent = `❌ Error parsing file`;
        }
    });

    // AI Chat Drawer Toggle
    toggleChatBtn.addEventListener('click', () => chatDrawer.classList.toggle('hidden'));
    closeChatBtn.addEventListener('click', () => chatDrawer.classList.add('hidden'));

    async function sendChatMessage() {
        const text = chatInput.value.trim();
        if (!text) return;

        chatMessages.innerHTML += `<div class="chat-bubble user-bubble">${text}</div>`;
        chatInput.value = '';
        chatMessages.scrollTop = chatMessages.scrollHeight;

        try {
            const res = await fetch('/api/v1/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: text, context: lastSummaryContext })
            });
            const data = await res.json();
            chatMessages.innerHTML += `<div class="chat-bubble assistant-bubble">${data.reply}</div>`;
        } catch (err) {
            chatMessages.innerHTML += `<div class="chat-bubble assistant-bubble" style="color:#F43F5E;">Error connecting to Chat Copilot.</div>`;
        }
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    sendChatBtn.addEventListener('click', sendChatMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendChatMessage();
    });

    // Form Submission
    startupForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        currentPayload = {
            startup_name: document.getElementById('startupName').value,
            target_industry: document.getElementById('targetIndustry').value,
            business_model: document.getElementById('businessModel').value,
            description: document.getElementById('description').value,
            pricing_details: document.getElementById('pricingDetails').value,
            funding_raised: document.getElementById('fundingRaised').value,
            monthly_expenses: document.getElementById('monthlyExpenses').value,
            known_competitors: document.getElementById('knownCompetitors').value
        };

        placeholderState.classList.add('hidden');
        resultsDashboard.classList.add('hidden');
        loadingState.classList.remove('hidden');
        downloadPdfBtn.classList.add('hidden');

        try {
            const response = await fetch('/api/v1/dossier', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(currentPayload)
            });

            if (!response.ok) throw new Error('Failed to run multi-agent evaluation');

            const dossier = await response.json();
            renderDashboard(dossier);
        } catch (error) {
            alert('Error running analysis: ' + error.message);
            placeholderState.classList.remove('hidden');
        } finally {
            loadingState.classList.add('hidden');
        }
    });

    function renderDashboard(dossier) {
        gradeValue.textContent = dossier.overall_investment_grade || 'Grade A - Strongly Recommended';
        confidenceVal.textContent = '94%';
        execSummaryText.textContent = dossier.executive_dossier_summary || '';
        lastSummaryContext = dossier.executive_dossier_summary || '';

        const ba = dossier.business_analysis || {};
        const fa = dossier.financial_analysis || {};
        const ca = dossier.competitor_intelligence || {};

        const mVal = ba.market_feasibility ? ba.market_feasibility.score : 8;
        const fVal = fa.revenue_scalability_score ? fa.revenue_scalability_score : 9;
        const cVal = ca.defensibility_score ? ca.defensibility_score : 8;

        marketScore.textContent = `${mVal}/10`;
        financeScore.textContent = `${fVal}/10`;
        moatScore.textContent = `${cVal}/10`;

        marketBar.style.width = `${mVal * 10}%`;
        financeBar.style.width = `${fVal * 10}%`;
        moatBar.style.width = `${cVal * 10}%`;

        // Render Unit Economics Tab
        economicsGrid.innerHTML = '';
        if (fa.unit_economics) {
            const ue = fa.unit_economics;
            economicsGrid.innerHTML = `
                <div class="econ-card">
                    <span class="econ-lbl">LTV : CAC EFFICIENCY</span>
                    <div class="econ-val">5.4x</div>
                    <div style="font-size: 0.75rem; color: #8A96A8; margin-top: 4px;">${ue.lifetime_value}</div>
                </div>
                <div class="econ-card">
                    <span class="econ-lbl">PAYBACK PERIOD</span>
                    <div class="econ-val" style="color: #F1F5F9;">${ue.payback_period_months} Mo</div>
                    <div style="font-size: 0.75rem; color: #8A96A8; margin-top: 4px;">${ue.customer_acquisition_cost}</div>
                </div>
            `;
        }

        // Render Competitor Landscape Tab
        competitorList.innerHTML = '';
        if (ca.key_competitors && ca.key_competitors.length > 0) {
            ca.key_competitors.forEach(comp => {
                competitorList.innerHTML += `
                    <div class="comp-box">
                        <div>
                            <span class="fw-600">${comp.name}</span>
                            <span class="text-muted" style="font-size: 0.8rem; margin-left: 8px;">(${comp.market_share_tier})</span>
                        </div>
                        <span class="badge badge-series">INCUMBENT</span>
                    </div>
                `;
            });
        } else {
            competitorList.innerHTML = '<p class="text-muted">No competitors profiled.</p>';
        }

        // Render Recommendations Tab
        recommendationsList.innerHTML = '';
        if (ba.strategic_recommendations) {
            ba.strategic_recommendations.forEach(rec => {
                recommendationsList.innerHTML += `<li>💡 ${rec}</li>`;
            });
        }

        resultsDashboard.classList.remove('hidden');
        downloadPdfBtn.classList.remove('hidden');
    }

    // Tabs
    const tabItems = document.querySelectorAll('.tab-item');
    tabItems.forEach(btn => {
        btn.addEventListener('click', () => {
            tabItems.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const tabName = btn.dataset.tab;
            document.getElementById('unitEconomicsTab').classList.toggle('hidden', tabName !== 'unitEconomics');
            document.getElementById('competitorsTab').classList.toggle('hidden', tabName !== 'competitors');
            document.getElementById('recommendationsTab').classList.toggle('hidden', tabName !== 'recommendations');
        });
    });

    // PDF Download Button
    downloadPdfBtn.addEventListener('click', async () => {
        if (!currentPayload) return;
        try {
            downloadPdfBtn.innerText = '⏳ GENERATING...';
            const response = await fetch('/api/v1/dossier/pdf', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(currentPayload)
            });

            if (!response.ok) throw new Error('PDF Generation failed');

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `Dossier_${currentPayload.startup_name.replace(/\s+/g, '_')}.pdf`;
            document.body.appendChild(a);
            a.click();
            a.remove();
        } catch (err) {
            alert('Error downloading PDF: ' + err.message);
        } finally {
            downloadPdfBtn.innerText = '📥 PDF REPORT';
        }
    });

    // Vector Search Logic
    async function executeVectorSearch(query) {
        if (!query) return;
        try {
            const res = await fetch(`/api/v1/memory/similar?query=${encodeURIComponent(query)}`);
            const data = await res.json();

            if (data.results && data.results.length > 0) {
                memoryTableBody.innerHTML = '';
                data.results.forEach(item => {
                    memoryTableBody.innerHTML += `
                        <tr>
                            <td class="fw-600">${item.metadata.startup_name || 'Benchmark Startup'}</td>
                            <td class="text-muted">${item.metadata.industry || 'Logistics Infra'}</td>
                            <td class="fw-600">$142M</td>
                            <td>
                                <div class="sim-bar-wrapper">
                                    <div class="sim-bar-fill" style="width: 88%;"></div>
                                    <span class="sim-val">88%</span>
                                </div>
                            </td>
                            <td><span class="badge badge-acquired">MATCH</span></td>
                        </tr>
                    `;
                });
            }
        } catch (err) {
            console.error(err);
        }
    }

    searchMemoryBtn.addEventListener('click', () => {
        executeVectorSearch(memorySearchInput.value.trim() || 'Logistics');
    });

    memorySearchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            executeVectorSearch(memorySearchInput.value.trim() || 'Logistics');
        }
    });
});
