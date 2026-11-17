/**
 * PulseGuard AI - Client Controller
 * Manages intake form submission, scenario pre-filling, live dashboard polling, and modal views.
 */

let currentFilter = "ALL";

// Scenario Presets for 1-Click Demos
const SCENARIOS = {
  critical: {
    full_name: "Eleanor Vance",
    age: 54,
    gender: "Female",
    contact_email: "eleanor.vance@example.com",
    contact_phone: "+1 (555) 234-5678",
    chief_complaint: "Crushing chest pressure radiating to left arm and jaw with cold sweat",
    symptoms_detail: "Onset 40 minutes ago while seated. Constant tight pressure, difficulty catching breath, sudden dizziness and nausea. Never experienced this severity before.",
    duration: "40 minutes",
    pre_existing_conditions: "Hypertension, Hyperlipidemia"
  },
  medium: {
    full_name: "David Miller",
    age: 32,
    gender: "Male",
    contact_email: "david.m@example.com",
    contact_phone: "+1 (555) 872-1092",
    chief_complaint: "Persistent high fever (102.8 F) with productive cough and wheezing",
    symptoms_detail: "Fever and chills for past 3 days. Green sputum, fatigue, shortness of breath after climbing home stairs. Oral antipyretics provide only temporary relief.",
    duration: "3 days",
    pre_existing_conditions: "Childhood asthma"
  },
  low: {
    full_name: "Clara Oswald",
    age: 26,
    gender: "Female",
    contact_email: "clara.o@example.com",
    contact_phone: "+1 (555) 431-7729",
    chief_complaint: "Mild itchy skin rash on right forearm after gardening",
    symptoms_detail: "Appeared yesterday morning. Mild erythematous patches with minor itching. No fever, no facial swelling, no breathing difficulties.",
    duration: "24 hours",
    pre_existing_conditions: "None"
  }
};

function fillScenario(type) {
  const data = SCENARIOS[type];
  if (!data) return;

  document.getElementById("fullName").value = data.full_name;
  document.getElementById("age").value = data.age;
  document.getElementById("gender").value = data.gender;
  document.getElementById("contactEmail").value = data.contact_email;
  document.getElementById("contactPhone").value = data.contact_phone;
  document.getElementById("chiefComplaint").value = data.chief_complaint;
  document.getElementById("symptomsDetail").value = data.symptoms_detail;
  document.getElementById("duration").value = data.duration;
  document.getElementById("conditions").value = data.pre_existing_conditions;

  // Visual flash on form to indicate filled data
  const formWrapper = document.querySelector(".form-wrapper");
  formWrapper.style.borderColor = "#38BDF8";
  setTimeout(() => { formWrapper.style.borderColor = ""; }, 400);
}

async function handleIntakeSubmit(event) {
  event.preventDefault();
  const submitBtn = document.getElementById("submitBtn");
  const btnText = submitBtn.querySelector(".btn-text");
  
  // Collect payload
  const formData = new FormData(event.target);
  const payload = {
    full_name: formData.get("full_name"),
    age: parseInt(formData.get("age")),
    gender: formData.get("gender"),
    contact_email: formData.get("contact_email") || "",
    contact_phone: formData.get("contact_phone") || "",
    chief_complaint: formData.get("chief_complaint"),
    symptoms_detail: formData.get("symptoms_detail"),
    duration: formData.get("duration") || "Not specified",
    pre_existing_conditions: formData.get("pre_existing_conditions") || "None"
  };

  try {
    btnText.textContent = "⚡ Running AI Triage & Dispatching Alerts...";
    submitBtn.disabled = true;

    const response = await fetch("/api/intake", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!response.ok) throw new Error("Server error during intake processing");

    const result = await response.json();
    displayTriageResult(result);
  } catch (err) {
    alert("Error processing intake: " + err.message);
  } finally {
    btnText.textContent = "Submit Intake & Trigger AI Triage Pipeline";
    submitBtn.disabled = false;
  }
}

function displayTriageResult(data) {
  const assessment = data.assessment;
  const resultCard = document.getElementById("resultCard");
  const resultBadge = document.getElementById("resultBadge");

  // Populate data
  document.getElementById("resultPatientId").textContent = data.patient_id;
  document.getElementById("resultScore").textContent = `${assessment.urgency_score}/100`;
  document.getElementById("resultDept").textContent = assessment.department;
  document.getElementById("resultRationale").textContent = assessment.clinical_rationale;
  document.getElementById("resultPhysicianNotes").textContent = assessment.physician_summary;
  document.getElementById("resultPatientMsg").textContent = `"${assessment.patient_message}"`;

  // Badge styling
  resultBadge.textContent = assessment.urgency;
  resultBadge.className = "result-status-badge";
  if (assessment.urgency === "CRITICAL") {
    resultBadge.classList.add("badge-critical");
  } else if (assessment.urgency === "MEDIUM") {
    resultBadge.classList.add("badge-medium");
  } else {
    resultBadge.classList.add("badge-low");
  }

  // Show card and scroll into view
  resultCard.style.display = "block";
  resultCard.scrollIntoView({ behavior: "smooth", block: "start" });
}

