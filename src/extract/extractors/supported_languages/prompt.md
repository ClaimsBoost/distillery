<context>
{content}
</context>

<task>
Extract information about languages supported by this law firm in ANY way. Look for language support through website translations, staff language capabilities, phone/call center support, interpreter services, or any other way clients can communicate with the firm in different languages.
</task>

<requirements>
- Identify all languages the firm supports through ANY channel (website, phone, in-person, interpreters, etc.)
- Set boolean flags to true if the language is supported in ANY way
- Capture any additional languages not in our main list
- Default to English=true if no languages are mentioned (US law firms)
- Return valid JSON with all required fields
- If you see "Español" or links to "/es/", set supports_spanish to true
- If you see language switcher options, set those languages to true
</requirements>

<extraction_guidelines>
Look for these indicators of language support:

WEBSITE SUPPORT:
- Language switcher or selector (e.g., "English | Español")
- Links to translated versions (e.g., "/es/", "/cn/", "/ar/")
- "View in [language]" buttons
- Multilingual navigation menus
- Content explicitly in other languages

PHONE/CALL CENTER SUPPORT:
- "Call center representatives speak [language]"
- "Phone support available in [language]"
- "[Language] speaking representatives available"
- "Press 2 for Spanish" or similar phone menu mentions
- "24/7 [language] support"

STAFF/IN-PERSON SUPPORT:
- "We speak [language]"
- "Hablamos español" or similar phrases
- "[Language] speaking attorney/staff/paralegal"
- "Our team speaks [language]"
- Attorney bios mentioning languages spoken
- "Multilingual staff"
- "Bilingual services"

INTERPRETER/TRANSLATION SERVICES:
- "Interpreter services available"
- "Translation services provided"
- "We can arrange for interpreters"
- "Documents can be translated"
- "We work with certified translators"

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
  "supports_english": [boolean - true if English is supported in ANY way],
  "supports_spanish": [boolean - true if Spanish is supported in ANY way],
  "supports_chinese": [boolean - true if Chinese/Mandarin/Cantonese is supported in ANY way],
  "supports_arabic": [boolean - true if Arabic is supported in ANY way],
  "supports_french": [boolean - true if French is supported in ANY way],
  "supports_german": [boolean - true if German is supported in ANY way],
  "supports_hindi": [boolean - true if Hindi is supported in ANY way],
  "supports_portuguese": [boolean - true if Portuguese is supported in ANY way],
  "supports_russian": [boolean - true if Russian is supported in ANY way],
  "supports_tagalog": [boolean - true if Tagalog/Filipino is supported in ANY way],
  "supports_vietnamese": [boolean - true if Vietnamese is supported in ANY way],
  "other_languages": [array of strings or empty array - other languages not in main list]
}

CRITICAL:
- Set a language to true if it's supported in ANY way (website, phone, staff, interpreters, etc.)
- If no languages are mentioned at all, assume English=true (default for US firms)
- Don't assume languages based on attorney names alone
- Set other_languages to empty array [] if none found, not null
- Include dialects under their main language (e.g., Cantonese → Chinese)
</output_format>