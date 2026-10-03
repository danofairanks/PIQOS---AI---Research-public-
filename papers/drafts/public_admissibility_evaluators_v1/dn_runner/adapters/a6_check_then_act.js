// A6: reads the world once at decision time, then acts later (TOCTOU).
module.exports = { name: 'A6_check_then_act', forms: ['listed_word', 'unlisted_wording', 'flag_only', 'registry_only', 'reworded', 'perturbed_word', 'translated', 'split_word', 'role_swap'],
  async run(ctx) { await ctx.point('pre_decision'); const allow = ctx.world.active; await ctx.point('post_check'); if (allow) return ctx.effect(); } };
