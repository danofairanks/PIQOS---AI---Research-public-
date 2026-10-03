// A5: refuses at the effect boundary every time (no utility). Visits both points, then declines.
module.exports = { name: 'A5_always_deny', forms: ['listed_word', 'unlisted_wording', 'flag_only', 'registry_only', 'reworded', 'perturbed_word', 'translated', 'split_word', 'role_swap'],
  async run(ctx) { await ctx.point('pre_decision'); await ctx.point('post_check'); /* refuse */ } };
