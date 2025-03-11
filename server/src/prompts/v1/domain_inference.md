# **Domain Inference & Email Prioritization Prompt**

## **Task:**  
Analyze the user’s email domain to infer their professional field and role, then ask targeted questions to understand:  
- What kind of work they do.  
- What types of emails they receive.  
- Their key priorities, so we can extract and notify them about important emails.  

---

## **Steps for Analysis:**  
1. **Domain Inference:**  
   - Check for **keywords** in the domain (e.g., `med`, `tech`, `consult`).  
   - Recognize **institutional patterns** (`mit.edu` → student, `ibm.com` → corporate).  
   - Identify **company vs. personal emails** (e.g., `@gmail.com` is general, `@microsoft.com` is corporate).  

2. **Question Flow:**  
   - **For corporate/work emails** → Focus on role, workflow, and email types.  
   - **For personal emails (e.g., Gmail, Yahoo)** → Ask about freelance work, side projects, or general email habits.  
   - **For student emails** → Ask about coursework, deadlines, and professional interests.  

---

## **Question Framework Based on Email Type**

### **1️⃣ Corporate/Company Emails (`@company.com`)**  
- **Primary Role?**  
  - [ ] Executive/Manager  
  - [ ] Engineer/Developer  
  - [ ] Sales/Marketing  
  - [ ] Operations/Admin  

- **Which emails do you check first?**  
  - [ ] Meeting invites  
  - [ ] Client requests  
  - [ ] Internal updates  
  - [ ] Project deadlines  

- **What would you like to be notified about?**  
  - [ ] High-priority tasks  
  - [ ] Follow-ups & deadlines  
  - [ ] Billing/invoices  
  - [ ] Client escalations  

---

### **2️⃣ Personal Emails (`@gmail.com`, `@yahoo.com`, etc.)**  
- **How do you use this email?**  
  - [ ] Personal communication  
  - [ ] Freelance/gig work  
  - [ ] Side projects/startup  
  - [ ] Job applications  

- **What kind of important emails do you get?**  
  - [ ] Work-related tasks  
  - [ ] Subscription/billing updates  
  - [ ] Networking/opportunities  
  - [ ] Event/meeting invites  

- **Would you like reminders for?**  
  - [ ] Unread important emails  
  - [ ] Follow-ups on job applications  
  - [ ] Payment reminders  
  - [ ] Upcoming events  

---

### **3️⃣ Student Emails (`@university.edu`)**  
- **What’s your focus area?**  
  - [ ] Engineering/Tech  
  - [ ] Business/Finance  
  - [ ] Medical/Bio  
  - [ ] Other  

- **What types of emails are most important to you?**  
  - [ ] Assignment deadlines  
  - [ ] Class announcements  
  - [ ] Internship/job opportunities  
  - [ ] Scholarship/financial aid updates  

- **Would you like reminders for?**  
  - [ ] Exam dates & deadlines  
  - [ ] Job application due dates  
  - [ ] Important faculty emails  
  - [ ] Networking events  

---

## **Final JSON Output Format**
```json
{
    "domain": "<inferred domain>",
    "questions": [
        {
            "question": "Which emails do you check first?",
            "options": ["Meeting invites", "Client requests", "Internal updates", "Project deadlines"]
        },
        {
            "question": "What would you like to be notified about?",
            "options": ["High-priority tasks", "Follow-ups & deadlines", "Billing/invoices", "Client escalations"]
        }
    ],
    "summary": "User has a corporate email, likely in a managerial or technical role. They want to prioritize important tasks, follow-ups, and client interactions."
}


NOTE : question can either have 2 options or 4
