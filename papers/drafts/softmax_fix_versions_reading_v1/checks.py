# Checks for arXiv 2610.31642 (v1 and v3), "A Fix for Softmax and Cross-Entropy".
# Part 1: closed forms (E1 arithmetic). Part 2: the paper's PRINTED JAX snippets (transcribed from the PDF text layer, comments dropped),
# run offline on CPU JAX (E1, labelled: this runs the printed code, not the authors' internal codebase) against the outputs the paper prints.
# Part 3: the v3 Errata claim (v1's printed code gives NaN gradients when all but one logit is -inf; v3's does not).
# Run: python3 -I checks.py   (needs jax, optax)
import math, numpy as np
print('#### PART 1: closed forms')
for name,bits in (('bf16 (8 bits)',8),('fp32 (24 bits)',24),('fp64 (53 bits)',53)):
    print(f'precision cliff {name}: m = bits*ln2 = {bits*math.log(2):.3f}   (paper: 5.5 / 16.6 / 36.7)')
for e in (1e-8,1e-12,1e-16): print(f'equilibrium log(1/eps) at eps={e:g}: {math.log(1/e):.2f}   (paper: 18.4 / 27.6 / 36.8)')
print('fp32 exponent limit ln(2^128) =',round(128*math.log(2),1),'(paper: ~88); fp32 min normal -> m =',round(126*math.log(2),1))
print('# mean-gain arithmetic in the v1 text "99-100%" vs v3 text ">=98.9%": the table row minima in Table 1 (v3 text layer) are 98.9 (bf16 Fixed CE, eps=1e-16) and 99.0 (fp32/fp64 Fixed CE, eps=1e-16): v1 wording under-stated the table; v3 matches it')
import jax, jax.numpy as jnp, optax
# ---- v3 printed code
def log_softmax_v3(z):
    i_max=jnp.argmax(z,axis=-1); z_max=jnp.take_along_axis(z,i_max[...,None],axis=-1)
    is_max=jax.nn.one_hot(i_max,z.shape[-1],dtype=bool)
    shifted=jnp.where(is_max,0.0,z-z_max)
    exp_others=jnp.where(is_max,0.0,jnp.exp(shifted))
    s=jnp.sum(exp_others,axis=-1,keepdims=True)
    return shifted-jnp.log1p(s)
softmax_v3=lambda z: jnp.exp(log_softmax_v3(z))
def cross_entropy_v3(z,t):
    z_t=jnp.take_along_axis(z,t[...,None],axis=-1)
    is_t=jax.nn.one_hot(t,z.shape[-1],dtype=bool)
    shifted=jnp.where(is_t,0.0,z-z_t)
    b=jnp.max(shifted,axis=-1,keepdims=True)
    s=jnp.sum(jnp.where(is_t,0.0,jnp.exp(shifted-b)),axis=-1)
    return b[...,0]+jnp.log1p(s+jnp.expm1(-b[...,0]))
def soft_target_cross_entropy_v3(z_S,z_T):
    log_q=log_softmax_v3(z_S); q,p=jnp.exp(log_q),softmax_v3(z_T)
    delta=z_S-z_T
    d=delta-jnp.sum(p*delta,axis=-1,keepdims=True)
    s=d-jnp.log1p(jnp.sum(p*jnp.expm1(d),axis=-1,keepdims=True))
    u=jnp.where(jnp.abs(s)<1,p*jnp.expm1(s),q-p)
    g=u-q*jnp.sum(u,axis=-1,keepdims=True)
    sg=jax.lax.stop_gradient
    loss=-jnp.sum(p*sg(log_q),axis=-1)
    return loss+jnp.sum(sg(g)*(z_S-sg(z_S)),axis=-1)
# ---- v1 printed code (hard-target part; v1's soft-target code lacked the |s|<1 branch)
def log_softmax_v1(z):
    i_max=jnp.argmax(z,axis=-1); z_max=jnp.take_along_axis(z,i_max[...,None],axis=-1)
    is_max=jax.nn.one_hot(i_max,z.shape[-1],dtype=bool)
    shifted=jnp.where(is_max,0.0,z-z_max)
    others=jnp.where(is_max,-jnp.inf,shifted)
    m=-jax.nn.logsumexp(others,axis=-1,keepdims=True)
    return shifted-jax.nn.softplus(-m)
def cross_entropy_v1(z,t):
    z_t=jnp.take_along_axis(z,t[...,None],axis=-1)
    is_t=jax.nn.one_hot(t,z.shape[-1],dtype=bool)
    others=jnp.where(is_t,-jnp.inf,z-z_t)
    m=-jax.nn.logsumexp(others,axis=-1)
    return jax.nn.softplus(-m)
