# Scientific figure atlas

Analysis API references: [SciPy Welch test](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html)
and [false discovery control](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.false_discovery_control.html).
Use the documented assumptions and distinguish FDR from familywise error control.

Choose the analytical family, then compose an ordered plate with a primary
result and relevant supporting views. The eight families below correspond to
the user's requested scope, also displayed on [MindPlot](https://mindplot.ai/).
They overlap: classify by the question, not a marketing label. The examples in
`scripts/render_domain_gallery.py` are reproducible synthetic demonstrations.
They are not an implementation of every analysis listed below.

| Family | Main encodings | Supporting panels |
| --- | --- | --- |
| Artificial intelligence | Training/validation curves, ablation estimates, benchmark matrix, attention map | Seed variability, compute/quality trade-off, subgroup error |
| Scientific plots | Signals, spectra, Bode, phase diagrams, contour/field maps, ridgelines | Residuals, uncertainty envelope, instrument baseline |
| 3D | Response surface, 3D scatter, wireframe, parametric trajectory | Matched contour/projection, common color scale |
| Academic plots | Forest/meta-analysis, repeated measures, survey distributions, survival | Subgroup bands, risk table, heterogeneity |
| Statistical test | Distribution + raw observations, paired changes, effect-size intervals | Multiplicity-aware test table, assumptions/diagnostics |
| Regression models | Fitted response with CI/PI, coefficient forest, partial effects | Residuals, Q–Q, influence, calibration |
| Machine learning | ROC, PR, confusion matrix, calibration, learning curve | Held-out metric intervals, feature stability, error by group |
| Bioinformatics | Volcano, MA, expression heatmap, PCA/UMAP, enrichment dot plot, genomic tracks | Cohort annotation, clustering dendrogram, quality metrics |

## Artificial intelligence

Separate AI-specific experiment structure (seeds, checkpoints, ablations,
compute budget, model versions) from generic ML evaluation. Show seed variation
as SD or an explicitly computed CI, not a decorative band. Never call an
attention map an explanation of causality. Align benchmark rows/columns and
use a clearly labeled normalization when tasks have incomparable metrics.
Avoid cherry-picking the best seed, hiding failed runs, or mixing validation
and test performance. The gallery pairs four-model, six-seed learning curves
with a row-normalized attention matrix.

## Scientific plots

Preserve sampling interval, frequency resolution, physical units, calibration,
and transformations. Distinguish power, amplitude, and power spectral density;
state windowing and normalization. Use shared axes for comparable signals,
stacked offset spectra when overlap conceals peaks, and a side color key for
ordered conditions. For Bode plots, align frequency axes and label dB/phase.
The gallery pairs multi-condition damped signals with window-normalized FFT
amplitude spectra computed from those signals.

## Genuine 3D

Use three dimensions when all three coordinates carry meaning or a response
surface is the object of study. The flat aesthetic concerns rendering and
typography; it does not ban genuine 3D. Use orthographic projection, restrained
panes, thin wireframe, an explicit view angle and units, and a matched 2D
projection. Keep one color scale across surface and contour. Never use 3D
extrusion merely to decorate bars or pies. Mark fitted/simulated surfaces as
such, disclose interpolation, and do not extend beyond observed support
without explaining extrapolation. The gallery uses an explicitly analytic field.

## Academic comparisons

Use a forest plot for many effects and intervals, grouped row spacing for
substantive strata, and a reference line matched to the estimand (0 for
differences, 1 for ratios). Meta-analysis requires study weights, method,
heterogeneity and interval definitions; do not manufacture a pooled diamond.
For repeated measurements preserve subject pairing and missingness. Survival
curves need censoring marks and numbers at risk; do not compute survival from
uncensored event times alone. The gallery shows 18 synthetic cohort estimates
and 80 subject trajectories; it is not a meta-analysis or survival estimator.

## Statistical testing

Establish independent versus paired sampling, the experimental unit, test
assumptions, pre-specified contrasts, and multiplicity family. Plot effect size
and uncertainty beside distributions. Report actual computed test results;
prefer exact numerical p-values with an explicit adjustment to star brackets.
Do not use independent t-tests on paired or nested observations. Never silently
choose a test by whichever produces the smallest p-value. The gallery uses
three pre-specified independent Welch contrasts against control, Holm-adjusted
p-values, and explicitly pointwise Welch 95% CIs (not simultaneous intervals).

## Regression

Identify response family/link, design matrix, covariate treatment, dependence,
and uncertainty method. Distinguish confidence bands for the mean from
prediction intervals for new observations. Plot data, model and diagnostics in
separate coordinated panels. Partial dependence, adjusted effects and observed
conditional means are different quantities. Never label a covariance-based
OLS interval as heteroscedasticity-robust or causal. The gallery fits quadratic
OLS to 600 observations and shows a pointwise mean CI with residuals.

## Machine learning

Split train/validation/test before transformations and model selection; fit
preprocessing on training data only. Define positive class, prevalence, and
independent resampling unit. Pair ROC with PR for class imbalance; show PR's
prevalence baseline, and use average precision terminology accurately.
Calibration needs bins/counts and an untouched evaluation set. Importance and
SHAP require background/sample definitions and correlated-feature caveats;
they are not causal effects. The gallery compares logistic regression and a
random forest on the same 35% held-out split of 2,400 synthetic observations.

## Bioinformatics

Establish assay, counts versus transformed expression, biological replicates,
normalization, batch handling, contrast, and multiple-testing universe. Use
validated count models for RNA-seq rather than uncritically applying t-tests
to raw counts. Volcano axes must show the actual effect and p/q definition;
thresholds are explicit. Heatmap z-scores need their axis and row selection
rule; clustering distances/linkage and sample metadata must be documented.
UMAP axes have no physical units and separation does not prove distinct biology.
Enrichment dot plots must state gene universe, correction, and size/color
encodings. The gallery analyzes continuous simulated log2 expression for
2,000 features × 16 independent samples with Welch tests and BH correction;
it is not a raw-count differential-expression pipeline. Top-40 q-selected
features are row-standardized for an exploratory heatmap, with labels reflecting
synthetic feature IDs only.

## High-dimensional data without visual disorder

Use coordinated views rather than shrinking thousands of labels. A compact
overview can reveal structure; a focused subset panel can show detail with a
declared selection rule. Keep omitted data discoverable in reproducible code.
Rasterize dense point layers in vector exports while retaining vector text.
Use shared legends, annotation tracks, aligned interval columns and consistent
scales. A dense plate passes only if a reader can identify grouping, main
comparison, uncertainty and reading order at a glance.
