<context>
{content}
</context>

<task>
Extract practice areas from this law firm website. You need to:
1. Create a list of practice areas EXACTLY as they appear on the website (preserve their wording)
2. Determine if they handle specific categories of cases
</task>

<requirements>
- Extract practice areas exactly as listed on the website (don't paraphrase or summarize)
- Set boolean flags for the 6 specific categories based on whether they handle those types
- Look for practice area lists, services sections, "cases we handle", menu items, etc.
- Return valid JSON with all required fields
</requirements>

<extraction_guidelines>
First, extract the exact list of practice areas as shown on the website. Look for:
- "Practice Areas" or "Areas of Practice" sections
- "Services" or "Legal Services" sections  
- "Cases We Handle" sections
- Navigation menus listing practice areas
- Bullet point lists of case types

Then, determine if they handle these specific categories:

**motor_vehicle_accident** (set to true if they handle ANY of these):
- Car accidents, auto accidents, vehicle accidents
- Truck accidents, semi accidents, 18-wheeler accidents
- Motorcycle accidents, bike accidents
- Bus accidents, Uber/Lyft accidents
- Any mention of motor vehicle, traffic accidents, or road accidents

**premises_liability** (set to true if they handle ANY of these):
- Slip and fall, trip and fall
- Premises liability
- Unsafe property conditions
- Store/restaurant/hotel accidents
- Inadequate security
- Dog bites (often part of premises liability)

**wrongful_death** (set to true if they handle):
- Wrongful death
- Fatal accidents
- Death claims

**product_liability** (set to true if they handle):
- Product liability
- Defective products
- Dangerous products
- Manufacturing defects

**workplace_injury** (set to true if they handle ANY of these):
- Workers' compensation, workers comp
- Workplace injuries, work injuries
- On-the-job injuries
- Construction accidents
- Industrial accidents

**medical_malpractice** (set to true if they handle):
- Medical malpractice
- Medical negligence
- Doctor/hospital errors
- Birth injuries
- Surgical errors
</extraction_guidelines>

<output_format>
Return a JSON object with this exact structure:
{
  "practice_areas_list": [array of strings - exact practice areas as listed on website],
  "motor_vehicle_accident": [boolean],
  "premises_liability": [boolean],
  "wrongful_death": [boolean],
  "product_liability": [boolean],
  "workplace_injury": [boolean],
  "medical_malpractice": [boolean]
}

Example:
{
  "practice_areas_list": [
    "Car Accidents",
    "Truck Accidents", 
    "Slip & Fall Injuries",
    "Medical Malpractice",
    "Wrongful Death",
    "Workers' Compensation"
  ],
  "motor_vehicle_accident": true,
  "premises_liability": true,
  "wrongful_death": true,
  "product_liability": false,
  "workplace_injury": true,
  "medical_malpractice": true
}

CRITICAL:
- Extract practice areas EXACTLY as written on the website
- Only set categories to true if they explicitly mention handling those types of cases
- If no practice areas are found, return empty array []
- Don't infer or assume - only extract what's explicitly stated
</output_format>