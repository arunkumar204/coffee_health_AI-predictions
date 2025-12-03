// Global state
let currentPage = 'landing';
let formData = {};
let predictionResults = {};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    updateSliders();
    initializeEventListeners();
});

// Initialize all event listeners
function initializeEventListeners() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Page Navigation Functions
function startAnalysis() {
    document.querySelector('.landing-container').style.display = 'none';
    document.getElementById('formPage').style.display = 'block';
    document.getElementById('resultsPage').style.display = 'none';
    currentPage = 'form';
}

function goBack() {
    document.querySelector('.landing-container').style.display = 'block';
    document.getElementById('formPage').style.display = 'none';
    document.getElementById('resultsPage').style.display = 'none';
    currentPage = 'landing';
}

function goBackToForm() {
    document.querySelector('.landing-container').style.display = 'none';
    document.getElementById('formPage').style.display = 'block';
    document.getElementById('resultsPage').style.display = 'none';
    currentPage = 'form';
}

// Update slider value displays
function updateCupsValue(value) {
    document.getElementById('cupsValue').textContent = value;
}

function updateCaffeineValue(value) {
    document.getElementById('caffeineValue').textContent = value;
}

function updateWeightValue(value) {
    document.getElementById('weightValue').textContent = value;
}

function updateSleepValue(value) {
    document.getElementById('sleepValue').textContent = value;
}

function updateExerciseValue(value) {
    document.getElementById('exerciseValue').textContent = value;
}

function updateStressValue(value) {
    document.getElementById('stressValue').textContent = value;
}

function updateWaterValue(value) {
    document.getElementById('waterValue').textContent = value;
}

// Initialize all sliders
function updateSliders() {
    updateCupsValue(document.getElementById('dailyCups').value);
    updateCaffeineValue(document.getElementById('caffeinePerCup').value);
    updateWeightValue(document.getElementById('bodyWeight').value);
    updateSleepValue(document.getElementById('sleepHours').value);
    updateExerciseValue(document.getElementById('exerciseMinutes').value);
    updateStressValue(document.getElementById('stressLevel').value);
    updateWaterValue(document.getElementById('waterIntake').value);
}

// Generate Prediction
function generatePrediction() {
    // Validate form data
    if (!validateFormData()) {
        return;
    }

    // Collect form data
    collectFormData();

    // Calculate total caffeine
    formData.totalCaffeine = formData.dailyCups * formData.caffeinePerCup;

    // Generate prediction results (using your actual ML model logic)
    predictionResults = calculateHealthPrediction(formData);

    // Display results
    displayResults(predictionResults);

    // Navigate to results page
    navigateToResultsPage();

    // Animate results
    animateResults();
}

// Validate form data
function validateFormData() {
    const age = parseInt(document.getElementById('age').value);
    if (age < 18 || age > 100) {
        alert('Please enter a valid age between 18 and 100');
        return false;
    }
    
    const bodyWeight = parseFloat(document.getElementById('bodyWeight').value);
    if (bodyWeight < 40 || bodyWeight > 200) {
        alert('Please enter a valid body weight between 40 and 200 kg');
        return false;
    }
    
    return true;
}

// Collect all form data
function collectFormData() {
    formData = {
        dailyCups: parseFloat(document.getElementById('dailyCups').value),
        caffeinePerCup: parseFloat(document.getElementById('caffeinePerCup').value),
        age: parseInt(document.getElementById('age').value),
        bodyWeight: parseFloat(document.getElementById('bodyWeight').value),
        sleepHours: parseFloat(document.getElementById('sleepHours').value),
        exerciseMinutes: parseInt(document.getElementById('exerciseMinutes').value),
        waterIntake: parseFloat(document.getElementById('waterIntake').value),
        stressLevel: parseInt(document.getElementById('stressLevel').value)
    };
}

// Navigate to results page
function navigateToResultsPage() {
    document.querySelector('.landing-container').style.display = 'none';
    document.getElementById('formPage').style.display = 'none';
    document.getElementById('resultsPage').style.display = 'block';
    currentPage = 'results';
}

