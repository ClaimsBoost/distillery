<context>
'''
{content}
'''
</context>

<task>
Extract all office locations from the above law firm website content and return them in the specified JSON format. Focus only on physical office addresses where the firm operates.
</task>

<requirements>
- Parse the markdown content thoroughly
- Identify all sections that might contain office information
- Extract complete address information when available
- Format addresses consistently
- Deduplicate addresses: if the same location appears multiple times with different formatting, only include it once
- Use the most complete version of each address (prefer versions with ZIP codes over those without)
- Return valid JSON only
</requirements>


<example_input>
markdown# About Our Firm
We serve clients from our offices across the country.

## Locations
- **New York Office**: 124 Main Street, New York, NY 10032
- **North Carolina Office**: 309 Elm Avenue, Raleigh, NC 27601

Contact us at info@lawfirm.com or call (555) 123-4567.

## Practice Areas
We handle cases nationwide from our main offices.
</example_input>

<expected_output>
json{
  "offices": [
    "124 Main Street New York, NY 10032",
    "309 Elm Avenue Raleigh, NC 27601"
  ]
}
</expected_output>

<edge_cases>
Multiple offices in the same city
International offices (adapt format as needed)
Offices listed across different website sections
Partial address information
Temporary or satellite offices mentioned
Suite numbers and floor information
Offices described in narrative text vs. structured lists
</edge_cases>

<validation_rules>
US state abbreviations must be valid (NY, CA, TX, etc.)
ZIP codes should be 5 digits or 5+4 format
No duplicate addresses in the output array
Street addresses should include numbers and street names
City names should be properly capitalized
CRITICAL: Deduplicate addresses that refer to the same location even if formatted differently
- Same street address with/without suite = duplicate
- Same address with state name vs abbreviation = duplicate
- Same address with/without building name = duplicate
- Only keep the most complete version of each unique address
</validation_rules>

<exclusions>
- Email addresses
- Phone numbers
- Fax numbers
- PO Box addresses
- Virtual office mentions
- Mailing addresses that are not physical locations
- Law school affiliations or bar admissions
- Law firm names within address strings
- Office descriptors without addresses (e.g., "Manhattan Office", "Main Office")
- Empty strings or null values
- Incomplete address fragments that cannot be reasonably completed
- JSON objects as string literals (parse them instead)
</exclusions>