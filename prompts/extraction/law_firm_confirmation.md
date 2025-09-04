<context>
'''
{content}
'''
</context>

<task>
Analyze the above content and extract information about the law firm, including a description and classification of the firm type.
</task>

<requirements>
- Extract a single sentence description of the law firm (maximum 30 words)
- Determine if this is actually a law firm website (not a directory, referral service, or other business)
- Determine if the firm handles personal injury cases
- Return valid JSON only
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
  "short_description": "Smith & Associates is a full-service California law firm specializing in personal injury, business litigation, real estate, and estate planning.",
  "is_law_firm": true,
  "is_personal_injury_firm": true
}
</expected_output>

<more_examples>
Input: "Johnson Accounting Services provides tax preparation, bookkeeping, and financial consulting for small businesses in Texas."
Output: {"short_description": "Johnson Accounting Services provides tax preparation and financial consulting for small businesses in Texas.", "is_law_firm": false, "is_personal_injury_firm": false}

Input: "The Martinez Firm exclusively represents injured workers in workers' compensation and personal injury claims throughout Texas."
Output: {"short_description": "The Martinez Firm exclusively represents injured workers in workers' compensation and personal injury claims throughout Texas.", "is_law_firm": true, "is_personal_injury_firm": true}

Input: "Wilson & Partners is a boutique intellectual property firm protecting patents, trademarks, and copyrights for technology companies."
Output: {"short_description": "Wilson & Partners is a boutique intellectual property firm protecting patents, trademarks, and copyrights for technology companies.", "is_law_firm": true, "is_personal_injury_firm": false}

Input: "LegalZoom helps you create legal documents and connect with attorneys for your business and personal needs."
Output: {"short_description": "LegalZoom helps create legal documents and connects users with attorneys for business and personal needs.", "is_law_firm": false, "is_personal_injury_firm": false}
</more_examples>

<classification_guidelines>
For is_law_firm = true:
- Must be an actual law firm or law office
- Has licensed attorneys providing legal services
- Not a directory, referral service, or legal tech platform

For is_personal_injury_firm = true:
- Handles personal injury, auto accidents, slip and fall cases
- Represents injured victims seeking compensation
- Includes workers' compensation, medical malpractice, wrongful death
- May also handle other practice areas but must include PI work
</classification_guidelines>

<validation_rules>
- short_description: Single sentence under 30 words
- is_law_firm: Boolean value (true/false)
- is_personal_injury_firm: Boolean value (true/false)
- All three fields are required in the response
</validation_rules>