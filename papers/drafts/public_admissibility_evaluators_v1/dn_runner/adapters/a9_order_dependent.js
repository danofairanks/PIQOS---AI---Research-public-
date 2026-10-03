// A9: shared state; caches the first decision it ever made for each form.
module.exports = { name: 'A9_order_dependent', shared: true, sharedState: async () => ({ cache: new Map() }),
  forms: ['listed_word', 'unlisted_wording', 'flag_only', 'registry_only', 'reworded', 'perturbed_word', 'translated', 'split_word', 'role_swap'],
  async run(ctx, form, st) { await ctx.point('pre_decision'); if (!st.cache.has(form)) st.cache.set(form, ctx.world.active); await ctx.point('post_check'); if (st.cache.get(form)) return ctx.effect(); } };
