// A7: reads the world at effect start in the same synchronous step as the effect begins.
module.exports = { name: 'A7_atomic_check', forms: ['listed_word', 'unlisted_wording', 'flag_only', 'registry_only', 'reworded', 'perturbed_word', 'translated', 'split_word', 'role_swap'],
  async run(ctx) { await ctx.point('pre_decision'); await ctx.point('post_check'); if (ctx.world.active) return ctx.effect(); } };