function resetForm() {
  document.getElementById("intakeForm").reset();
  const resultCard = document.getElementById("resultCard");
  resultCard.style.display = "none";
  window.scrollTo({ top: 0, behavior: "smooth" });
}

/* ============================================================
   STAFF DASHBOARD LOGIC
   ============================================================ */

async function loadDashboardData() {
  await Promise.all([fetchStats(), fetchPatientsQueue()]);
}

async function fetchStats() {
  try {
    const res = await fetch("/api/stats");
    if (!res.ok) return;
    const stats = await res.json();
    
    document.getElementById("statTotal").textContent = stats.total;
    document.getElementById("statCritical").textContent = stats.critical;
    document.getElementById("statMedium").textContent = stats.medium;
    document.getElementById("statLow").textContent = stats.low;
  } catch (e) {
    console.error("Failed fetching stats", e);
  }
}

async function fetchPatientsQueue() {
  const tbody = document.getElementById("patientsTableBody");
  if (!tbody) return;

  try {
    const res = await fetch(`/api/patients?urgency=${currentFilter}`);
    if (!res.ok) return;
    const data = await res.json();
    const patients = data.patients;

    if (patients.length === 0) {
      tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; padding: 2.5rem; color: #94A3B8;">No patients currently in this queue.</td></tr>`;
      return;
    }

    tbody.innerHTML = patients.map(p => {
      const urgencyClass = p.urgency === "CRITICAL" ? "triage-critical" :
                           p.urgency === "MEDIUM" ? "triage-medium" : "triage-low";
      
      const timeFormatted = p.created_at ? p.created_at.split(" ")[1] || p.created_at : "Recent";

      return `
        <tr>
          <td><code style="color: #38BDF8; font-weight:700;">${p.id}</code></td>
          <td>
            <div class="patient-cell">
              <span class="patient-name">${escapeHtml(p.full_name)}</span>
              <span class="patient-demographics">${p.age}yo • ${p.gender}</span>
            </div>
          </td>
          <td style="max-width: 280px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
            ${escapeHtml(p.chief_complaint)}
          </td>
          <td>
            <span class="triage-badge ${urgencyClass}">${p.urgency}</span>
          </td>
          <td><strong>${p.urgency_score}</strong>/100</td>
          <td style="color: #cbd5e1; font-weight:500;">${escapeHtml(p.department)}</td>
          <td style="color: #64748B; font-size: 0.8rem;">${timeFormatted}</td>
          <td>
            <button class="btn-view-details" onclick="viewPatientDetails('${p.id}')">Inspect SBAR</button>
          </td>
        </tr>
      `;
    }).join("");
  } catch (e) {
    console.error("Failed loading patient table", e);
  }
}

function setFilter(filter) {
  currentFilter = filter;
  document.querySelectorAll(".filter-btn").forEach(btn => {
    btn.classList.toggle("active", btn.getAttribute("data-filter") === filter);
  });
  fetchPatientsQueue();
}

async function viewPatientDetails(patientId) {
  try {
    const res = await fetch(`/api/patients/${patientId}`);
    if (!res.ok) throw new Error("Could not load patient");
    const p = await res.json();

    document.getElementById("modalPatientId").textContent = p.id;
    document.getElementById("modalPatientName").textContent = p.full_name;
    document.getElementById("modalAgeGender").textContent = `${p.age} years old • ${p.gender}`;
    document.getElementById("modalEmail").textContent = p.contact_email || "Not provided";
    document.getElementById("modalPhone").textContent = p.contact_phone || "Not provided";
    document.getElementById("modalDuration").textContent = p.duration || "Not specified";
    document.getElementById("modalConditions").textContent = p.pre_existing_conditions || "None";

    document.getElementById("modalComplaint").textContent = p.chief_complaint;
    document.getElementById("modalSymptoms").textContent = p.symptoms_detail;

    document.getElementById("modalDept").textContent = p.department;
    document.getElementById("modalScore").textContent = `Urgency Risk: ${p.urgency_score}/100`;
    document.getElementById("modalRationale").textContent = p.clinical_rationale;

    document.getElementById("modalPhysicianNotes").textContent = p.physician_summary;
    document.getElementById("modalPatientMsg").textContent = `"${p.patient_message}"`;

    const badge = document.getElementById("modalUrgencyBadge");
    badge.textContent = p.urgency;
    badge.className = "badge";
    if (p.urgency === "CRITICAL") badge.classList.add("badge-critical");
    else if (p.urgency === "MEDIUM") badge.classList.add("badge-medium");
    else badge.classList.add("badge-low");

    document.getElementById("detailModal").style.display = "flex";
  } catch (e) {
    alert("Error fetching patient details: " + e.message);
  }
}

function closeModal() {
  document.getElementById("detailModal").style.display = "none";
}

function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
