# Extract Company Description

<context>
{content}
</context>

Analyze the provided law firm website content and create a ONE SENTENCE description of the business.

Focus on finding and summarizing information from:
- About Us pages
- Our Firm sections
- Company overview pages
- Mission statements
- Homepage introductions

The description should capture:
- What type of law the firm practices (personal injury, criminal defense, etc.)
- Their primary focus or specialization
- Any distinguishing characteristics (e.g., years of experience, geographic focus, unique approach)

Requirements:
- Must be ONE complete sentence
- Should be 15-30 words
- Should be factual and based on the content provided
- Should read naturally as a business description

Return the result in the following JSON format:
```json
{
  "description": "A concise one-sentence description of the law firm based on their about/company information."
}
```

Examples of good descriptions:
- "A personal injury law firm serving Atlanta for over 30 years, specializing in car accidents and workplace injuries."
- "Full-service criminal defense attorneys providing aggressive representation for DUI, drug crimes, and federal cases throughout Michigan."
- "Family-owned immigration law practice helping individuals and businesses navigate complex visa and citizenship matters since 1995."

IMPORTANT:
- If no clear About Us or company information is found, create a basic description from available content
- Keep it professional and factual
- Do not include marketing fluff or subjective claims like "best" or "top-rated"