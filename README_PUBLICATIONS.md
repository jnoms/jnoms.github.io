# 📚 Simple Publication Management

## Quick Start

1. **Edit publications**: Open `publications.csv` in Excel/Google Sheets
2. **Update website**: Run `python3 update_publications.py`
3. **Deploy**: `git add . && git commit -m "Update publications" && git push`

## CSV Format

The `publications.csv` file has these columns:
- **Date**: YYYY-MM-DD format
- **Title**: Full publication title
- **Authors**: Author list with special markers:
  - `*` for co-first authors (displays with red asterisk)
  - `#` for co-corresponding authors (displays with blue #)
- **Journal**: Journal/venue name
- **DOI**: DOI number (without https://doi.org/ prefix)
- **Description**: Brief description for the excerpt

## Example Row

```csv
2025-08-21,Divergent viral phosphodiesterases for immune signaling evasion,"Doherty EE*, Nomburg J*, Adler BA, Lopez S, Hsieh K, et al.",bioRxiv,10.1101/2025.08.21.671373,Investigation of viral phosphodiesterases and their role in evading host immune signaling pathways.
```

## Features

✅ **Automatic formatting**: Your name gets bolded automatically  
✅ **Co-first authors**: Red asterisks for shared first authorship  
✅ **DOI links**: Publication titles link directly to papers  
✅ **Single category**: All publications appear under "Manuscripts"  
✅ **Chronological order**: Newest publications appear first  

## Files Generated

The script creates markdown files in `_publications/` directory:
- One `.md` file per publication
- Automatic Jekyll front matter
- Proper citation formatting
- DOI links

## Local Testing

To test locally before deploying:
```bash
docker compose up
# Visit http://localhost:4000/publications/
```

---
*This system replaces the old complex TSV/notebook workflow with a simple CSV + Python script approach.*
