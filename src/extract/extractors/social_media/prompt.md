# Extract Social Media Links

<context>
{content}
</context>

Analyze the provided website content and extract ALL social media and professional profile links.

Look for links to the following platforms:
- Facebook (facebook.com)
- Twitter/X (twitter.com, x.com)
- LinkedIn (linkedin.com)
- Instagram (instagram.com)
- YouTube (youtube.com, youtube.be)
- Justia (justia.com)
- Avvo (avvo.com)
- Martindale-Hubbell/Nolo (martindale.com, lawyers.com, nolo.com)

Extract the full URLs for each platform found. Look for these links in:
- Footer sections
- Header sections
- Contact pages
- About Us pages
- Social media icons/buttons
- Any embedded links in the content

Return the results in the following JSON format:
```json
{
  "social_media": {
    "facebook": "url or null",
    "twitter": "url or null",
    "linkedin": "url or null",
    "instagram": "url or null",
    "youtube": "url or null",
    "justia": "url or null",
    "avvo": "url or null",
    "martindale": "url or null"
  }
}
```

IMPORTANT:
- Return the FULL URL for each platform found (e.g., "https://www.facebook.com/lawfirmname")
- If a platform is not found, set the value to null
- Only extract official law firm profiles, not individual attorney profiles unless it's clearly the primary firm profile
- For Martindale-Hubbell, include links from martindale.com, lawyers.com, or nolo.com