np.set_printoptions(precision=4,linewidth=120)
print('\n#### PART 2: the paper\'s printed examples (fp32), v3 code; paper prints in comments')
z=jnp.array([9.0,-9.0,-9.0],dtype=jnp.float32); t=jnp.array(0)
std_ce=optax.softmax_cross_entropy_with_integer_labels
print('std log_softmax          :',np.array(jax.nn.log_softmax(z)),'   paper: [0, -18, -18]')
print('std grad softmax[0]      :',np.array(jax.grad(lambda z:jax.nn.softmax(z)[0])(z)),'   paper: [0, -1.523e-8, -1.523e-8]')
v,g=jax.value_and_grad(std_ce)(z,t); print('std value_and_grad CE    :',float(v),np.array(g),'   paper: 0.0 [0, 1.523e-8, 1.523e-8]')
print('v3 log_softmax           :',np.array(log_softmax_v3(z)),'   paper: [-3.046e-8, -18, -18]')
print('v3 grad softmax[0]       :',np.array(jax.grad(lambda z:softmax_v3(z)[0])(z)),'   paper: [3.046e-8, -1.523e-8, -1.523e-8]')
v,g=jax.value_and_grad(cross_entropy_v3)(z,t); print('v3 value_and_grad CE     :',float(v),np.array(g),'   paper: 3.046e-8 [-3.046e-8, 1.523e-8, 1.523e-8]')
print('v3 gradient sums to zero :',float(jnp.sum(g)))
zT=jnp.array([2.0,1.0,0.0],dtype=jnp.float32); zS=zT+jnp.array([-1e-7,1e-7,0.0],dtype=jnp.float32)
std_soft=lambda zS,zT:-jnp.sum(jax.nn.softmax(zT)*jax.nn.log_softmax(zS))
print('std soft-target grad     :',np.array(jax.grad(std_soft)(zS,zT)),'   paper: [-5.960e-8, 1.452e-8, -1.123e-9]')
print('v3 soft-target grad      :',np.array(jax.grad(soft_target_cross_entropy_v3)(zS,zT)),'   paper: [-4.596e-8, 4.144e-8, 4.513e-9]')
# exact float64 gradient q - p from the float32 inputs, via mpmath-free float64 numpy
zS64=np.array(zS,dtype=np.float64); zT64=np.array(zT,dtype=np.float64)
q=np.exp(zS64-zS64.max()); q/=q.sum(); p=np.exp(zT64-zT64.max()); p/=p.sum()
print('exact float64 q - p      :',q-p,'   paper: [-4.596e-8, 4.144e-8, 4.513e-9]')
print('\n#### PART 3: Errata claim (all but one logit effectively -inf, e.g. causal masking)')
zm=jnp.array([0.5,-jnp.inf,-jnp.inf],dtype=jnp.float32); tm=jnp.array(0)
for name,fn in (('v1 printed code',cross_entropy_v1),('v3 printed code',cross_entropy_v3)):
    v,g=jax.value_and_grad(fn)(zm,tm); print(f'{name}: loss {float(v)}, grad {np.array(g)}')
zl=jnp.array([0.5,-1e30,-1e30],dtype=jnp.float32)
for name,fn in (('v1 printed code',cross_entropy_v1),('v3 printed code',cross_entropy_v3)):
    v,g=jax.value_and_grad(fn)(zl,tm); print(f'{name} (logits -1e30): loss {float(v)}, grad {np.array(g)}')
for name,lsm in (('v1 log_softmax',log_softmax_v1),('v3 log_softmax',log_softmax_v3)):
    g=jax.grad(lambda z:lsm(z)[0])(zm); print(f'{name} grad wrt masked logits: {np.array(g)}')
print('\n#### PART 4: v3 hard-target loss vs the paper\'s own Eq. 6, in float64 (does the v3 snippet implement softplus(-m)?)')
jax.config.update('jax_enable_x64',True)
for m in (1.0,10.0,30.0):
    zz=jnp.array([m+math.log(2),0.0,0.0],dtype=jnp.float64); tt=jnp.array(0)   # margin m = z_t - log(sum exp(z_j)) = m
    print(f'margin {m:>4}: v3 CE {float(cross_entropy_v3(zz,tt)):.6e}  | softplus(-m) {float(jax.nn.softplus(-m)):.6e}  | v1 CE {float(cross_entropy_v1(zz,tt)):.6e}')
print('\n#### PART 5: v3 printed code in fp32 at large margins (does the target gradient survive past the fp32 cliff 16.6, toward the underflow near 87?)')
jax.config.update('jax_enable_x64',False)
for m in (20.0,40.0,60.0,80.0):
    zz=jnp.array([m+math.log(2),0.0,0.0],dtype=jnp.float32); tt=jnp.array(0)
    v,g=jax.value_and_grad(cross_entropy_v3)(zz,tt); sv,sg_=jax.value_and_grad(std_ce)(zz,tt)
    print(f'margin {m:>4}: v3 loss {float(v):.3e} target grad {float(g[0]):+.3e} sum {float(jnp.sum(g)):+.1e} | std loss {float(sv):.3e} target grad {float(sg_[0]):+.3e} | exact e^-m = {math.exp(-m):.3e}')
print('\n#### PART 6 (Addendum 1): the independent report\'s failing input, float64 [1.7976931348623157e308, -9.9792015476736e291] and [1e308, -1e308]')
jax.config.update('jax_enable_x64',True)
softmax_v1=lambda z: jnp.exp(log_softmax_v1(z))
for vec in ([1.7976931348623157e308,-9.9792015476736e291],[1e308,-1e308]):
    zz=jnp.array(vec,dtype=jnp.float64)
    for name,fn in (('standard jax.nn.softmax',jax.nn.softmax),('v1 printed softmax',softmax_v1),('v3 printed softmax',softmax_v3)):
        J=jax.jacobian(fn)(zz)
        print(f'{vec}: {name:24s} forward {np.array(fn(zz))} Jacobian {np.array(J).ravel()}')
