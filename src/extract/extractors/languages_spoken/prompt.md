<context>
{content}
</context>

<task>
Extract information about languages supported by this website. Look for language options, translated versions of the site, multilingual services, or mentions of staff who speak specific languages.
</task>

<requirements>
- Identify all languages the website supports (through language switchers, alternate versions, or staff capabilities)
- Set boolean flags for each of the tracked languages
- Capture any additional languages not in our main list
- Default to English=true if no languages are mentioned (US law firms)
- Return valid JSON with all required fields
- If you see "Español" or links to "/es/", set speaks_spanish to true
- If you see language switcher options, set those languages to true
</requirements>

<extraction_guidelines>
Look for these indicators of language capabilities:
- "We speak [language]"
- "Hablamos español" or similar phrases in other languages
- "[Language] speaking attorney/staff"
- "Services available in [language]"
- "Multilingual staff"
- "Bilingual services"
- Staff member names followed by languages they speak
- Language flags or symbols near text
- "Interpreter services available"
- "Translation services"
- Attorney bios mentioning languages spoken
- Language switcher or selector (e.g., "English | Español")
- Links to translated versions of the site (e.g., "/es/" for Spanish)
- "Switch to [language]" buttons or links
- Language options in navigation menus

Language mappings to extract:
- English: English
- Spanish: Spanish, Español, Castellano
- Chinese: Chinese, Mandarin, Cantonese, 中文, 普通话, 广东话
- Arabic: Arabic, العربية
- French: French, Français
- German: German, Deutsch
- Hindi: Hindi, हिन्दी
- Portuguese: Portuguese, Português, Brazilian Portuguese
- Russian: Russian, Русский
- Tagalog: Tagalog, Filipino, Pilipino
- Vietnamese: Vietnamese, Tiếng Việt

Also capture other languages mentioned that aren't in this list.
</extraction_guidelines>

<output_format>
Return a JSON object with this exact structure:
{
  "speaks_english": [boolean - true if English is spoken],
  "speaks_spanish": [boolean - true if Spanish is spoken],
  "speaks_chinese": [boolean - true if Chinese/Mandarin/Cantonese is spoken],
  "speaks_arabic": [boolean - true if Arabic is spoken],
  "speaks_french": [boolean - true if French is spoken],
  "speaks_german": [boolean - true if German is spoken],
  "speaks_hindi": [boolean - true if Hindi is spoken],
  "speaks_portuguese": [boolean - true if Portuguese is spoken],
  "speaks_russian": [boolean - true if Russian is spoken],
  "speaks_tagalog": [boolean - true if Tagalog/Filipino is spoken],
  "speaks_vietnamese": [boolean - true if Vietnamese is spoken],
  "other_languages": [array of strings or null - other languages not in main list]
}

CRITICAL:
- Only set a language to true if it's explicitly mentioned
- If no languages are mentioned at all, assume English=true (default for US firms)
- Don't assume languages based on attorney names alone
- Set other_languages to empty array [] if none found, not null
- Include dialects under their main language (e.g., Cantonese → Chinese)
</output_format>