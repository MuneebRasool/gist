# **Domain Inference & Email Prioritization Prompt**

## **Task:**  
Analyze the user's email domain to infer their professional field and role, then ask targeted questions to understand:  
- What kind of work they do.  
- Their professional priorities.
- Why they rated specific emails as high or low priority.
- Their email prioritization patterns to improve our notification system.

---

## **Steps for Analysis:**  
1. **Domain Inference:**  
   - Check for **keywords** in the domain (e.g., `med`, `tech`, `consult`).  
   - Recognize **company patterns** (`ibm.com` → corporate, `accenture.com` → consulting).  
   - Identify **industry indicators** in the domain (e.g., `healthcare`, `fintech`, `legal`).  

2. **Question Focus:**  
   - **Work Context Questions** → Understand role and professional priorities.
   - **Email Rating Questions** → Learn why they rated specific emails as high or low priority.

---

## **Question Framework for Working Professionals**

### **Work Context Questions**  
- **What industry do you primarily work in?**  
  - [ ] Technology/Software  
  - [ ] Finance/Banking  
  - [ ] Healthcare/Medical  
  - [ ] Consulting/Professional Services  

- **What best describes your primary responsibilities?**  
  - [ ] Managing teams and projects  
  - [ ] Technical development/implementation  
  - [ ] Client relations and business development  
  - [ ] Operations and administration  

### **Email Rating Questions**  
- **I noticed you rated [specific high-priority email subject] as high priority. What was your main reason?**  
  - [ ] Time-sensitive information requiring immediate action  
  - [ ] It's from a key stakeholder or executive  
  - [ ] It directly impacts your current project/deliverable  
  - [ ] It contains critical information you needed to reference  

- **I see you marked [specific low-priority email subject] as low priority. What was your reasoning?**  
  - [ ] It's an automated notification that doesn't require action  
  - [ ] The content isn't directly relevant to your current work  
  - [ ] It's informational and can be reviewed later  
  - [ ] It's a routine update with no urgent components  

---

## **Prompt Guidelines:**
- Always ask all 4 questions to every professional user.
- Each question must have exactly 4 options.
- For email rating questions, reference specific emails that the user has already rated.
- Use actual email subjects when referring to specific emails the user has rated.

---

## **Final JSON Output Format**
```json
{
    "domain": "<inferred domain>",
    "questions": [
        {
            "question": "What industry do you primarily work in?",
            "options": ["Technology/Software", "Finance/Banking", "Healthcare/Medical", "Consulting/Professional Services"]
        },
        {
            "question": "What best describes your primary responsibilities?",
            "options": ["Managing teams and projects", "Technical development/implementation", "Client relations and business development", "Operations and administration"]
        },
        {
            "question": "I noticed you rated '[specific high-priority email subject]' as high priority. What was your main reason?",
            "options": ["Time-sensitive information requiring immediate action", "It's from a key stakeholder or executive", "It directly impacts your current project/deliverable", "It contains critical information you needed to reference"]
        },
        {
            "question": "I see you marked '[specific low-priority email subject]' as low priority. What was your reasoning?",
            "options": ["It's an automated notification that doesn't require action", "The content isn't directly relevant to your current work", "It's informational and can be reviewed later", "It's a routine update with no urgent components"]
        }
    ],
    "summary": "User is a working professional in the [industry] field with [role type] responsibilities. They prioritize emails that [key priority factors] and tend to deprioritize [low priority factors]."
}
```

