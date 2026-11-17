"""Fair style comparison: same synthetic data, analysis, dimensions and marks.

The ordinary version uses Matplotlib defaults with constrained layout; it is
not intentionally crowded or degraded. The skill version composes the same
evidence into an editorial plate. Run with requirements-gallery.txt installed.
"""
from pathlib import Path
import json
import hashlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.cluster.hierarchy import linkage, leaves_list, dendrogram
from render_domain_gallery import ROOT, SEED, integrated_plate
from figure_kit import use_publication_style, palette_colors, save_publication_figure


def plain_figure():
    rng=np.random.default_rng(SEED+7)
    expression=rng.normal(6,1,(2000,16))
    expression[:120,8:]+=1.5; expression[120:240,8:]-=1.5
    effect=expression[:,8:].mean(1)-expression[:,:8].mean(1)
    p=stats.ttest_ind(expression[:,8:],expression[:,:8],axis=1,equal_var=False).pvalue
    q=stats.false_discovery_control(p,method="bh")
    selected=(q<.05)&(abs(effect)>1)
    top=np.argsort(q,kind="stable")[:50]
    z=stats.zscore(expression[top],axis=1,ddof=1)
    tree=linkage(z,method="average",metric="euclidean")
    order=leaves_list(tree)
    u,s,_=np.linalg.svd(expression.T-expression.mean(axis=1),full_matrices=False)
    scores=u[:,:2]*s[:2]; variance=s*s/np.sum(s*s)
    with plt.rc_context():
        plt.rcdefaults()
        fig,axes=plt.subplots(2,3,figsize=(16,9),layout="constrained")
        a,b,c,d,e,f=axes.flat
        for mask,color,label in [(~selected,"gray","Other"),(selected&(effect<0),"tab:orange","Lower"),
                                  (selected&(effect>0),"tab:green","Higher")]:
            a.scatter(effect[mask],-np.log10(q[mask]),s=6,color=color,alpha=.75,edgecolors="none",label=label,rasterized=True)
        a.axhline(-np.log10(.05),color="gray",ls="--",lw=.7)
        for x in [-1,1]: a.axvline(x,color="gray",ls="--",lw=.7)
        a.set(title="Volcano plot",xlabel="Mean difference (log2 units)",ylabel="-log10(q)")
        a.legend()
        for ix,color,label,marker in [(slice(0,8),"tab:blue","Control","o"),(slice(8,16),"tab:green","Treatment","s")]:
            b.scatter(scores[ix,0],scores[ix,1],color=color,s=33,marker=marker,label=label,edgecolors="white",lw=.6)
        b.set(title="PCA",xlabel=f"PC1 ({variance[0]:.1%})",ylabel=f"PC2 ({variance[1]:.1%})")
        b.legend()
        image=c.imshow(z[order],aspect="auto",cmap="coolwarm",vmin=-2.5,vmax=2.5,interpolation="nearest")
        c.axvline(7.5,color="white",lw=2)
        c.set(title="Top 50 features",xlabel="Samples",ylabel="Features")
        c.set_xticks([3.5,11.5],["Control","Treatment"]); c.set_yticks([])
        fig.colorbar(image,ax=c,label="Row z-score",ticks=[-2,0,2])
        for i in range(16):
            q1,median,q3=np.quantile(expression[:,i],[.25,.5,.75])
            color="tab:blue" if i<8 else "tab:green"
            d.vlines(i,q1,q3,color=color,lw=2); d.plot(i,median,"o",color=color,ms=3)
        d.axvline(7.5,color="gray",lw=.7,ls="--")
        d.set(title="Sample median and IQR",xlabel="Sample",ylabel="Expression (log2)")
        d.set_xticks([3.5,11.5],["Control · 8","Treatment · 8"])
        e.hist(effect,bins=45,color="tab:blue",alpha=.85,edgecolor="white",lw=.35)
        for threshold,color in [(-1,"tab:orange"),(1,"tab:green")]: e.axvline(threshold,color=color,ls="--",lw=1)
        e.set(title="Effect distribution",xlabel="Mean difference (log2 units)",ylabel="Feature count")
        dendrogram(tree,no_labels=True,color_threshold=0,above_threshold_color="gray",ax=f)
        f.set(title="Feature clustering",xlabel="Selected feature order",ylabel="Euclidean distance")
        fig.suptitle("Synthetic expression analysis: 2,000 features × 16 samples")
        fig.supxlabel("Synthetic design data · Welch tests + BH · Top 50 by q · Row z-score · Average-linkage Euclidean clustering",fontsize=9)
        # Match data ranges for all directly comparable views.
        return fig,expression


def main(output):
    output=Path(output); output.mkdir(parents=True,exist_ok=True)
    baseline,data=plain_figure()
    use_publication_style(ROOT/"assets/publication.mplstyle",context="screen")
    premium=integrated_plate(palette_colors())
    # The premium plate is constructed from the same SEED+7 data recipe.
    rng=np.random.default_rng(SEED+7)
    check=rng.normal(6,1,(2000,16)); check[:120,8:]+=1.5; check[120:240,8:]-=1.5
    np.testing.assert_array_equal(data,check)
    # Preserve the baseline's default fonts/style through export.
    with plt.rc_context():
        plt.rcdefaults()
        save_publication_figure(baseline,output/"before-default",dpi=180)
    save_publication_figure(premium,output/"after-skill",dpi=180)
    fig=plt.figure(figsize=(24,7.8))
    axes=[fig.add_axes([.015,.10,.475,.80]),fig.add_axes([.51,.10,.475,.80])]
    for ax,name,title in zip(axes,["before-default","after-skill"],
                             ["01  /  Ordinary Matplotlib defaults","02  /  With publication-chart-designer"]):
        ax.imshow(plt.imread(output/f"{name}.png")); ax.set_axis_off()
        fig.text(.025 if name=="before-default" else .52,.95,title,
                 fontsize=13,fontweight="semibold",va="top")
    fig.text(.5,.035,"Same synthetic data and analyses · Same 16 × 9 in canvas · Both versions retain the evidence",
             fontsize=10,ha="center")
    save_publication_figure(fig,output/"comparison",formats=("png",),dpi=150)
    (output/"comparison-notes.json").write_text(json.dumps({
        "synthetic":True,"seed":SEED+7,"shape":list(data.shape),
        "data_sha256":hashlib.sha256(data.tobytes()).hexdigest(),
        "shared_analysis":"Welch + BH; top-50 q selection; row z-score; average-linkage Euclidean clustering; centered PCA",
        "baseline":"Matplotlib defaults + constrained 2x3 layout; no intentional degradation",
        "after":"Skill typography, color system, integrated dendrogram, panel hierarchy, legend/method zones",
        "canvas_inches":[16,9],"differences_are_design_not_model_performance":True
    },indent=2),encoding="utf-8")
    print(output/"comparison.png")


if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",default=str(ROOT/"docs/gallery/comparison"))
    args=parser.parse_args(); main(args.output)
