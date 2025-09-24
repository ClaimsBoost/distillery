# Extract Contact Information

<context>
{content}
</context>

Analyze the provided law firm website content and extract all contact information.

Look for:
- Primary phone numbers
- Toll-free numbers (800, 888, 877, 866, 855, 844, 833)
- Fax numbers
- Email addresses (general firm email)

Search in sections like:
- Contact Us pages
- Header/Footer areas
- About Us pages
- Home page prominently displayed numbers
- "Call Now" buttons
- Contact forms

Extract:
1. **Primary Phone**: Main office phone number
2. **Toll-Free Phone**: Any 1-800 or similar number
3. **Fax**: Fax number if available
4. **Email**: Primary contact email

Return the results in the following JSON format:
```json
{
  "primary_phone": "(859) 873-8033",
  "toll_free_phone": "1-800-555-1234",
  "fax": "(859) 873-8035",
  "email": "contact@lawfirm.com"
}
```

Example with minimal information:
```json
{
  "primary_phone": "(555) 123-4567",
  "toll_free_phone": null,
  "fax": null,
  "email": "info@example.com"
}
```

IMPORTANT:
- Format phone numbers consistently with parentheses for area code
- Include country code only if international
- Use null for missing information, not empty strings
- Don't include attorney direct lines unless they're the primary contact
- Extract the most prominent/general firm contact info
- If multiple offices, focus on main/headquarters contact info