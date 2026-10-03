// S6: caches its first reading for the lifetime of the (shared) process; no fence.
module.exports = { name: 'S6_caching_shared', shared: true, start: async () => ({ cached: null }),
  async act({ registryUrl, sinkUrl }, h) { if (!h.cached) h.cached = await (await fetch(registryUrl + '/standing/nda')).json(); if (h.cached.status !== 'active') return;
    await fetch(sinkUrl + '/effect', { method: 'POST', body: '{}' }); } };
