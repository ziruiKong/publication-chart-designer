"""Eight editorial scientific plates; all data are synthetic demonstrations.

Install requirements-gallery.txt, then run from any directory. Each plate
includes computed analysis, a methods strip, and PNG/PDF/SVG exports.
"""
from pathlib import Path
import argparse
import json
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.colors import Normalize
import numpy as np
from scipy import stats
from scipy.cluster.hierarchy import linkage, leaves_list, dendrogram
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve, average_precision_score
from figure_kit import use_publication_style, palette_colors, colormap, refine_axes, save_publication_figure

ROOT = Path(__file__).resolve().parents[1]
INK = "#172B3A"
GRAY = "#94A1AC"
SEED = 20261117


def plate(number, family, title, descriptor, methods, projection=False):
    fig = plt.figure(figsize=(12.8, 6.4))
    fig.text(.065, .955, f"RESEARCH ATLAS   /   {number:02d}   /   {family.upper()}",
             fontsize=9, color="#5F8878", fontweight="medium")
    fig.text(.065, .89, title, fontsize=21, fontweight="semibold", color=INK)
    fig.text(.065, .84, descriptor, fontsize=10, color="#465966")
    fig.add_artist(Line2D([.065, .95], [.805, .805], transform=fig.transFigure,
                         color="#C7D0D7", lw=.7))
    grid = fig.add_gridspec(1, 2, left=.085, right=.94, bottom=.23, top=.72,
                           width_ratios=[1.25, 1], wspace=.36)
    axes = [fig.add_subplot(grid[0], projection="3d" if projection else None),
            fig.add_subplot(grid[1])]
    fig.add_artist(Line2D([.065, .95], [.14, .14], transform=fig.transFigure,
                         color="#C7D0D7", lw=.7))
    fig.text(.065, .105, "METHOD / " + "\n".join(textwrap.wrap(methods, 151)),
             fontsize=8, color="#465966", va="top", linespacing=1.5)
    fig.text(.065, .025, "SYNTHETIC DESIGN DATA  /  NOT RESEARCH FINDINGS", fontsize=8,
             fontweight="medium", color="#64748B")
    return fig, axes


def heading(ax, letter, title):
    ax.set_title(f"{letter}   {title}", fontsize=11, fontweight="semibold", pad=7)


def ai(rng, colors):
    fig, (ax, bx) = plate(1, "Artificial intelligence", "Learning dynamics, made comparable",
        "4 architectures  /  6 independent synthetic seeds  /  80 checkpoints",
        "Lines: seed means; bands: ±1 SD across six seeds. Attention is row-normalized synthetic structure, not a causal explanation.")
    epochs = np.arange(80)
    for i, (name, color) in enumerate(zip(["Baseline", "ConvNet", "Transformer", "Hybrid"], colors)):
        runs = np.array([.40 + (.36 + .04*i)*(1-np.exp(-epochs/(17+4*i))) +
                         rng.normal(0,.014,80) + rng.normal(0,.012) for _ in range(6)])
        mean, sd = runs.mean(0), runs.std(0, ddof=1)
        ax.plot(epochs, mean, color=color, label=name, lw=1.9)
        ax.fill_between(epochs, mean-sd, mean+sd, color=color, alpha=.18, linewidth=0)
    ax.set(xlabel="Checkpoint", ylabel="Validation accuracy", ylim=(.36,.96))
    ax.legend(ncols=2, loc="lower right", fontsize=9)
    refine_axes(ax); heading(ax,"a","Training stability")
    matrix = rng.gamma(1.2,1,(16,16)) + 6*np.exp(-abs(np.subtract.outer(np.arange(16),np.arange(16)))/2)
    matrix /= matrix.sum(axis=1,keepdims=True)
    image = bx.imshow(matrix,cmap=colormap(),vmin=0,vmax=matrix.max(),aspect="equal")
    bx.set(xlabel="Key token",ylabel="Query token",xticks=[0,5,10,15],yticks=[0,5,10,15])
    heading(bx,"b","Attention structure")
    fig.colorbar(image,ax=bx,fraction=.045,pad=.04,label="Attention weight")
    return fig, {"models":4,"seeds":6,"checkpoints":80,"attention_shape":[16,16]}


