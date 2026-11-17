from pathlib import Path
import json
r=Path(__file__).resolve().parent
changes=json.loads('{"site/county-roadmap.js": [["[\'alw\',\'ALW\',\'ALW waiver\'],[\'private\'", "[\'alw\',\'ALW\',\'ALW waiver\'],[\'loa\',\'LOA \\u2014 short-term hospital contract\',\'LOA\'],[\'private\'"]], "site/api.js": [["l&&l.payer===\'CalAIM Community Supports\'?\'calaim\':null;", "l&&l.payer===\'CalAIM Community Supports\'?\'calaim\':l&&l.payer===\'LOA\'?\'loa\':null;"], ["p===\'calaim\'?\'CalAIM\':\'\';", "p===\'calaim\'?\'CalAIM\':p===\'loa\'?\'LOA\':\'\';"]], "site/referral-progress.js": [["if(l.payer===\'Private pay\')return", "if(l.payer===\'LOA\')return [[\'contract\',\'Hospital contract approval\'],[\'agreement\',\'Signed LOA contract\']];if(l.payer===\'Private pay\')return"], ["const provider=(l.cca||flow?.config.partner||\'\').trim()", "const provider=(l.cca||flow?.config.partner||(l.payer===\'LOA\'?\'the hospital\':\'\')).trim()"], ["const document=privatePay?\'signed agreement\':", "const document=l.payer===\'LOA\'?\'signed LOA contract\':privatePay?\'signed agreement\':"]], "site/capture.js": [["const PAYER=[\'Private pay\',\'ALW waiver\',", "const PAYER=[\'Private pay\',\'ALW waiver\',\'LOA\',"], ["if(/cal[- ]?aim|community supports?|kalam/.test(s))", "if(/\\\\b(?:hospital\\\\s+loa|loa\\\\s+(?:hospital|contract)|short[- ]term\\\\s+(?:hospital\\\\s+)?contract)\\\\b/.test(s)||/^loa$/.test(s.trim())) return \'LOA\';\\n  if(/cal[- ]?aim|community supports?|kalam/.test(s))"]]}')
for name,edits in changes.items():
 p=r/name;s=p.read_text()
 for old,new in edits:
  if s.count(old)!=1: raise SystemExit(f"Unexpected LOA source in {name}; no deployment patch applied")
  s=s.replace(old,new,1)
 p.write_text(s)
