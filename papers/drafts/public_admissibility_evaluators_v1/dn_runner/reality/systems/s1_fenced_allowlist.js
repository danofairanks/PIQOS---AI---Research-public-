// S1: reads status+revision, allow-list ('active'), acts carrying the revision as a fence.
module.exports = { name: 'S1_fenced_allowlist',
  async act({ registryUrl, sinkUrl }) { const r = await (await fetch(registryUrl + '/standing/nda')).json(); if (r.status !== 'active') return;
    await fetch(sinkUrl + '/effect', { method: 'POST', body: JSON.stringify({ fence: r.revision }) }); } };