def scientific(rng, colors):
    fig,(ax,bx)=plate(2,"Scientific plots","Signal structure across experimental conditions",
        "3 conditions  /  12 repeated traces each  /  2,048 samples per trace",
        "Signals: damped 18/30/42 Hz sinusoids plus Gaussian noise. Bands show repeat SD. FFT amplitude uses a Hann window and coherent-gain normalization.")
    t=np.arange(2048)/1024
    for i,color in enumerate(colors[:3]):
        signals=np.array([np.exp(-t*.8)*np.sin(2*np.pi*(18+12*i)*t)+rng.normal(0,.16,len(t)) for _ in range(12)])
        mean,sd=signals.mean(0),signals.std(0,ddof=1)
        ax.plot(t,mean+2.5*i,color=color,lw=1.55,label=f"Condition {i+1}")
        ax.fill_between(t,mean-sd+2.5*i,mean+sd+2.5*i,color=color,alpha=.16,lw=0)
        window=np.hanning(len(t))
        amp=2*np.abs(np.fft.rfft(signals*window,axis=1))/window.sum()
        freq=np.fft.rfftfreq(len(t),1/1024)
        bx.plot(freq,amp.mean(0),color=color,lw=1.3)
    ax.set(xlabel=r"Time, $t$ (s)",ylabel="Amplitude + display offset (a.u.)",xlim=(0,.6))
    bx.set(xlabel="Frequency (Hz)",ylabel="Mean amplitude (a.u.)",xlim=(0,65))
    ax.legend(ncols=3,loc="upper right",fontsize=9)
    for axis,letter,title in [(ax,"a","Repeated signals"),(bx,"b","Frequency signature")]:
        refine_axes(axis); heading(axis,letter,title)
    return fig,{"conditions":3,"repeats":12,"samples":2048,"sample_rate_hz":1024}


def three_d(rng, colors):
    fig,(ax,bx)=plate(3,"3D","A response landscape with a shared projection",
        "Analytic field  /  100 × 100 grid  /  Orthographic surface + contour",
        "Analytic demonstration: z = exp(−0.18(x²+y²)) cos(1.4x) sin(1.2y). Both views use identical limits and the same zero-centered color scale.",True)
    x=np.linspace(-3,3,100); xx,yy=np.meshgrid(x,x)
    zz=np.exp(-.18*(xx**2+yy**2))*np.cos(1.4*xx)*np.sin(1.2*yy)
    norm=Normalize(-.8,.8); cmap=colormap("diverging")
    ax.plot_surface(xx,yy,zz,cmap=cmap,norm=norm,linewidth=0,antialiased=True,rasterized=True)
    ax.plot_wireframe(xx,yy,zz,rcount=12,ccount=12,color=INK,lw=.25,alpha=.3)
    ax.set_proj_type("ortho"); ax.view_init(28,-58)
    ax.set(xlabel=r"$x$ (a.u.)",ylabel=r"$y$ (a.u.)",zlabel=r"$z$ (a.u.)",zlim=(-.8,.8))
    ax.set_box_aspect((1,1,.65)); ax.tick_params(labelsize=8)
    for axis in [ax.xaxis,ax.yaxis,ax.zaxis]:
        axis.pane.fill=False
    image=bx.contourf(xx,yy,zz,levels=np.linspace(-.8,.8,25),cmap=cmap,norm=norm)
    bx.contour(xx,yy,zz,levels=[0],colors=INK,linewidths=.7)
    bx.set(xlabel=r"$x$ (a.u.)",ylabel=r"$y$ (a.u.)",aspect="equal")
    fig.colorbar(image,ax=bx,fraction=.045,pad=.04,label=r"Response, $z$")
    heading(ax,"a","Response surface"); heading(bx,"b","Zero-contour projection")
    return fig,{"grid":[100,100],"analytic":True,"view":[28,-58]}


