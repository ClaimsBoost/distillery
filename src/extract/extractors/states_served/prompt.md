# Extract States Served

<context>
{content}
</context>

Analyze the provided law firm website content and extract information about which states the law firm serves or is licensed to practice in.

Look for:
- Explicit mentions of states served
- Attorney bar admissions by state
- Office locations (which imply service in those states)
- Service area descriptions
- Jurisdictional information
- "We serve clients in..." statements
- "Licensed to practice in..." mentions
- Nationwide practice indicators
- Multi-state practice mentions
- Regional coverage descriptions

Search in sections like:
- About Us / Our Firm
- Service Areas / Coverage
- Attorney profiles (for bar admissions)
- Contact / Location pages
- Practice area descriptions
- Footer information

Extract:
1. **States**: List of US states where the firm practices (use 2-letter abbreviations)

Return the results in the following JSON format:
```json
{
  "states": ["KY", "OH", "IN"]
}
```

Example with single state:
```json
{
  "states": ["CA"]
}
```

Example with many states:
```json
{
  "states": ["NY", "NJ", "CT", "PA", "MA"]
}
```

IMPORTANT:
- Use standard 2-letter state abbreviations (e.g., CA, NY, TX)
- If they mention serving "surrounding states" or "tri-state area", try to identify specific states
- If the firm practices nationwide, include all states or the main states mentioned
- Include states where they have offices
- Include states where attorneys are licensed/admitted to practice
- If no clear information is found, return empty arrays and false values
- Don't assume states based solely on office locations unless explicitly stated they serve those states