// A8: an adapter that never visits pre_decision or post_check.
module.exports = { name: 'A8_no_points', forms: ['listed_word', 'unlisted_wording', 'flag_only', 'registry_only', 'reworded', 'perturbed_word', 'translated', 'split_word', 'role_swap'],
  async run(ctx) { return ctx.effect(); } };
