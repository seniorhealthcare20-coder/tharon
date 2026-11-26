from pathlib import Path

def replace(path, old, new):
    file = Path(path)
    source = file.read_text()
    if source.count(old) != 1:
        raise ValueError(f"Unexpected source in {path}")
    file.write_text(source.replace(old, new))

replace("site/api.js", "if(!l||!isOpen(l))return false;const a=leadAging(l);", """if(!l||!isOpen(l))return false;
 if(openDays!=='all'){
  const moveStatus=referralSummary(l)?.moveStatus;
  if(moveStatus==='moved'||(moveStatus==='scheduled'&&window.TLReferral.date(l.moveIn)))return false;
 }
 const a=leadAging(l);""")
replace("site/app.js", "Days since the referral was added.", "Open referrals without a scheduled move-in, counted from the date added.")
with Path("test/lead-aging.test.mjs").open("a") as file:
    file.write("""
test('open age excludes future and overdue scheduled arrivals and closed referrals',()=>{
 const tl=engine(fixture(),'u0'),lead=tl.Lead('L_aging_old');
 setDates(tl,lead,31,null);
 for(const days of [7,14,30]){
  lead.stage='new';lead.moveIn=null;
  assert.equal(tl.matchesLeadAging(lead,{openDays:days}),true);
  for(const offset of [-2,0,2]){
   lead.moveIn=tl.addDays(offset);
   assert.equal(tl.matchesLeadAging(lead,{openDays:days}),false);
  }
  lead.moveIn=null;
  for(const stage of ['movein','lost']){
   lead.stage=stage;
   assert.equal(tl.matchesLeadAging(lead,{openDays:days}),false);
  }
 }
});
""")
replace("test/simple-referrals.test.mjs",
        "UI.openDays='14';assert.deepEqual(Array.from(filtered(),l=>l.id).sort(),[old.id,other.id].sort());UI.simpleApproval='approved';assert.deepEqual(Array.from(filtered(),l=>l.id),[old.id]);",
        "UI.openDays='14';assert.deepEqual(Array.from(filtered(),l=>l.id),[other.id]);UI.simpleApproval='approved';assert.deepEqual(Array.from(filtered(),l=>l.id),[]);")