def academic(rng, colors):
    estimates=rng.normal(.28,.17,18); se=rng.uniform(.04,.10,18)
    fig,(ax,bx)=plate(4,"Academic plots","Cohort precision alongside individual trajectories",
        "18 independent cohorts  /  80 longitudinal subjects  /  8 visits",
        "Left: simulated estimates and known-SE normal 95% intervals, grouped into three strata. Right: individual trajectories and mean ±1 SD; views are separate illustrative datasets.")
    rows=np.arange(18)+np.repeat([0,1,2],6)
    for g,color in enumerate(colors[:3]):
        ix=slice(g*6,(g+1)*6)
        ax.errorbar(estimates[ix],rows[ix],xerr=1.96*se[ix],fmt="o",color=color,ms=3.8,elinewidth=1.1,capsize=2)
    ax.axvline(0,color=GRAY,lw=.8,ls="--")
    ax.set_yticks(rows,[f"C{i+1:02d}" for i in range(18)])
    ax.invert_yaxis(); ax.set(xlabel="Standardized difference",ylabel="Cohort")
    ax.tick_params(axis="y",labelsize=7)
    visits=np.arange(1,9)
    traces=rng.normal(0,.5,(80,1))+.11*visits+rng.normal(0,.22,(80,8))
    bx.plot(visits,traces.T,color=colors[0],alpha=.12,lw=.6)
    mean,sd=traces.mean(0),traces.std(0,ddof=1)
    bx.fill_between(visits,mean-sd,mean+sd,color=colors[2],alpha=.18,lw=0)
    bx.plot(visits,mean,color=colors[2],marker="o",lw=2,ms=4,label="Mean ±1 SD")
    bx.legend(loc="upper left",fontsize=9)
    bx.set(xlabel="Visit",ylabel="Outcome (a.u.)")
    refine_axes(ax,"x"); refine_axes(bx)
    heading(ax,"a","Grouped cohort effects"); heading(bx,"b","Within-subject change")
    return fig,{"cohorts":18,"subjects":80,"visits":8}


def statistical(rng, colors):
    groups=[rng.normal(mu,sd,100) for mu,sd in [(0,1),(.28,1.1),(.62,.85),(.95,1.2)]]
    fig,(ax,bx)=plate(5,"Statistical test","Distributions first, inference alongside",
        "4 independent groups  /  100 observations each  /  3 planned contrasts",
        "Welch two-sided tests versus control; p-values use Holm correction across three contrasts. Intervals are pointwise Welch 95% CIs, not simultaneous. Jitter is deterministic.")
    violins=ax.violinplot(groups,positions=np.arange(4),widths=.72,showextrema=False)
    for body,color in zip(violins["bodies"],colors):
        body.set_facecolor(color); body.set_edgecolor("none"); body.set_alpha(.23)
    for i,(values,color) in enumerate(zip(groups,colors)):
        ax.scatter(i+rng.uniform(-.12,.12,len(values)),values,s=5,color=color,alpha=.5,edgecolors="none",rasterized=True)
        q1,median,q3=np.quantile(values,[.25,.5,.75])
        ax.plot([i,i],[q1,q3],color=INK,lw=3); ax.plot(i,median,"o",color="white",ms=3)
    ax.set_xticks(range(4),["Control","A","B","C"]); ax.set_ylabel("Outcome (a.u.)")
    tests=[stats.ttest_ind(values,groups[0],equal_var=False) for values in groups[1:]]
    p=np.array([t.pvalue for t in tests]); order=np.argsort(p)
    corrected=np.empty(3); corrected[order]=np.minimum(1,np.maximum.accumulate(p[order]*np.arange(3,0,-1)))
    effects=[]; cis=[]
    for i,values in enumerate(groups[1:]):
        control=groups[0]; a=values.var(ddof=1)/len(values); b=control.var(ddof=1)/len(control)
        se=np.sqrt(a+b); df=(a+b)**2/(a*a/(len(values)-1)+b*b/(len(control)-1))
        effect=values.mean()-control.mean(); ci=stats.t.ppf(.975,df)*se
        effects.append(float(effect)); cis.append([float(effect-ci),float(effect+ci)])
        bx.errorbar(effect,i,xerr=ci,fmt="o",color=colors[i+1],capsize=3,ms=6)
        bx.text(.98,i+.24,rf"Holm $p$ = {corrected[i]:.2g}",transform=bx.get_yaxis_transform(),ha="right",fontsize=9,color="#465966")
    bx.set_yticks(range(3),["A − control","B − control","C − control"])
    bx.set(xlabel="Mean difference (95% CI)",ylim=(-.6,2.65))
    bx.axvline(0,color=GRAY,lw=.8,ls="--")
    refine_axes(ax); refine_axes(bx,"x")
    heading(ax,"a","Observed distributions"); heading(bx,"b","Effects and adjusted tests")
    return fig,{"group_sizes":[100]*4,"holm_p":corrected.tolist(),"effects":effects,"pointwise_ci":cis}


