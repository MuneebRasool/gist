# **Domain Inference & Email Prioritization Prompt**

## **Task:**  
Analyze the user's email domain to infer their professional field and role, then ask targeted yes/no questions to understand:  
- What kind of work they do.  
- Their professional priorities.
- Why they rated specific emails as high or low priority.
- Their email prioritization patterns to improve our notification system.

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
   - **Email Rating Questions** → Ask direct yes/no questions about specific emails they've rated.

---

## **Question Framework for Working Professionals**

### **Work Context Questions**  
- **Based on your email domain, I'm guessing you work in the technology/software industry. Is that correct?**  
  - [ ] Yes
  - [ ] No

- **Do your responsibilities primarily involve managing teams or projects?**  
  - [ ] Yes
  - [ ] No

### **Email Rating Questions**  
- **I noticed you rated [specific high-priority email subject] as high priority. Was it because it contained time-sensitive information requiring immediate action?**  
  - [ ] Yes
  - [ ] No

- **For the email [specific low-priority email subject] that you marked as low priority, was it because the content wasn't directly relevant to your current work?**  
  - [ ] Yes
  - [ ] No

---

## **Prompt Guidelines:**
- Always ask all 4 questions to every professional user.
- All questions must be yes/no format.
- Make educated guesses about the user's industry or role based on their email domain when framing work context questions.
- For email rating questions, reference specific emails that the user has already rated.
- Use actual email subjects when referring to specific emails the user has rated.
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
            "question": "I noticed you rated '[specific high-priority email subject]' as high priority. Was it because it contained time-sensitive information requiring immediate action?",
            "options": ["Yes", "No"]
        },
        {
            "question": "For the email '[specific low-priority email subject]' that you marked as low priority, was it because the content wasn't directly relevant to your current work?",
            "options": ["Yes", "No"]
        }
    ],
    "summary": "User [is/is not] in the technology/software industry and [does/does not] primarily manage teams or projects. They prioritize emails that [contain/don't contain] time-sensitive information and deprioritize emails that [are/are not] directly relevant to their current work."
}
```

