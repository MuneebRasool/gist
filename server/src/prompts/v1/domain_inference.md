# Domain Inference from Email

**Task**: Analyze the user's email domain to infer their professional domain (medical, tech, consulting) and based on the domain, craft few questions with options to help them better understand their role and responsibilities.

**Rules**:
1. **Steps for Analysis**:  
   - **Keyword Identification**: Check for domain/subdomain components (e.g., `med`, `health`, `tech`, `ai`, `consult`, `advisory`).  
   - **Abbreviation Mapping**: Recognize institutional abbreviations (e.g., `mit.edu` → tech, `gsb.columbia.edu` → consulting).  
   - **Industry Terms**: Prioritize terms like `clinic`, `hospital` (medical), `software`, `cloud` (tech), or `strategy`, `advisory` (consulting).  
   - **Contextual Inference**: If ambiguous, use institutional context (e.g., `harvardmed.edu` → medical).  

2. **Output Rules**:  
   - Return **one domain** (medical, tech, consulting).  
   - If uncertain, choose the **closest match** based on keywords or context.  

---

## Examples  
- `user@harvardmed.edu` → **medical**  
- `contact@siliconvalleytech.net` → **tech**  
- `team@bainconsulting.org` → **consulting**  
- `john@ai-research.org` → **tech**

### Examples of Questions to Ask the User
#### **Medical Domain**  
1. **Primary Role**:  
   - [ ] Clinician (e.g., doctor, nurse)  
   - [ ] Administrator (e.g., hospital management)  
   - [ ] Researcher (e.g., clinical trials)  
   - [ ] Other  

2. **Top Challenge**:  
   - [ ] Patient no-shows  
   - [ ] EHR system inefficiencies  
   - [ ] Staff scheduling conflicts  
   - [ ] Regulatory compliance  

3. **Critical Tool**:  
   - [ ] Epic/Cerner  
   - [ ] Calendly/Appointment scheduling apps  
   - [ ] Zoom/Telehealth platforms  
   - [ ] Custom internal software
---

#### **Tech Domain**  
1. **Primary Role**:  
   - [ ] Developer/Engineer  
   - [ ] Product Manager  
   - [ ] DevOps/Cloud Specialist  
   - [ ] Other  

2. **Top Challenge**:  
   - [ ] Scalability issues  
   - [ ] Security vulnerabilities  
   - [ ] Legacy system integration  
   - [ ] Meeting sprint deadlines  

3. **Key Tool**:  
   - [ ] AWS/Azure/GCP  
   - [ ] Jira/Asana  
   - [ ] GitHub/GitLab  
   - [ ] Kubernetes/Docker  

---
#### **Consulting Domain**  
1. **Primary Role**:  
   - [ ] Strategy Consultant  
   - [ ] Data Analyst  
   - [ ] Client Engagement Manager  
   - [ ] Other  

2. **Top Challenge**:  
   - [ ] Client ROI justification  
   - [ ] Data collection/accuracy  
   - [ ] Stakeholder alignment  
   - [ ] Tight deadlines  

3. **Key Tool**:  
   - [ ] Excel/Google Sheets  
   - [ ] Tableau/Power BI  
   - [ ] Salesforce  
   - [ ] Miro/Mural  

---

#### **Cross-Domain**  
1. **Work Focus**:  
   - [ ] Process optimization  
   - [ ] Data analysis  
   - [ ] Client/customer interaction  
   - [ ] Technical execution  

2. **Urgent Need**:  
   - [ ] Automation  
   - [ ] Training/resources  
   - [ ] Better collaboration tools  
   - [ ] Faster decision-making  

---

### Usage Tips:  
- Pair with **domain inference** (e.g., show medical questions if email domain is `@mayoclinic.org`).  
- Add an optional free-text field for "Other" responses.  
- Use responses to tailor content, product features, or communication style
---
Return the response in JSON format with the following keys:
 {
    "domain": <inferred domain>
    "questions": [
        {
            "question": <question to ask the user>,
            "options": ['option1', 'option2', 'option3']
        }
    ]
    ]   
 }