def regression(rng, colors):
    x=rng.uniform(-3,3,600); y=.6+.7*x-.22*x*x+rng.normal(0,.7,600)
    X=np.column_stack([np.ones(len(x)),x,x*x]); beta=np.linalg.lstsq(X,y,rcond=None)[0]
    fitted=X@beta; residual=y-fitted; sigma2=residual@residual/(len(y)-3)
    cov=sigma2*np.linalg.inv(X.T@X)
    grid=np.linspace(-3,3,180); design=np.column_stack([np.ones(len(grid)),grid,grid*grid])
    pred=design@beta; half=stats.t.ppf(.975,len(x)-3)*np.sqrt(np.einsum("ij,jk,ik->i",design,cov,design))
    r2=1-np.sum(residual**2)/np.sum((y-y.mean())**2)
    fig,(ax,bx)=plate(6,"Regression models","A fitted relationship with its diagnostic evidence",
        "600 observations  /  Quadratic ordinary least squares  /  Pointwise mean uncertainty",
        "OLS includes intercept, x and x². Shaded band: pointwise 95% CI for mean response under homoscedastic independent-error assumptions; it is not a prediction interval.")
    ax.scatter(x,y,s=11,color=colors[0],alpha=.4,edgecolors="none",rasterized=True)
    ax.fill_between(grid,pred-half,pred+half,color=colors[1],alpha=.22,lw=0)
    ax.plot(grid,pred,color=colors[1],lw=1.8,label="OLS mean + 95% CI")
    ax.legend(loc="lower right",fontsize=9)
    ax.text(.03,.95,rf"$n$ = {len(x)}; $R^2$ = {r2:.2f}",transform=ax.transAxes,va="top",fontsize=9)
    ax.set(xlabel=r"Predictor, $x$",ylabel=r"Response, $y$")
    bx.scatter(fitted,residual,s=8,color=colors[2],alpha=.4,edgecolors="none",rasterized=True)
    bx.axhline(0,color=INK,lw=.8,ls="--"); bx.set(xlabel="Fitted response",ylabel="Residual")
    refine_axes(ax); refine_axes(bx)
    heading(ax,"a","Response and mean confidence band"); heading(bx,"b","Residual structure")
    return fig,{"n":600,"coefficients":beta.tolist(),"r_squared":float(r2)}


