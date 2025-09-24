<context>
'''
{content}
'''
</context>


<task>
Extract the year when this law firm was founded or established. Look for explicit mentions of founding year, establishment date, or when the firm began.
</task>

<requirements>
- Find the specific 4-digit year when the firm was founded/established
- Only extract explicit founding years, not years of experience or other dates
- Return null if no founding year is clearly stated
- Return valid JSON with the year_founded field
</requirements>

<example_input>
# About Smith & Associates

Smith & Associates was founded in 1985 by John Smith, a veteran trial attorney with a vision to create a law firm dedicated to fighting for injured workers. 

## Our History
For over 35 years, we have been serving the community with exceptional legal representation. Since our founding, we have recovered millions in compensation for our clients.

## Our Team
Our experienced attorneys have decades of combined experience in personal injury law.
</example_input>

<expected_output>
{
  "year_founded": 1985
}
</expected_output>

<more_examples>
Input: "Johnson Law Firm was established in 1992 to serve the legal needs of injured victims."
Output: {"year_founded": 1992}

Input: "Since 2001, Martinez & Partners has been fighting for justice for personal injury victims."
Output: {"year_founded": 2001}

Input: "The Wilson Law Group opened its doors in 1978 and has been a trusted name ever since."
Output: {"year_founded": 1978}

Input: "Founded in the year 2010, our firm specializes in personal injury and workers' compensation."
Output: {"year_founded": 2010}

Input: "Established 1965. Three generations of legal excellence."
Output: {"year_founded": 1965}

Input: "We began serving clients in 1999 from our downtown office."
Output: {"year_founded": 1999}

Input: "Our firm started in the early 2000s with a focus on personal injury."
Output: {"year_founded": null}

Input: "With over 30 years of experience, our attorneys are ready to help you."
Output: {"year_founded": null}

Input: "We are a new firm dedicated to providing exceptional legal services."
Output: {"year_founded": null}

Input: "Our senior partner has been practicing law since 1982."
Output: {"year_founded": null}
</more_examples>

<extraction_guidelines>
Look for these key phrases that indicate founding year:
- "Founded in [YEAR]"
- "Established in [YEAR]"
- "Since [YEAR]"
- "Opened in [YEAR]"
- "Started in [YEAR]"
- "Began in [YEAR]"
- "Created in [YEAR]"
- "[YEAR] - Present" in firm history
- "Serving since [YEAR]"
- "In business since [YEAR]"

DO NOT extract:
- Years of experience (e.g., "30 years of experience")
- Individual attorney admission years
- Office opening years (unless it's the firm's founding)
- Years mentioned in other contexts (awards, cases, etc.)
- Vague references like "early 2000s" or "the 1990s"
- Future years or years after current year

Important notes:
- The year must be explicitly stated as the founding/establishment year
- Must be a 4-digit year between 1800 and current year
- If multiple years are mentioned, extract the earliest one that clearly refers to founding
- Return null if no clear founding year is found
</extraction_guidelines>

<validation_rules>
- year_founded: Integer (4-digit year) or null
- Must be between 1800 and current year
- This field is required in the response
- Return ONLY this field, no description or other fields
- If uncertain or no founding year found, return null
</validation_rules>