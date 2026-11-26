from pathlib import Path

app = Path("site/app.js")
source = app.read_text()
anchor = "${duplicatePanel(l)}${paymentButtons(l,canEdit)}"
if source.count(anchor) != 1:
    raise ValueError("Expected one editable referral profile")
action = """${canEdit && TL.isOpen(l) ? `<div class="btnrow"><button type="button" class="btn ghost" data-act="reviewLostOutcome" data-id="${esc(l.id)}">Mark as lost</button></div>` : ''}"""
handler = "  if(a==='restoreDuplicate')"
if source.count(handler) != 1:
    raise ValueError("Expected one profile action dispatcher")
source = source.replace(anchor, action + anchor)
source = source.replace(handler, """  if(a==='reviewLostOutcome'){
    const lead=TL.Lead(id);
    if(lead && TL.isOpen(lead) && TL.canEditLead(lead)) return modal(lostForm(id));
    return;
  }
""" + handler)
app.write_text(source)

tests = Path("test/simple-referrals.test.mjs")
with tests.open("a") as out:
    out.write("""
test('open profiles offer a lost outcome and closed profiles leave the open list',()=>{
 const ctx=uiContext(), {V,UI,filtered}=ctx.simpleTest, tl=ctx.TL;
 const lead=tl.Lead('L_simple_old');
 vm.runInContext(read('followup-contacts.js'),ctx);
 const button='data-act="reviewLostOutcome"';
 assert.ok(V.lead(lead.id).includes(button));
 tl.closeLead(lead.id,'lost',tl.LOST_REASONS[0]);
 assert.equal(tl.isOpen(lead),false);
 assert.ok(!V.lead(lead.id).includes(button));
 for(const view of ['open','upcoming','moved','lost']){
  UI.moveView=view;
  assert.equal(filtered().some(item=>item.id===lead.id),view==='lost');
 }
});
""")
