// S2: same check, no fence (check-then-act).
module.exports = { name: 'S2_unfenced_check_then_act',
  async act({ registryUrl, sinkUrl }) { const r = await (await fetch(registryUrl + '/standing/nda')).json(); if (r.status !== 'active') return;
    await fetch(sinkUrl + '/effect', { method: 'POST', body: '{}' }); } };
