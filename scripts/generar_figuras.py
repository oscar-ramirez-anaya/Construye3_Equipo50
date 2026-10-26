"""Genera las figuras del README a partir del conjunto común. Uso: python3 scripts/generar_figuras.py datos figuras"""
import sys, pandas as pd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
R=sys.argv[1]; OUT=sys.argv[2]
B,O,T1,T2,G='#2a78d6','#eb6834','#0b0b0b','#52514e','#e4e3df'
plt.rcParams.update({'font.family':'Arial','font.size':10,'axes.edgecolor':G,'axes.labelcolor':T2,'xtick.color':T2,'ytick.color':T2,'figure.facecolor':'#fcfcfb','axes.facecolor':'#fcfcfb','savefig.facecolor':'#fcfcfb'})
def limpiar(ax):
    for s in ('top','right'): ax.spines[s].set_visible(False)
inv=pd.read_csv(R+'/inventarios.csv',parse_dates=['fecha']); hoy=inv.fecha.max()
w=inv[inv.fecha>hoy-pd.Timedelta(days=14)]
# 1 embudo
et=['Inventarios (13 semanas)','Ventana de 14 días','Filas con 0 unidades','Combinaciones con\n≥ 2 días en cero','Caso enviado al modelo']
v=[len(inv),len(w),int((w.unidades_disponibles==0).sum()),2528,1]
fig,ax=plt.subplots(figsize=(8,3.4)); y=range(len(v))[::-1]
ax.barh(list(y),v,color=B,height=0.55); ax.set_xscale('log'); ax.set_yticks(list(y)); ax.set_yticklabels(et,color=T1)
for yi,vi in zip(y,v): ax.text(vi*1.15,yi,f'{vi:,}',va='center',color=T1)
ax.set_xlim(0.5,3e6); ax.set_xlabel('Filas o combinaciones (escala logarítmica)'); limpiar(ax); ax.grid(axis='x',color=G,lw=0.6); ax.set_axisbelow(True)
ax.set_title('Selección y compresión: de 475,800 filas a un caso',loc='left',color=T1,fontsize=11.5,fontweight='bold')
fig.tight_layout(); fig.savefig(OUT+'/01_seleccion_compresion.png',dpi=160); plt.close(fig)
# 2 vigencia
f=['ventas (7 d)','inventarios (1 d)','precios_competencia (14 d)']; vig=[50371,4200,536]; tot=[50371+599192,4200+471600,536+3060]
pct=[a/b*100 for a,b in zip(vig,tot)]
fig,ax=plt.subplots(figsize=(8,2.8)); y=[2,1,0]
ax.barh(y,pct,color=B,height=0.5); ax.set_yticks(y); ax.set_yticklabels(f,color=T1); ax.set_xlim(0,20)
for yi,p,a,b in zip(y,pct,vig,tot): ax.text(p+0.3,yi,f'{p:.1f} %  ({a:,} de {b:,})',va='center',color=T1)
ax.set_xlabel('Registros dentro de la ventana de vigencia (%)'); limpiar(ax); ax.grid(axis='x',color=G,lw=0.6); ax.set_axisbelow(True)
ax.set_title('Vigencia por fuente al corte (Registro 1, pasos 2 a 4)',loc='left',color=T1,fontsize=11.5,fontweight='bold')
fig.tight_layout(); fig.savefig(OUT+'/02_vigencia_por_fuente.png',dpi=160); plt.close(fig)
# 3 empate
t=w[(w.producto_id=='P060')&(w.tienda_id.isin(['T0046','T0053']))]
fig,ax=plt.subplots(figsize=(8,3.4))
for tid,c in (('T0046',B),('T0053',O)):
    s=t[t.tienda_id==tid].sort_values('fecha'); ax.plot(s.fecha,s.unidades_disponibles,color=c,lw=2,marker='o',ms=5,label=tid)
    ax.text(s.fecha.iloc[-1]+pd.Timedelta(hours=10),s.unidades_disponibles.iloc[-1],f'{tid}: {int(s.unidades_disponibles.iloc[-1])} u. al corte',va='center',color=T1,fontsize=9)
ax.set_xlim(t.fecha.min()-pd.Timedelta(hours=12),hoy+pd.Timedelta(days=3.2))
ax.axvline(hoy,color=T2,lw=0.8,ls='--'); ax.text(hoy,ax.get_ylim()[1]*0.97,' corte 2026-08-30',color=T2,fontsize=8.5,va='top')
ax.set_ylabel('Unidades disponibles (P060)'); limpiar(ax); ax.grid(axis='y',color=G,lw=0.6); ax.set_axisbelow(True)
ax.legend(frameon=False,loc='lower right',bbox_to_anchor=(1,1.0),ncol=2,fontsize=9)
import matplotlib.dates as md; ax.set_xticks(pd.date_range(t.fecha.min(),hoy,freq='2D')); ax.xaxis.set_major_formatter(md.DateFormatter('%d/%m'))
ax.set_title('Mismo costo estimado (2,719), distinto estado al corte',loc='left',color=T1,fontsize=11.5,fontweight='bold')
fig.tight_layout(); fig.savefig(OUT+'/03_empate_T0046_T0053.png',dpi=160); plt.close(fig)
print('ok')
