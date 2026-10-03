// S5: deny-list of status words, with a fence.
const DENY = ['revoked', 'expired', 'denied', 'suspended'];
module.exports = { name: 'S5_fenced_denylist',
  async act({ registryUrl, sinkUrl }) { const r = await (await fetch(registryUrl + '/standing/nda')).json(); if (DENY.includes(r.status)) return;
    await fetch(sinkUrl + '/effect', { method: 'POST', body: JSON.stringify({ fence: r.revision }) }); } };
