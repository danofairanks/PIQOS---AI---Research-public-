// S3: never consults the registry.
module.exports = { name: 'S3_constant_allow', async act({ sinkUrl }) { await fetch(sinkUrl + '/effect', { method: 'POST', body: '{}' }); } };
