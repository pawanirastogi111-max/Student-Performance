document.addEventListener('DOMContentLoaded', () => {
    // ----------------- Elements Setup -----------------
    const form = document.getElementById('diagnostics-form');
    
    // Sliders & Selects
    const inputs = {
        age: document.getElementById('age'),
        gender: document.getElementById('gender'),
        academic_level: document.getElementById('academic_level'),
        internet_quality: document.getElementById('internet_quality'),
        attendance: document.getElementById('attendance'),
        study_hours: document.getElementById('study_hours'),
        self_study_hours: document.getElementById('self_study_hours'),
        online_classes_hours: document.getElementById('online_classes_hours'),
        social_media_hours: document.getElementById('social_media_hours'),
        gaming_hours: document.getElementById('gaming_hours'),
        sleep_hours: document.getElementById('sleep_hours'),
        exercise_minutes: document.getElementById('exercise_minutes'),
        caffeine_intake_mg: document.getElementById('caffeine_intake_mg'),
        part_time_job: document.getElementById('part_time_job'),
        upcoming_deadline: document.getElementById('upcoming_deadline'),
        mental_health_score: document.getElementById('mental_health_score')
    };

    // Displays
    const valAge = document.getElementById('val-age');
    const valAttendance = document.getElementById('val-attendance');
    const valStudyHours = document.getElementById('val-study_hours');
    const valSelfStudy = document.getElementById('val-self_study_hours');
    const valOnlineClasses = document.getElementById('val-online_classes_hours');
    const valSocialMedia = document.getElementById('val-social_media_hours');
    const valGaming = document.getElementById('val-gaming_hours');
    const valSleep = document.getElementById('val-sleep_hours');
    const valExercise = document.getElementById('val-exercise_minutes');
    const valCaffeine = document.getElementById('val-caffeine_intake_mg');
    const valMentalHealth = document.getElementById('val-mental_health_score');

    // Outputs
    const statusBanner = document.getElementById('status-banner');
    const statusIcon = document.getElementById('status-icon');
    const statusTitle = document.getElementById('status-title');
    const statusDesc = document.getElementById('status-desc');

    const metricScore = document.getElementById('metric-score');
    const metricAttendance = document.getElementById('metric-attendance');
    const metricFocus = document.getElementById('metric-focus');
    const metricBurnout = document.getElementById('metric-burnout');

    const scoreProgressText = document.getElementById('score-progress-text');
    const scoreProgressBar = document.getElementById('score-progress-bar');
    const attendanceProgressText = document.getElementById('attendance-progress-text');
    const attendanceProgressBar = document.getElementById('attendance-progress-bar');

    const insightsContainer = document.getElementById('insights-container');

    // ----------------- Tab Switching -----------------
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            const target = btn.getAttribute('data-tab');
            document.getElementById(target).classList.add('active');
        });
    });

    // ----------------- Diagnostic Calculator -----------------
    function calculateDiagnostics() {
        // Values extraction
        const age = parseFloat(inputs.age.value);
        const attendance = parseFloat(inputs.attendance.value);
        const studyHours = parseFloat(inputs.study_hours.value);
        const selfStudyHours = parseFloat(inputs.self_study_hours.value);
        const onlineClassesHours = parseFloat(inputs.online_classes_hours.value);
        const socialMediaHours = parseFloat(inputs.social_media_hours.value);
        const gamingHours = parseFloat(inputs.gaming_hours.value);
        const sleepHours = parseFloat(inputs.sleep_hours.value);
        const exerciseMins = parseFloat(inputs.exercise_minutes.value);
        const caffeineMg = parseFloat(inputs.caffeine_intake_mg.value);
        const partTimeJob = inputs.part_time_job.value === 'Yes' ? 1 : 0;
        const upcomingDeadline = inputs.upcoming_deadline.value === 'Yes' ? 1 : 0;
        const mentalHealth = parseFloat(inputs.mental_health_score.value);

        // Update Slider Label Displays
        valAge.innerText = age;
        valAttendance.innerText = `${attendance}%`;
        valStudyHours.innerText = `${studyHours.toFixed(1)} hrs`;
        valSelfStudy.innerText = `${selfStudyHours.toFixed(1)} hrs`;
        valOnlineClasses.innerText = `${onlineClassesHours.toFixed(1)} hrs`;
        valSocialMedia.innerText = `${socialMediaHours.toFixed(1)} hrs`;
        valGaming.innerText = `${gamingHours.toFixed(1)} hrs`;
        valSleep.innerText = `${sleepHours.toFixed(1)} hrs`;
        valExercise.innerText = `${exerciseMins} mins`;
        valCaffeine.innerText = `${caffeineMg} mg`;
        valMentalHealth.innerText = mentalHealth;

        // Intermediate feature calculations matching Python app logic
        const totalLeisureScreen = socialMediaHours + gamingHours;
        const screenTimeHours = totalLeisureScreen + 2.0;

        // Focus Index (1-100)
        const focusRaw = (studyHours * 3.5 + sleepHours * 2.0 + mentalHealth * 1.5 - screenTimeHours * 1.2);
        let focusIndex = 1 + 62 * (focusRaw - (-0.11215367)) / (68.3961045 - (-0.11215367));
        focusIndex = Math.min(Math.max(focusIndex, 1), 100);

        // Burnout Level (1-100)
        const burnoutRaw = (screenTimeHours * 3.0 + upcomingDeadline * 25 + partTimeJob * 20 - sleepHours * 4.0);
        let burnoutLevel = 1 + 96 * (burnoutRaw - (-29.88057)) / (74.140395 - (-29.88057));
        burnoutLevel = Math.min(Math.max(burnoutLevel, 1), 100);

        // Productivity Score (1-100)
        const productivityRaw = (focusIndex * 2.0 + sleepHours * 1.5 - burnoutLevel * 0.4);
        let productivityScore = 1 + 97 * (productivityRaw - (-24.367417)) / (136.543746 - (-24.367417));
        productivityScore = Math.min(Math.max(productivityScore, 1), 100);

        // Final Predicted Exam Score
        const examScoreRaw = (productivityScore * 0.8 + focusIndex * 0.4 + studyHours * 0.3);
        let predictedScore = 1 + 63 * (examScoreRaw - 2.0) / (145.0 - 2.0);
        predictedScore = Math.min(Math.max(predictedScore, 1), 100);

        // Pass / Fail Threshold Checks
        const isScorePassing = predictedScore >= 33;
        const isAttendancePassing = attendance >= 75;

        // Render Metrics
        metricScore.innerText = `${predictedScore.toFixed(1)}%`;
        metricScore.className = `metric-value ${isScorePassing ? 'text-green' : 'text-red'}`;

        metricAttendance.innerText = `${attendance}%`;
        metricAttendance.className = `metric-value ${isAttendancePassing ? 'text-green' : 'text-orange'}`;

        metricFocus.innerText = focusIndex.toFixed(1);
        
        metricBurnout.innerText = `${burnoutLevel.toFixed(1)}%`;
        metricBurnout.className = `metric-value ${burnoutLevel > 65 ? 'text-red' : (burnoutLevel > 40 ? 'text-orange' : 'text-green')}`;

        // Render Progress Bars
        scoreProgressText.innerText = `${predictedScore.toFixed(1)}% / 100% (Passing Threshold: 33%)`;
        scoreProgressBar.style.width = `${predictedScore}%`;
        scoreProgressBar.className = `progress-bar-fill ${isScorePassing ? 'fill-green' : 'fill-red'}`;

        attendanceProgressText.innerText = `${attendance}% / 100% (Mandatory Threshold: 75%)`;
        attendanceProgressBar.style.width = `${attendance}%`;
        attendanceProgressBar.className = `progress-bar-fill ${isAttendancePassing ? 'fill-green' : 'fill-orange'}`;

        // Render Status Banner
        if (isScorePassing && isAttendancePassing) {
            statusBanner.className = 'status-card status-pass';
            statusIcon.innerText = '🎉';
            statusTitle.innerText = 'ELIGIBLE & PASSED';
            statusDesc.innerText = `Congratulations! You meet both academic score requirements (Predicted Score: ${predictedScore.toFixed(1)}% >= 33%) and attendance standards (Current Attendance: ${attendance}% >= 75%).`;
        } else if (isScorePassing && !isAttendancePassing) {
            statusBanner.className = 'status-card status-detained';
            statusIcon.innerText = '⚠️';
            statusTitle.innerText = 'DETAINED (Low Attendance)';
            statusDesc.innerText = `Warning! Although your academic projection is passing (${predictedScore.toFixed(1)}% >= 33%), your attendance is below the mandatory 75% threshold (Current Attendance: ${attendance}%). You risk detention from exams.`;
        } else if (!isScorePassing && isAttendancePassing) {
            statusBanner.className = 'status-card status-fail-academic';
            statusIcon.innerText = '❌';
            statusTitle.innerText = 'FAILED (Academic Shortage)';
            statusDesc.innerText = `Action Required! Your predicted exam score (${predictedScore.toFixed(1)}%) falls below the 33% passing line. Immediate learning support and schedule updates are recommended.`;
        } else {
            statusBanner.className = 'status-card status-fail-both';
            statusIcon.innerText = '🚨';
            statusTitle.innerText = 'FAILED & DETAINED';
            statusDesc.innerText = `Critical Alert! You do not meet the minimum academic performance (Predicted Score: ${predictedScore.toFixed(1)}% < 33%) and have failed to meet the attendance requirements (Current Attendance: ${attendance}% < 75%).`;
        }

        // Render AI Consultation Bullet Insights
        let htmlInsights = '';

        if (!isAttendancePassing) {
            const gap = 75 - attendance;
            htmlInsights += `
                <div class="insight-bullet" style="border-left: 5px solid #ef4444;">
                    <div class="bullet-icon">🚨</div>
                    <div>
                        <div class="bullet-title">Attendance Deficit (Shortfall: ${gap}%)</div>
                        <div class="bullet-text">Your current attendance stands at ${attendance}%. You are detained from writing examinations under university policy.</div>
                        <div class="bullet-tip">Action: Consult course coordinators and attend all remaining sessions to restore eligibility above 75%.</div>
                    </div>
                </div>
            `;
        } else {
            htmlInsights += `
                <div class="insight-bullet" style="border-left: 5px solid #10b981;">
                    <div class="bullet-icon">✅</div>
                    <div>
                        <div class="bullet-title">Attendance Clearance Verified</div>
                        <div class="bullet-text">Keeping attendance at ${attendance}% protects continuous internal review marks and ensures exam eligibility.</div>
                    </div>
                </div>
            `;
        }

        if (!isScorePassing) {
            htmlInsights += `
                <div class="insight-bullet" style="border-left: 5px solid #ef4444;">
                    <div class="bullet-icon">📖</div>
                    <div>
                        <div class="bullet-title">Critical Academic Enrichment Plan</div>
                        <div class="bullet-text">Predicted exam performance is ${predictedScore.toFixed(1)}%, which is below the 33% passing grade. High screen time or short study hours severely limit memory retention.</div>
                        <div class="bullet-tip">Action: Double daily self-study hours and schedule weekly self-mock tests on high-weightage topics.</div>
                    </div>
                </div>
            `;
        }

        if (sleepHours < 7.0) {
            htmlInsights += `
                <div class="insight-bullet" style="border-left: 5px solid #f97316;">
                    <div class="bullet-icon">🌙</div>
                    <div>
                        <div class="bullet-title">Sleep Deficiency & Cognitive Recovery</div>
                        <div class="bullet-text">Sleeping for ${sleepHours.toFixed(1)} hours restricts long-term memory integration and triggers early daytime exhaustion.</div>
                        <div class="bullet-tip">Action: Target 7.5 hours of continuous sleep and restrict mobile screens 30 minutes before bedtime.</div>
                    </div>
                </div>
            `;
        }

        if (totalLeisureScreen > 4.0) {
            htmlInsights += `
                <div class="insight-bullet" style="border-left: 5px solid #f97316;">
                    <div class="bullet-icon">📱</div>
                    <div>
                        <div class="bullet-title">Digital Distraction Audit</div>
                        <div class="bullet-text">Leisure screen time (gaming + social media) is ${totalLeisureScreen.toFixed(1)} hours. This triggers dopamine fatigue, reducing lecture focus.</div>
                        <div class="bullet-tip">Action: Set a lock-out timer on leisure applications for no more than 2 hours daily.</div>
                    </div>
                </div>
            `;
        }

        if (caffeineMg > 300 && sleepHours < 6.5) {
            htmlInsights += `
                <div class="insight-bullet" style="border-left: 5px solid #ef4444;">
                    <div class="bullet-icon">☕</div>
                    <div>
                        <div class="bullet-title">Caffeine-Sleep Disconnect</div>
                        <div class="bullet-text">High caffeine intake (${caffeineMg}mg) with short sleep duration (${sleepHours.toFixed(1)}h) elevates cortisol and feeds the Burnout Risk.</div>
                        <div class="bullet-tip">Action: Switch to herbal tea after 2:00 PM and reduce daily caffeine intake below 200mg.</div>
                    </div>
                </div>
            `;
        }

        if (exerciseMins < 30) {
            htmlInsights += `
                <div class="insight-bullet" style="border-left: 5px solid #3b82f6;">
                    <div class="bullet-icon">🏃</div>
                    <div>
                        <div class="bullet-title">Physical Stagnation</div>
                        <div class="bullet-text">Exercise is ${exerciseMins} minutes. Cardiovascular training increases cerebral blood flow, boosting retention by up to 15%.</div>
                        <div class="bullet-tip">Action: Incorporate a 20-minute daily brisk walk before study sessions.</div>
                    </div>
                </div>
            `;
        }

        if (isScorePassing && isAttendancePassing && totalLeisureScreen <= 4.0 && sleepHours >= 7.0) {
            htmlInsights += `
                <div class="insight-bullet" style="border-left: 5px solid #10b981; background: #f0fdf4;">
                    <div class="bullet-icon">🏆</div>
                    <div>
                        <div class="bullet-title">High-Efficiency Student Profile</div>
                        <div class="bullet-text">You display optimal focus, balanced sleep, and strong classroom presence. Maintain this high-performance routine!</div>
                    </div>
                </div>
            `;
        }

        insightsContainer.innerHTML = htmlInsights;
    }

    // Add listeners to all form controls
    Object.values(inputs).forEach(input => {
        input.addEventListener('input', calculateDiagnostics);
        input.addEventListener('change', calculateDiagnostics);
    });

    // Initial calculation
    calculateDiagnostics();

    // ----------------- Tab 2: Cohort Charts & Table Setup -----------------
    initCohortChartsAndTable();
});

