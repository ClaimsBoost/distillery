<context>
{content}
</context>

<task>
Analyze the provided content and extract settlement/verdict amounts. You must distinguish between:
1. FIRM-WIDE TOTAL: The cumulative amount the entire firm has recovered across ALL cases over time
2. INDIVIDUAL CASES: Specific case results with their individual settlement/verdict amounts

IMPORTANT: Only extract what is explicitly stated in the context above. Do not use any example data.
</task>

<firm_total_indicators>
A firm-wide total will have language indicating accumulation over time or across many cases:
- "We have recovered [amount] for our clients"
- "Our firm has secured [amount] in settlements and verdicts"
- "[amount] recovered since [year/founding]"
- "Total recoveries: [amount]"
- "Track record of [amount]"

If you see "over", "more than", "in excess of" before the amount, set is_minimum to true.
If no firm-wide total is mentioned, set all firm_total fields to null/false.
</firm_total_indicators>

<individual_case_indicators>
Individual cases are specific incidents with their own amounts:
- Look for case descriptions (accident types, injuries) followed by amounts
- "TOTAL RECOVERED: $[amount]" under a specific case description
- "Settlement: $[amount]" for a specific incident
- "Verdict: $[amount]" for a specific case
- Insurance company names (State Farm, Progressive, etc.) near amounts often indicate individual cases

NOT individual cases (do not extract these):
- General statistics like "average settlements range from X to Y"
- Industry averages like "slip and fall cases typically settle for X"
- General statements like "cases can be worth X to Y"
- Educational content about typical case values

Extract ALL individual cases you find. For each case, include:
- amount: The numeric value (convert dollar amounts to numbers)
- display_text: How it appears in the text (preserve original formatting)
- case_type: Type of incident if mentioned (e.g., "Car Accident", "Slip and Fall")
- insurance_company: Insurance company name if mentioned
</individual_case_indicators>

<output_format>
Return a JSON object with this exact structure:
{
  "firm_total": {
    "total_amount": [number or null - firm's cumulative total in dollars],
    "display_text": [string or null - how the firm total appears in text],
    "is_minimum": [boolean - true if preceded by "over", "more than", etc.]
  },
  "individual_cases": [
    {
      "amount": [number - case amount in dollars],
      "display_text": [string - how amount appears in text],
      "case_type": [string or null - type of case],
      "insurance_company": [string or null - insurance company name]
    }
  ]
}

CRITICAL:
- Do NOT confuse individual case amounts with firm totals
- Do NOT add up individual cases to create a firm total
- Only report amounts that are explicitly stated in the context
- Individual cases should be in an array, even if empty []
- If NO individual cases are found, return an EMPTY array [] for "individual_cases"
- Do NOT create placeholder entries with zero/empty values
- Only include actual cases with real settlement amounts
</output_format>