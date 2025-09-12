<context>
'''
{content}
'''
</context>


<task>
Analyze the above content and classify whether this is a law firm and whether they handle personal injury cases.
</task>

<requirements>
- Determine if this is actually a law firm website (not a directory, referral service, or other business)
- Determine if the firm takes on personal injury cases or clients
- Return valid JSON only with two boolean fields
</requirements>

<example_input>
# Smith & Associates

Smith & Associates is a full-service law firm serving individuals and businesses throughout California. Our practice areas include personal injury, business litigation, real estate, and estate planning.

## Practice Areas
- Personal Injury & Auto Accidents
- Business Litigation  
- Real Estate Law
- Estate Planning

## Contact Us
Call us at 555-123-4567 for a free consultation.
</example_input>

<expected_output>
json{
  "is_law_firm": true,
  "is_personal_injury_firm": true
}
</expected_output>

<more_examples>
Input: "The Martinez Firm exclusively represents injured workers in workers' compensation and personal injury claims throughout Texas."
Output: {"is_law_firm": true, "is_personal_injury_firm": true}

Input: "Our firm handles nursing home abuse, medical malpractice, and catastrophic injury cases."
Output: {"is_law_firm": true, "is_personal_injury_firm": true}

Input: "We handle slip and fall accidents, dog bites, and construction site injuries for union workers."
Output: {"is_law_firm": true, "is_personal_injury_firm": true}

Input: "Wilson & Partners is a boutique intellectual property firm protecting patents, trademarks, and copyrights."
Output: {"is_law_firm": true, "is_personal_injury_firm": false}

Input: "LegalZoom helps you create legal documents and connect with attorneys."
Output: {"is_law_firm": false, "is_personal_injury_firm": false}

Input: "Our practice areas include family law, criminal defense, and personal injury."
Output: {"is_law_firm": true, "is_personal_injury_firm": true}

Input: "We are a tax and estate planning firm serving high net worth individuals."
Output: {"is_law_firm": true, "is_personal_injury_firm": false}
</more_examples>

<classification_guidelines>
For is_law_firm = true:
- Must be an actual law firm or law office
- Has licensed attorneys providing legal services
- Not a directory, referral service, or legal tech platform

For is_personal_injury_firm = true:
- Firm accepts or takes on ANY type of personal injury cases or clients, including:
  * Car/automobile accidents
  * Premises liability (slip and fall)
  * Product liability
  * Wrongful death
  * Workplace injuries/workers' compensation
  * Medical malpractice
  * Motorcycle, truck, pedestrian accidents
- Even if personal injury is a minor practice area among others, mark as true
- Only mark false if the firm does NOT accept or handle injury cases or clients
</classification_guidelines>

<validation_rules>
- is_law_firm: Boolean value (true/false)
- is_personal_injury_firm: Boolean value (true/false)
- Both fields are required in the response
- Return ONLY these two fields, no description or other fields
</validation_rules>