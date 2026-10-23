#include <stdio.h>
#include <stdint.h>
#include <string.h>
#define N 1024
#define W 16
typedef uint64_t u64;
static u64 adj[N][W];
static unsigned long long cnt[7];
static void rec(int depth,u64*cand,int maxk){ // cand: common nbrs with index > last
  for(int w=0;w<W;w++){u64 x=cand[w];while(x){int b=__builtin_ctzll(x);x&=x-1;int v=w*64+b;
    cnt[depth+1]++;
    if(depth+1<maxk){u64 nc[W];int any=0;for(int t=0;t<W;t++){nc[t]=cand[t]&adj[v][t];}
      // keep only > v
      for(int t=0;t<w;t++)nc[t]=0; nc[w]&= (b==63)?0:(~0ULL<<(b+1));
      rec(depth+1,nc,maxk);} }}
}
int main(int argc,char**argv){
  int comp=argc>1; char line[N+4]; FILE*f=fopen("adj.txt","r");
  for(int i=0;i<N;i++){fgets(line,sizeof line,f);for(int j=0;j<N;j++){int a=line[j]=='1'; if(comp)a=(i!=j)&&!a; if(a)adj[i][j/64]|=1ULL<<(j%64);}}
  u64 all[W];for(int i=0;i<W;i++)all[i]=~0ULL;
  rec(0,all,5);
  for(int k=1;k<=5;k++)printf("%llu\n",cnt[k]);
}
