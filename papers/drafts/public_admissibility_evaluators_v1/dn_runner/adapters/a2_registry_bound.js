// A2: registry-bound guard with compare-and-swap (B1 toy). The host supplies an identifier; the registry is the decisive input.
const { makeSystem } = require('../b1_registry_bound_guard.js');
const crypto = require('node:crypto'); const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
function build(mutations) {
  return {
    name: mutations.noCAS ? 'A3_registry_bound_no_CAS' : 'A2_registry_bound_CAS', forms: ['listed_word', 'unlisted_wording', 'flag_only', 'registry_only', 'reworded', 'perturbed_word', 'translated', 'split_word', 'role_swap'],
    async setup(ctx) { const s = makeSystem({ mutations }); s.registry.set('nda', true); ctx.world.onChange((w) => { if (!w.active) s.registry.set('nda', false); }); return s; },
    async run(ctx, form, s) {
      await ctx.point('pre_decision');
      const pid = crypto.randomUUID(); const receipt = s.evaluate({ standing_id: 'nda', action: 'slow_release', packet_id: pid }); // host text is ignored by design
      await ctx.point('post_check');
      const pending = s.execute({ receipt, packet_id: pid, action: 'slow_release' });
      await sleep(5); await ctx.point('in_flight'); await pending; ctx.report(s.effects.length);
    },
  };
}
module.exports = build({}); module.exports.build = build;