def machine_learning(rng, colors):
    X,y=make_classification(n_samples=2400,n_features=16,n_informative=8,weights=[.75,.25],random_state=SEED)
    train,test=train_test_split(np.arange(len(y)),test_size=.35,stratify=y,random_state=SEED)
    fig,(ax,bx)=plate(7,"Machine learning","Discrimination on an untouched evaluation split",
        "2,400 samples  /  16 features  /  35% stratified held-out evaluation",
        "Fixed hyperparameters; preprocessing fits training data only. Both models use the same held-out samples. AP denotes average precision, not trapezoidal PR area. No interval is claimed.")
    metrics={}
    for name,model,color in [("Logistic",make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000)),colors[0]),
                              ("Random forest",RandomForestClassifier(n_estimators=120,max_depth=8,random_state=SEED,n_jobs=1),colors[1])]:
        model.fit(X[train],y[train]); prob=model.predict_proba(X[test])[:,1]
        fpr,tpr,_=roc_curve(y[test],prob); precision,recall,_=precision_recall_curve(y[test],prob)
        auc=roc_auc_score(y[test],prob); ap=average_precision_score(y[test],prob)
        ax.plot(fpr,tpr,color=color,label=f"{name}  AUC {auc:.3f}",lw=1.6)
        bx.plot(recall,precision,color=color,label=f"{name}  AP {ap:.3f}",lw=1.6)
        metrics[name]={"auc":float(auc),"average_precision":float(ap)}
    prevalence=float(y[test].mean())
    ax.plot([0,1],[0,1],color=GRAY,ls="--",lw=.8)
    bx.axhline(prevalence,color=GRAY,ls="--",lw=.8,label=f"Prevalence {prevalence:.2f}")
    ax.set(xlabel="False positive rate",ylabel="True positive rate",xlim=(0,1),ylim=(0,1.02))
    bx.set(xlabel="Recall",ylabel="Precision",xlim=(0,1),ylim=(0,1.02))
    for axis,letter,title in [(ax,"a","Receiver operating characteristic"),(bx,"b","Precision–recall")]:
        refine_axes(axis)
        axis.set_xticks([0,.25,.5,.75,1]); axis.set_yticks([0,.25,.5,.75,1])
        heading(axis,letter,title); axis.legend(loc="lower left" if axis is bx else "lower right",fontsize=9)
    return fig,{"n":2400,"train_n":len(train),"test_n":len(test),"prevalence":prevalence,"metrics":metrics}


def bioinformatics(rng, colors):
    expression=rng.normal(6,1,(2000,16))
    expression[:120,8:]+=1.5; expression[120:240,8:]-=1.5
    effect=expression[:,8:].mean(1)-expression[:,:8].mean(1)
    p=stats.ttest_ind(expression[:,8:],expression[:,:8],axis=1,equal_var=False).pvalue
    order=np.argsort(p); q=np.empty_like(p)
    q[order]=np.minimum(1,np.minimum.accumulate((p[order]*len(p)/np.arange(1,len(p)+1))[::-1])[::-1])
    selected=(q<.05)&(abs(effect)>1)
    fig,(ax,bx)=plate(8,"Bioinformatic analysis","Feature-level change and coordinated expression",
        "2,000 features × 16 samples  /  8 biological replicates per independent group",
        "Continuous synthetic log2 expression; Welch tests + BH across all 2,000 features. Heatmap: top 40 by q, row z-score, average-linkage Euclidean row clustering; not a raw-count RNA-seq workflow.")
    for mask,color,label in [(~selected,"#798894","Other"),(selected&(effect<0),colors[0],"Lower"),(selected&(effect>0),colors[1],"Higher")]:
        ax.scatter(effect[mask],-np.log10(np.clip(q[mask],1e-300,1)),s=12,color=color,alpha=.84,edgecolors="none",label=label,rasterized=True)
    ax.axhline(-np.log10(.05),color=GRAY,lw=.8,ls="--")
    for threshold in [-1,1]: ax.axvline(threshold,color=GRAY,lw=.8,ls="--")
    ax.set(xlabel=r"Mean difference (log$_2$ expression)",ylabel=r"$-\log_{10}(q)$")
    ax.legend(loc="lower right",fontsize=9)
    top=np.argsort(q,kind="stable")[:40]
    z=stats.zscore(expression[top],axis=1,ddof=1)
    row_order=leaves_list(linkage(z,method="average",metric="euclidean"))
    image=bx.imshow(z[row_order],cmap=colormap("diverging"),vmin=-2.5,vmax=2.5,aspect="auto",interpolation="nearest")
    bx.axvline(7.5,color="white",lw=2)
    bx.set_xticks([3.5,11.5],["Control · 8","Treatment · 8"])
    bx.set_yticks([0,9,19,29,39],[f"F{top[row_order[i]]+1:04d}" for i in [0,9,19,29,39]])
    bx.set(xlabel="Independent samples",ylabel="Selected features")
    fig.colorbar(image,ax=bx,fraction=.045,pad=.04,label="Row z-score",ticks=[-2,0,2])
    refine_axes(ax,"x"); heading(ax,"a","Effect and false discovery rate"); heading(bx,"b","Coordinated expression")
    return fig,{"features":2000,"samples":16,"selected_q05_and_abs_effect_gt1":int(selected.sum()),"heatmap_features":(top[row_order]+1).tolist(),"min_q":float(q.min())}