function initCohortChartsAndTable() {
    // Generate 50 sample points for Scatter Plot
    const scatterData = [];
    for (let i = 0; i < 50; i++) {
        const study = 1 + Math.random() * 11;
        const baseScore = study * 7.5 + (Math.random() * 15 - 7.5);
        scatterData.push({
            x: parseFloat(study.toFixed(1)),
            y: parseFloat(Math.min(Math.max(baseScore, 10), 98).toFixed(1))
        });
    }

    const scatterCtx = document.getElementById('scatterChart').getContext('2d');
    new Chart(scatterCtx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Student Sample Records',
                data: scatterData,
                backgroundColor: '#3b82f6'
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: { title: { display: true, text: 'Study Hours (Daily)' } },
                y: { title: { display: true, text: 'Projected Exam Score (%)' }, min: 0, max: 100 }
            }
        }
    });

    // Histogram Chart
    const histCtx = document.getElementById('histChart').getContext('2d');
    new Chart(histCtx, {
        type: 'bar',
        data: {
            labels: ['10-20%', '20-30%', '30-40%', '40-50%', '50-60%', '60-70%', '70-80%', '80-90%', '90-100%'],
            datasets: [{
                label: 'Student Frequency',
                data: [120, 340, 680, 1150, 1420, 890, 310, 80, 10],
                backgroundColor: '#8b5cf6'
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: { title: { display: true, text: 'Score Bins' } },
                y: { title: { display: true, text: 'Student Count' } }
            }
        }
    });

    // Populate Cohort Raw Records Table
    const tableBody = document.getElementById('cohort-table-body');
    const academicLevels = ['Undergraduate', 'High School', 'Postgraduate'];
    let rowsHtml = '';

    for (let i = 1; i <= 15; i++) {
        const study = (2 + Math.random() * 9).toFixed(1);
        const sleep = (5 + Math.random() * 4).toFixed(1);
        const screen = (1 + Math.random() * 5).toFixed(1);
        const focus = (40 + Math.random() * 50).toFixed(1);
        const burnout = (15 + Math.random() * 50).toFixed(1);
        const score = (study * 8 + Math.random() * 10).toFixed(1);
        const level = academicLevels[i % 3];

        rowsHtml += `
            <tr>
                <td>#STD-${1000 + i}</td>
                <td>${18 + (i % 6)}</td>
                <td>${level}</td>
                <td>${study} hrs</td>
                <td>${sleep} hrs</td>
                <td>${screen} hrs</td>
                <td>${focus}</td>
                <td>${burnout}%</td>
                <td><strong>${score}%</strong></td>
            </tr>
        `;
    }

    tableBody.innerHTML = rowsHtml;
}