// Calculate Health Prediction (Replace with your actual ML model logic)
function calculateHealthPrediction(data) {
    const { 
        dailyCups, 
        totalCaffeine, 
        sleepHours, 
        exerciseMinutes, 
        waterIntake, 
        stressLevel, 
        age, 
        bodyWeight 
    } = data;
    
    // Calculate base scores
    let overallScore = 70;
    let sleepQuality = 70;
    let heartRate = 72;
    let stressIndex = 50;
    
    // Adjust based on coffee consumption
    if (dailyCups <= 2) {
        overallScore += 5;
    } else if (dailyCups > 4) {
        overallScore -= 15;
        sleepQuality -= 20;
        stressIndex += 15;
    } else if (dailyCups > 2) {
        overallScore -= 5;
        sleepQuality -= 10;
        stressIndex += 8;
    }
    
    // Adjust based on total caffeine
    if (totalCaffeine > 400) {
        sleepQuality -= 15;
        heartRate += 5;
        stressIndex += 10;
    } else if (totalCaffeine > 200) {
        sleepQuality -= 5;
        heartRate += 2;
        stressIndex += 5;
    }
    
    // Adjust based on sleep
    if (sleepHours >= 7 && sleepHours <= 9) {
        overallScore += 10;
        sleepQuality += 15;
        stressIndex -= 10;
        heartRate -= 2;
    } else if (sleepHours < 6) {
        overallScore -= 10;
        sleepQuality -= 20;
        stressIndex += 15;
        heartRate += 3;
    }
    
    // Adjust based on exercise
    if (exerciseMinutes >= 30) {
        overallScore += 15;
        sleepQuality += 5;
        stressIndex -= 15;
        heartRate -= 3;
    } else if (exerciseMinutes < 15) {
        overallScore -= 10;
        sleepQuality -= 5;
        stressIndex += 10;
        heartRate += 2;
    }
    
    // Adjust based on water intake
    if (waterIntake >= 2.5) {
        overallScore += 10;
        sleepQuality += 5;
        stressIndex -= 5;
    } else if (waterIntake < 1.5) {
        overallScore -= 8;
        sleepQuality -= 5;
        stressIndex += 5;
        heartRate += 1;
    }
    
    // Adjust based on stress level
    stressIndex += (stressLevel - 5) * 5;
    
    // Adjust based on age
    heartRate += Math.max(0, (age - 30) * 0.1);
    
    // Adjust based on weight (BMI approximation)
    const height = 1.75; // Average height in meters
    const bmi = bodyWeight / (height * height);
    if (bmi > 25) {
        overallScore -= 5;
        heartRate += 2;
    } else if (bmi < 18.5) {
        overallScore -= 3;
    }
    
    // Ensure scores are within bounds
    overallScore = Math.max(30, Math.min(95, overallScore));
    sleepQuality = Math.max(30, Math.min(95, sleepQuality));
    heartRate = Math.max(60, Math.min(100, Math.round(heartRate)));
    stressIndex = Math.max(30, Math.min(95, Math.round(stressIndex)));
    
    // Determine labels
    const overallLabel = getScoreLabel(overallScore);
    
    // Generate recommendations
    const recommendations = generateRecommendations({
        dailyCups,
        totalCaffeine,
        sleepHours,
        exerciseMinutes,
        waterIntake,
        stressIndex
    });
    
    return {
        overallScore: Math.round(overallScore),
        overallLabel: overallLabel,
        sleepQuality: Math.round(sleepQuality),
        heartRate: `${heartRate}bpm`,
        stressIndex: `${stressIndex}/100`,
        recommendations: recommendations.trim()
    };
}

// Get score label based on value
function getScoreLabel(score) {
    if (score >= 85) return 'Excellent';
    if (score >= 75) return 'Very Good';
    if (score >= 65) return 'Good';
    if (score >= 55) return 'Fair';
    return 'Needs Improvement';
}

// Generate personalized recommendations
function generateRecommendations(data) {
    const { 
        dailyCups, 
        totalCaffeine, 
        sleepHours, 
        exerciseMinutes, 
        waterIntake, 
        stressIndex 
    } = data;
    
    let recommendations = "Great job! Your current habits are well-balanced. ";
    
    if (dailyCups > 3) {
        recommendations += "Consider reducing coffee intake to 2 cups daily for better sleep quality. ";
    }
    
    if (sleepHours < 7) {
        recommendations += "Aim for 7-9 hours of sleep per night to improve recovery and cognitive function. ";
    }
    
    if (exerciseMinutes < 30) {
        recommendations += "Incorporate at least 30 minutes of moderate exercise daily for cardiovascular health. ";
    }
    
    if (waterIntake < 2) {
        recommendations += "Increase water intake to at least 3 liters per day for better hydration. ";
    }
    
    if (stressIndex > 60) {
        recommendations += "Practice stress management techniques like meditation or deep breathing exercises. ";
    }
    
    if (totalCaffeine > 400) {
        recommendations += "Try to limit total caffeine intake to under 400mg per day. ";
    }
    
    return recommendations;
}

// Display Results
function displayResults(results) {
    // Update all result values
    updateResultElement('overallScoreValue', `${results.overallScore}%`);
    updateResultElement('overallScoreLabel', results.overallLabel);
    updateResultElement('sleepQualityValue', `${results.sleepQuality}%`);
    updateResultElement('heartRateValue', results.heartRate);
    updateResultElement('stressIndexValue', results.stressIndex);
    updateResultElement('overallBreakdownValue', `${results.overallScore}%`);
    updateResultElement('sleepBreakdownValue', `${results.sleepQuality}%`);
    updateResultElement('recommendationText', results.recommendations);
    
    // Update progress bars
    updateProgressBar('overallBreakdownBar', results.overallScore);
    updateProgressBar('sleepBreakdownBar', results.sleepQuality);
    
    // Update colors based on scores
    updateScoreColors(results.overallScore, 'overallScoreValue');
    updateScoreColors(results.sleepQuality, 'sleepQualityValue');
    updateScoreColors(parseInt(results.stressIndex), 'stressIndexValue');
}