FAMILIES={"artificial-intelligence":ai,"scientific-plots":scientific,"3d":three_d,
          "academic-plots":academic,"statistical-test":statistical,"regression-models":regression,
          "machine-learning":machine_learning,"bioinformatics":bioinformatics}


def integrated_plate(colors):
    """Six aligned views of the same simulated expression experiment."""
    rng=np.random.default_rng(SEED+7)
    expression=rng.normal(6,1,(2000,16))
    expression[:120,8:]+=1.5; expression[120:240,8:]-=1.5
    effect=expression[:,8:].mean(1)-expression[:,:8].mean(1)
    p=stats.ttest_ind(expression[:,8:],expression[:,:8],axis=1,equal_var=False).pvalue
    q=stats.false_discovery_control(p,method="bh")
    top=np.argsort(q,kind="stable")[:50]
    z=stats.zscore(expression[top],axis=1,ddof=1)
    tree=linkage(z,method="average",metric="euclidean")
    order=leaves_list(tree)
    # Center each feature across samples, then use SVD for sample PCA.
    centered=expression.T-expression.mean(axis=1)
    u,s,_=np.linalg.svd(centered,full_matrices=False)
    scores=u[:,:2]*s[:2]; variance=s*s/np.sum(s*s)
    low,high=colors[1],colors[2]
    selected=(q<.05)&(abs(effect)>1)
    fig=plt.figure(figsize=(16,9))
    fig.text(.055,.965,"From sample structure to feature-level evidence",fontsize=16,fontweight="semibold",color=INK)
    fig.legend(handles=[Line2D([],[],color=colors[0],marker="o",ls="",label="Control"),
                        Line2D([],[],color=high,marker="s",ls="",label="Treatment"),
                        Line2D([],[],color="#798894",marker="o",ls="",label="Other"),
                        Line2D([],[],color=low,marker="o",ls="",label="Lower: q < .05, |effect| > 1"),
                        Line2D([],[],color=high,marker="o",ls="",label="Higher: q < .05, |effect| > 1")],
               loc="center right",bbox_to_anchor=(.96,.963),ncols=5,fontsize=9,
               columnspacing=.7,handletextpad=.4)
    grid=fig.add_gridspec(2,3,left=.065,right=.96,bottom=.13,top=.91,
                          width_ratios=[1,1,1],wspace=.30,hspace=.38)
    a,b,c=(fig.add_subplot(grid[0,i]) for i in range(3))
    d,e,f=(fig.add_subplot(grid[1,i]) for i in range(3))
    for mask,color in [(~selected,"#798894"),(selected&(effect<0),low),(selected&(effect>0),high)]:
        a.scatter(effect[mask],-np.log10(q[mask]),s=10,color=color,alpha=.92,edgecolors="none",rasterized=True)
    a.axhline(-np.log10(.05),color="#526574",ls="--",lw=1.1)
    for x in [-1,1]: a.axvline(x,color="#526574",ls="--",lw=1.1)
    a.set(xlabel=r"Difference (log$_2$ units)",ylabel=r"$-\log_{10}(q)$")
    refine_axes(a,"x"); heading(a,"a","Feature-level changes")
    for ix,color,label,marker in [(slice(0,8),colors[0],"Control","o"),(slice(8,16),high,"Treatment","s")]:
        b.scatter(scores[ix,0],scores[ix,1],color=color,s=42,marker=marker,label=label,edgecolors="white",lw=.65)
    b.set(xlabel=f"PC1 ({variance[0]:.1%})",ylabel=f"PC2 ({variance[1]:.1%})")
    refine_axes(b,None); heading(b,"b","Sample structure")
    image=c.imshow(z[order],aspect="auto",cmap=colormap("diverging"),
                   vmin=-2.5,vmax=2.5,interpolation="nearest")
    c.axvline(7.5,color="white",lw=2)
    c.set_xticks([3.5,11.5],["Control","Treatment"]); c.set_yticks([])
    c.set_xlabel("Independent biological replicates")
    refine_axes(c,None)
    heading(c,"c","Top 50 features · row z-score")
    fig.colorbar(image,ax=c,fraction=.05,pad=.04,ticks=[-2,0,2],label="Row z-score")
    for i in range(16):
        q1,median,q3=np.quantile(expression[:,i],[.25,.5,.75])
        color=colors[0] if i<8 else high
        d.vlines(i,q1,q3,color=color,lw=2.4); d.plot(i,median,"o",color=color,ms=4)
    d.axvline(7.5,color="#637482",lw=1,ls="--")
    d.set_xticks([3.5,11.5],["Control · 8","Treatment · 8"])
    d.set(xlabel="Sample",ylabel=r"Expression (log$_2$)")
    refine_axes(d); heading(d,"d","Median and interquartile range")
    e.hist(effect,bins=45,color=colors[0],alpha=.92,edgecolor="white",lw=.45)
    for threshold,color in [(-1,low),(1,high)]: e.axvline(threshold,color=color,ls="--",lw=1.2)
    e.set(xlabel=r"Mean difference (log$_2$ units)",ylabel="Feature count")
    refine_axes(e); heading(e,"e","Global effect distribution")
    dendrogram(tree,no_labels=True,color_threshold=0,above_threshold_color="#81949F",ax=f)
    f.set(xlabel="Selected feature rank",ylabel="Euclidean distance")
    refine_axes(f,None); f.set_xticks([])
    heading(f,"f","Feature clustering")
    note=("METHOD / Continuous synthetic log2 expression; 8 independent biological replicates per group; Welch tests; BH over 2,000 features. PCA uses all centered features. "
          "Top 50 q-selected features: row z-score, Euclidean average linkage. Sample summaries span all features. No raw-count RNA-seq inference is claimed.")
    fig.text(.055,.075,"\n".join(textwrap.wrap(note,185)),fontsize=8,color="#465966",va="top",linespacing=1.35)
    fig.text(.055,.025,"SYNTHETIC DESIGN DATA  /  NOT RESEARCH FINDINGS",fontsize=8,fontweight="medium",color="#64748B")
    return fig


