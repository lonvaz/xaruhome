# XARU HOME — stock scouting brief

You are selecting REAL STOCK PHOTOGRAPHS for a demonstrative real-estate platform.

## Tool
`mcp__Magnific__stock_search` (load via ToolSearch first:
`select:mcp__Magnific__stock_search`).
Always pass: content_type="photo", ai_generated="excluded", orientation="landscape".
NOTE: `per_page` is IGNORED — every call returns 50 items. Budget your calls.

## What makes a good pick
- Real architecture / real landscape, photographed. Aerials and exteriors are ideal.
- Search by REAL PLACE NAME ("Santorini caldera hotel", "Mendoza vineyard Andes").
  Generic luxury words ("luxury villa", "modern mansion") return junk.
- Must plausibly depict the slot's asset type in the slot's country/city.

## REJECT
- Anything whose title contains: "Generative AI", "AI generated", "AIG", "3D render",
  "illustration", "rendering", "digital art".
- People as the subject (models by pools, tourists posing, portraits, hands, couples).
  Incidental distant figures are fine.
- Interiors of hotel rooms, close-ups of objects, food, beds, towels, spa stones.
- Stock-cliché business imagery (handshakes, charts, suited people).
- Anything that reads as a template/mockup.

## Output format — THIS IS THE ONLY THING YOU RETURN
One line per pick, pipe-separated, no prose, no markdown, no headers:

slot_id|stock_id|preview_url|short honest description of what the photo shows

Return exactly THREE candidates per slot, best first. If a slot is genuinely hard,
still return three — the closest you found — and mark the line with a trailing `|WEAK`.

Do NOT return anything else. No preamble, no summary, no explanation.
