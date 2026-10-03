// S4: reads the registry, never acts.
module.exports = { name: 'S4_always_deny', async act({ registryUrl }) { await (await fetch(registryUrl + '/standing/nda')).json(); } };