// Update HTML element content
function updateResultElement(elementId, value) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = value;
    }
}

// Update progress bar width
function updateProgressBar(barId, percentage) {
    const bar = document.getElementById(barId);
    if (bar) {
        bar.style.width = `${percentage}%`;
    }
}

// Update score colors
function updateScoreColors(score, elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    let color;
    if (score >= 85) {
        color = '#27AE60'; // Excellent
    } else if (score >= 75) {
        color = '#2ECC71'; // Very Good
    } else if (score >= 65) {
        color = '#F39C12'; // Good
    } else if (score >= 55) {
        color = '#E67E22'; // Fair
    } else {
        color = '#E74C3C'; // Needs Improvement
    }
    
    element.style.color = color;
}

// Animate results on display
function animateResults() {
    const bars = document.querySelectorAll('.bar-fill');
    bars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0';
        setTimeout(() => {
            bar.style.transition = 'width 1s ease-in-out';
            bar.style.width = width;
        }, 100);
    });
}

// Start New Analysis
function startNewAnalysis() {
    resetForm();
    updateSliders();
    goBackToForm();
}

// Reset form to default values
function resetForm() {
    document.getElementById('dailyCups').value = 2;
    document.getElementById('caffeinePerCup').value = 95;
    document.getElementById('age').value = 30;
    document.getElementById('bodyWeight').value = 70;
    document.getElementById('sleepHours').value = 7;
    document.getElementById('exerciseMinutes').value = 30;
    document.getElementById('waterIntake').value = 2;
    document.getElementById('stressLevel').value = 5;
}

// Download Results as PDF
async function downloadResults() {
    const { jsPDF } = window.jspdf;

    const doc = new jsPDF({
        unit: "pt",
        format: "a4"
    });

    let y = 40; // Starting position

    // Add Title
    doc.setFont("Helvetica", "bold");
    doc.setFontSize(18);
    doc.text("COFFEE & HEALTH ANALYSIS REPORT", 40, y);
    y += 30;

    doc.setFont("Helvetica", "normal");
    doc.setFontSize(12);

    const reportLines = generateReport().split("\n");
    reportLines.forEach(line => {
        doc.text(line, 40, y);
        y += 18;

        // Auto add new page if content exceeds
        if (y > 780) {
            doc.addPage();
            y = 40;
        }
    });

    doc.save(`health-analysis-${new Date().toISOString().split("T")[0]}.pdf`);

    // Show confirmation
    alert('Report downloaded successfully!');
}

// Generate comprehensive report (same content but formatted for PDF)
function generateReport() {
    return `
Personal Information
----------------------------
- Daily Coffee Cups: ${formData.dailyCups}
- Caffeine per Cup: ${formData.caffeinePerCup}mg
- Total Daily Caffeine: ${formData.totalCaffeine}mg
- Age: ${formData.age}
- Weight: ${formData.bodyWeight}kg
- Sleep: ${formData.sleepHours} hours/night
- Exercise: ${formData.exerciseMinutes} minutes/day
- Water Intake: ${formData.waterIntake} liters/day
- Stress Level: ${formData.stressLevel}/10

Health Predictions
----------------------------
- Overall Health Score: ${predictionResults.overallScore}% (${predictionResults.overallLabel})
- Sleep Quality: ${predictionResults.sleepQuality}%
- Predicted Heart Rate: ${predictionResults.heartRate}
- Stress Index: ${predictionResults.stressIndex}

Recommendations
----------------------------
${predictionResults.recommendations}

Analysis Details
----------------------------
${getAnalysisDetails()}

Generated on: ${new Date().toLocaleDateString()}

Disclaimer: This report is for informational purposes only and should not replace 
professional medical advice. Always consult a healthcare provider for personalized guidance.
    `;
}


// Get additional analysis details
function getAnalysisDetails() {
    let details = '';
    
    if (formData.totalCaffeine > 400) {
        details += '- Your caffeine intake exceeds the recommended daily limit of 400mg\n';
    }
    
    if (formData.sleepHours < 7) {
        details += '- Sleep duration is below the recommended 7-9 hours per night\n';
    }
    
    if (formData.exerciseMinutes < 30) {
        details += '- Consider increasing exercise to at least 30 minutes daily\n';
    }
    
    if (formData.waterIntake < 2) {
        details += '- Water intake is below the recommended 2 liters per day\n';
    }
    
    return details || '- All lifestyle factors are within healthy ranges';
}

// Export functions for global access
window.startAnalysis = startAnalysis;
window.goBack = goBack;
window.goBackToForm = goBackToForm;
window.updateCupsValue = updateCupsValue;
window.updateCaffeineValue = updateCaffeineValue;
window.updateWeightValue = updateWeightValue;
window.updateSleepValue = updateSleepValue;
window.updateExerciseValue = updateExerciseValue;
window.updateWaterValue = updateWaterValue;
window.updateStressValue = updateStressValue;
window.generatePrediction = generatePrediction;
window.startNewAnalysis = startNewAnalysis;
window.downloadResults = downloadResults;