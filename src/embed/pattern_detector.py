"""
Pattern detector for chunk metadata enhancement
Detects specific patterns in text chunks to improve retrieval
"""

import re
from typing import Dict, Any


class PatternDetector:
    """Detects various patterns in text for metadata tagging"""
    
    # Only count COMPLETE street addresses with building/house numbers
    FULL_ADDRESS_PATTERNS = [
        # Complete street addresses: Must have number + street name + street type
        # Examples: "100 Main Street", "1201 Front Ave", "3070 N Main St."
        # Now more flexible with prefixes (including '[' for markdown links) and additional street types
        r'(?:^|\s|[\*\-•\[\(]\s*)(\d{1,5}\s+(?:[NSEW]\.?\s+)?[\w\s]+?(?:Street|St\.?|Avenue|Ave\.?|Boulevard|Blvd\.?|Drive|Dr\.?|Lane|Ln\.?|Road|Rd\.?|Way|Court|Ct\.?|Plaza|Pl\.?|Circle|Cir\.?|Parkway|Pkwy\.?|Highway|Hwy\.?|Square|Concourse|Center|Terrace|Trail|Park|Place)\b)',
        # Highway/Route addresses: "7608 GA-85", "1234 US-1", "5678 Route 66"
        r'\d{1,5}\s+(?:GA|US|State Route|Route|SR|Highway|Hwy|Interstate|I)-?\d+',
        # PO Box (counts as a complete mailing address)
        r'P\.?O\.?\s*Box\s+\d+',
        # Numbered streets like "147 North Avenue NE" or "100 Grace Hopper Ln"
        r'(?:^|\s|[\*\-•\[\(]\s*)(\d{1,5}\s+(?:North|South|East|West|N|S|E|W)?\s*[\w\s]+?(?:Avenue|Ave|Street|St|Road|Rd|Lane|Ln|Drive|Dr|Boulevard|Blvd)\b)',
    ]
    
    # Email patterns
    EMAIL_PATTERNS = [
        r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    ]
    
    # Phone patterns - various formats
    PHONE_PATTERNS = [
        r'\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}',  # (123) 456-7890 or 123-456-7890
        r'\d{3}\.\d{3}\.\d{4}',  # 123.456.7890
        r'\+1[\s.-]?\d{3}[\s.-]?\d{3}[\s.-]?\d{4}',  # +1 123-456-7890
        r'1-\d{3}-\d{3}-\d{4}',  # 1-123-456-7890
    ]

    # Money/settlement amount patterns
    MONEY_PATTERNS = [
        # Dollar amounts with various formats: $1,000,000, $1M, $1.5 million
        r'\$[\d,]+(?:\.\d+)?(?:\s*(?:million|Million|MILLION|mil|MIL|billion|Billion|BILLION|bil|BIL|thousand|Thousand|THOUSAND|k|K|M|B))?',
        # Written numbers with dollar context: "five million dollars", "100 thousand dollars"
        r'\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion)(?:\s+(?:hundred|thousand|million|billion))?\s+dollars?\b',
        # Settlements/verdicts/awards with numbers: "1.5 million settlement", "500k verdict"
        r'\b\d+(?:,\d{3})*(?:\.\d+)?\s*(?:million|Million|mil|thousand|Thousand|k|K|M)\s*(?:in\s+)?(?:settlement|verdict|award|compensation|recovery|damages)',
        # Plain large numbers that could be money (10,000+ or 100000+)
        r'\b\d{1,3}(?:,\d{3}){1,}\b|\b\d{5,}\b',
        # Written form: "twenty thousand", "five hundred thousand", "1.2 million"
        r'\b(?:one|two|three|four|five|six|seven|eight|nine|ten|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion)(?:\s+(?:hundred|thousand|million|billion))+\b',
    ]

    
    @classmethod
    def detect_patterns(cls, text: str) -> Dict[str, Any]:
        """
        Detect various patterns in text chunk
        
        Args:
            text: Text chunk to analyze
            
        Returns:
            Dictionary with boolean flags and counts for each pattern type
        """
        metadata = {}
        
        # Check for COMPLETE addresses only (with street numbers)
        address_matches = []
        for pattern in cls.FULL_ADDRESS_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            # Handle both captured groups and plain matches
            for match in matches:
                if isinstance(match, tuple):
                    # If it's a tuple (from capture groups), take the captured part
                    address_matches.extend([m for m in match if m])
                else:
                    address_matches.append(match)
        
        # Remove duplicates and clean up matches
        unique_addresses = set(match.strip() for match in address_matches if match and match.strip())
        
        metadata['contains_addresses'] = len(unique_addresses) > 0
        metadata['address_count'] = len(unique_addresses)  # Count of unique full addresses
        
        # Check for emails
        email_matches = []
        for pattern in cls.EMAIL_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            email_matches.extend(matches)
        
        metadata['contains_emails'] = len(email_matches) > 0
        metadata['email_count'] = len(set(email_matches))
        
        # Check for phone numbers
        phone_matches = []
        for pattern in cls.PHONE_PATTERNS:
            matches = re.findall(pattern, text)
            phone_matches.extend(matches)
        
        # Filter out false positives (like dates that look like phones)
        phone_matches = [p for p in phone_matches if not re.search(r'^(19|20)\d{2}', p)]  # Avoid years
        
        metadata['contains_phone_numbers'] = len(phone_matches) > 0
        metadata['phone_count'] = len(set(phone_matches))

        # Combined contact count (emails + phone numbers)
        total_contact_count = metadata['email_count'] + metadata['phone_count']
        metadata['contains_contact'] = total_contact_count > 0
        metadata['contact_count'] = total_contact_count

        # Check for money/settlement amounts
        money_matches = []
        for pattern in cls.MONEY_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            money_matches.extend(matches)

        metadata['contains_money'] = len(money_matches) > 0
        metadata['money_count'] = len(set(money_matches))

        # Add additional useful flags for law firm context
        metadata['contains_attorney_names'] = bool(
            re.search(r'\b(?:attorney|lawyer|esq\.?|esquire|partner|associate|counsel|jr\.?|sr\.?|iii|ii)\b',
                     text, re.IGNORECASE)
        )
        
        metadata['contains_hours'] = bool(
            re.search(r'\b(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday|mon|tue|wed|thu|fri|sat|sun)\b.*(?:am|pm|\d{1,2}:\d{2})', 
                     text, re.IGNORECASE)
        )
        
        metadata['contains_practice_areas'] = bool(
            re.search(r'\b(?:personal injury|criminal defense|family law|divorce|bankruptcy|immigration|real estate|corporate|tax|estate planning|workers compensation|medical malpractice|employment law|intellectual property)\b',
                     text, re.IGNORECASE)
        )
        
        # Character count for context
        metadata['chunk_length'] = len(text)
        
        return metadata