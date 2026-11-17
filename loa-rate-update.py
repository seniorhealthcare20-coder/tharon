from pathlib import Path
import json
r=Path(__file__).resolve().parent
changes=json.loads('{"site/county-roadmap.js": [["LOA \\u2014 short-term hospital contract", "LOA"]], "site/app.js": [["f.querySelector(\'[data-tier-field]\').hidden=priv;", "f.querySelector(\'[data-tier-field]\').hidden=priv||x.payer===\'LOA\';f.querySelector(\'[data-loa-rate-field]\').hidden=x.payer!==\'LOA\';"], ["<label data-tier-field ${priv?\'hidden\':\'\'}>", "<label data-tier-field ${priv||x.payer===\'LOA\'?\'hidden\':\'\'}>"], ["</select></label><label class=\\"span2\\" data-budget-field", "</select></label><label data-loa-rate-field ${x.payer===\'LOA\'?\'\':\'hidden\'}>Rate amount ($)<input class=\\"input\\" name=\\"loaRate\\" type=\\"number\\" min=\\"0\\" step=\\"0.01\\" value=\\"${esc(x.loaRate??\'\')}\\"></label><label class=\\"span2\\" data-budget-field"], ["if(d.payer===\'Private pay\')d.budget=", "if(d.payer===\'LOA\')d.loaRate=v(\'loaRate\')===\'\'?null:Number(v(\'loaRate\'));else if(d.payer===\'Private pay\')d.budget="]], "server/engine.mjs": [["\'payer\',\'budget\',\'moveIn\'", "\'payer\',\'budget\',\'loaRate\',\'moveIn\'"], ["  if(d.tier!=null", "  if(d.loaRate!=null&&(!Number.isFinite(d.loaRate)||d.loaRate<0))fail(422,\'Enter a valid rate amount.\');\\n  if(d.tier!=null"]], "site/api.js": [["monthly_budget:l.budget,", "monthly_budget:l.budget,loa_rate_amount:l.loaRate??null,"], ["monthly_budget:\'budget\',", "monthly_budget:\'budget\',loa_rate_amount:\'loaRate\',"]]}')
for name,edits in changes.items():
 p=r/name;s=p.read_text()
 for old,new in edits:
  if s.count(old)!=1: raise SystemExit(f"Unexpected LOA rate source in {name}; no deployment patch applied")
  s=s.replace(old,new,1)
 p.write_text(s)