def main(output, only=None):
    use_publication_style(ROOT/"assets/publication.mplstyle",context="screen")
    colors=palette_colors()
    output=Path(output); output.mkdir(parents=True,exist_ok=True)
    manifest={"seed":SEED,"synthetic":True,"analyses":{}}
    for index,(name,fn) in enumerate(FAMILIES.items()):
        if only and name not in only: continue
        fig,summary=fn(np.random.default_rng(SEED+index),colors)
        save_publication_figure(fig,output/name,dpi=300)
        manifest["analyses"][name]=summary
        print(name)
    (output/"analysis-summary.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    if only: return
    save_publication_figure(integrated_plate(colors),output/"integrated-research-plate",dpi=300)
    # A catalog sheet is a separate overview; individual files retain readable type.
    fig,axes=plt.subplots(4,2,figsize=(16,16),layout="constrained")
    for ax,name in zip(axes.flat,FAMILIES):
        ax.imshow(plt.imread(output/f"{name}.png")); ax.set_axis_off()
    save_publication_figure(fig,output/"domain-atlas",formats=("png",),dpi=160)


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",default=str(ROOT/"docs/gallery/domains"))
    parser.add_argument("--only",nargs="+",choices=list(FAMILIES))
    args=parser.parse_args(); main(args.output,args.only)
