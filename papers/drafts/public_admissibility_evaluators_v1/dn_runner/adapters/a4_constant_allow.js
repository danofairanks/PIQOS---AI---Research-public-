// A4: constant-ALLOW system (decision ignores everything).
module.exports = { name: 'A4_constant_allow', forms: ['listed_word', 'unlisted_wording', 'flag_only', 'registry_only', 'reworded', 'perturbed_word', 'translated', 'split_word', 'role_swap'],
  async run(ctx) { await ctx.point('pre_decision'); await ctx.point('post_check'); return ctx.effect(); } };
