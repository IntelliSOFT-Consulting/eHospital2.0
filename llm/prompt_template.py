def generate_prompt(patient_data):
    prompt: str = f""" 
Hello, I need you to create a concise, patient-friendly explanation of the following medical 
encounter. Provided with the patient's details and the diagnosis, 
act as a medical assistant explaining the diagnosis and treatment to the patient. 

General guidelines for the explanation include
- Keep messages concise in a brief paragraph 200 characters or less for SMS.
- Use simple, non-technical language.
- Provide actionable advice or reminders.
- Use a friendly and respectful tone.

The message should include: 
1. Inform the patient that message follows their visit to St Joseph's Hospital.
2. Summary of the basic patient information e.g vitals, 
3. Diagnosis - the name of the diagnosis
4. More information about the diagnosis - simple (layman's) explanation about the diagnosis
5. Tests ordered and results and what they mean (if any)
6. Treatment plan - instead of listing the drugs given to the patient, figure out what drug class they belong to and explain the purpose of the drug class.
7. Provide lifestyle recommendations on what to do to prevent re-occurrence of the disease (if any) or alleviate the disease in cases of chronic illnesses
8. Inform the patient of emergency signs to look out for the particular diagnosis (if any)
9. Reminder to follow the instructions and take medications as prescribed by the doctor


### **Patient Details**
- **Age**: {patient_data['age']}
- **Gender**: {patient_data['gender']}
- **Vitals**: BP: {patient_data['blood_pressure']}, Heart Rate: {patient_data['heart_rate']}, Temperature: {patient_data['temperature']}
### **Diagnosis**
The patient has been diagnosed with **{patient_data['diagnosis']}**.

### **Tests Ordered & Results**
{format_tests(patient_data['tests'])}

### **Treatment**
- **Medications**: {", ".join(patient_data['medications'])}


"""
    return prompt


def format_tests(tests):
    """
        Converts a list of test dictionaries into a formatted string.
        """
    if not tests:
        return "No tests ordered."

    test_summary = ""
    for test in tests:
        test_summary += f"- **{test['name']}**: {test['result']} (Reason: {test['reason']})\n"
    return test_summary
