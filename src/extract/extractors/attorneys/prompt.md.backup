<task>
You are looking at website content. Extract all attorneys/lawyers from this law firm website. You need to:
1. Find all attorneys mentioned on the website
2. Extract their full names and any titles or positions
3. Extract a brief bio snippet if available
</task>

Here is the content.
<context>
{content}
</context>


<requirements>
- Extract ALL attorneys/lawyers mentioned, including partners, associates, and of counsel
- Capture their full names as displayed
- Include their titles/positions if mentioned (e.g., "Partner", "Senior Attorney", "Managing Partner")
- Return valid JSON with all required fields
- IMPORTANT: Only extract attorneys with explicitly stated PERSONAL NAMES - do not generate or guess names
- An attorney name MUST be a PERSON'S NAME (first name and/or last name)
- If no attorney names are found in the content, return empty attorneys array
- NEVER generate placeholder or example attorney names
</requirements>

<extraction_guidelines>
VALID attorney name patterns (EXTRACT THESE):
- "John Smith, Esq."
- "Attorney Jane Doe"
- "Managing Partner John Smith"
- "Sarah Johnson, Partner"
- Names with titles like Partner, Associate, Of Counsel
- Must contain an actual person's name (first and/or last name)

INVALID - DO NOT EXTRACT THESE:
- Company/firm names: "Smith & Associates", "1-800-HURT911", "The Law Offices of..."
- Generic descriptions: "our attorneys", "experienced lawyers", "Atlanta truck accident lawyers"
- Service descriptions: "personal injury team", "legal department"
- Phone numbers or marketing names: "1-800-ANYTHING"
- Generic references: "truck accident lawyers", "personal injury attorneys"
- Groups without names: "our team of attorneys", "experienced legal professionals"

For each attorney, extract:
- **name**: Full name as displayed (required) - MUST be a person's actual name
- **title**: Their position/title (e.g., "Partner", "Associate", "Of Counsel", "Managing Attorney")
- **bio_snippet**: A brief excerpt from their bio if available (max 100 words)
</extraction_guidelines>

<output_format>
Return a JSON object with this exact structure:
{
  "attorneys": [
    {
      "name": "string - full name",
      "title": "string - position/title or null",
      "bio_snippet": "string - brief bio excerpt or null"
    }
  ],
  "total_attorneys": number
}

If no actual attorney names are found, return:
{
  "attorneys": [],
  "total_attorneys": 0
}
</output_format>

CRITICAL RULES:
1. Only extract PERSONAL NAMES of actual attorneys
2. Company names, phone numbers, and generic descriptions are NOT attorney names
3. If the content only mentions "our attorneys" or similar without actual names, return empty array
4. When in doubt, return empty array rather than extracting non-names