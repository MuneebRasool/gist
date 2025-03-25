## **Task:**  
Analyze the user's email domain to infer their professional field and role, then ask targeted yes/no questions to understand:  
- What kind of work they do.  
- Their professional priorities.
- Their general email prioritization patterns to improve our notification system.

---

## Input Format

You will receive a JSON object containing:
1. **domain** - The professional domain/industry of the user (e.g., "tech", "medical", "consulting")
3. **emails** - Array of email objects with:
   - `subject`: Email subject line
   - `snippet`: Brief preview of the email content
   - `body` : the main content of the email
   - `from`: Sender name
   - `rating`: User's importance rating (1-5, where 5 is most important and 1 is least important)
     - **Rating Scale:**
       - **1**: Spam – Unwanted, irrelevant, or outright junk. → Goes to Spam/Trash
       - **2**: Low Relevance – Not immediately useful but also not junk (e.g., soft promotions, secondary newsletters). → Likely auto-archived or filtered into a lesser-priority Library category
       - **3**: For Later / Keep on File – Important but not requiring action (e.g., receipts, confirmations, newsletters of interest). → Goes to Library
       - **4**: Important – Needs attention but not urgent (e.g., follow-ups, pending approvals). → Goes to In View or Library depending on time-sensitivity
       - **5**: Priority – Urgent and actionable (e.g., calendar invites, investor emails, deadlines). → Goes to In View

## **Steps for Analysis:**  
1. **Domain Inference:**  
   - Check for **keywords** in the domain (e.g., `med`, `tech`, `consult`).  
   - Recognize **company patterns** (`ibm.com` → corporate, `accenture.com` → consulting).  
   - Identify **industry indicators** in the domain (e.g., `healthcare`, `fintech`, `legal`).  

2. **Question Focus:**  
   - **Work Context Questions** → Ask specific yes/no questions about their role and industry.
   - **Priority Pattern Questions** → Ask general questions about their email prioritization habits based on domain context.

---

## **Question Framework for Working Professionals**

### **Work Context Questions**  
- **Based on your email domain, I'm guessing you work in the technology/software industry. Is that correct?**  
  - [ ] Yes
  - [ ] No

- **Do your responsibilities primarily involve managing teams or projects?**  
  - [ ] Yes
  - [ ] No

### **Priority Pattern Questions**  
- **In your role, do you typically need to respond to time-sensitive requests within 24 hours?**  
  - [ ] Yes
  - [ ] No

- **Do you often receive emails that require coordination with multiple stakeholders?**  
  - [ ] Yes
  - [ ] No

---

## **Prompt Guidelines:**
- Always ask all 4 questions to every professional user.
- All questions must be yes/no format.
- Make educated guesses about the user's industry or role based on their email domain when framing work context questions.
- For priority pattern questions, focus on general patterns relevant to their domain rather than specific emails.
- Use the domain context to tailor questions about email handling patterns.
- If the answer to a question is "No," consider following up with another yes/no question about a different potential aspect.

---

## **Final JSON Output Format**
```json
{
    "domain": "<inferred domain>",
    "questions": [
        {
            "question": "Based on your email domain, I'm guessing you work in the technology/software industry. Is that correct?",
            "options": ["Yes", "No"]
        },
        {
            "question": "Do your responsibilities primarily involve managing teams or projects?",
            "options": ["Yes", "No"]
        },
        {
            "question": "In your role, do you typically need to respond to time-sensitive requests within 24 hours?",
            "options": ["Yes", "No"]
        },
        {
            "question": "Do you often receive emails that require coordination with multiple stakeholders?",
            "options": ["Yes", "No"]
        }
    ],
    "summary": "User [is/is not] in the technology/software industry and [does/does not] primarily manage teams or projects. Their role [requires/does not require] quick responses to time-sensitive requests and [involves/does not involve] frequent stakeholder coordination."
}
```

