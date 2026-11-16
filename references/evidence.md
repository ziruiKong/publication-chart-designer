# Evidence Base

Use these sources as design evidence, not as a substitute for the user's
domain conventions. The chart playbook refers to entries by key.

## E1. Graphical Perception

Cleveland WS, McGill R. “Graphical Perception: Theory, Experimentation, and
Application to the Development of Graphical Methods.” *Journal of the American
Statistical Association* 79, no. 387 (1984): 531–554.
https://doi.org/10.1080/01621459.1984.10478080

Supports: elementary perceptual tasks differ in accuracy; position and length
are generally more accurate than angle, area, or volume; replace weak
encodings with dot charts and framed rectangles when possible.

## E2. Crowdsourced Graphical Perception

Heer J, Bostock M. “Crowdsourcing Graphical Perception: Using Mechanical Turk
to Assess Visualization Design.” *CHI 2010*.
https://doi.org/10.1145/1753326.1753357

Supports: perceptual encoding rankings can be tested at scale; chart size,
gridline spacing, and spatial encoding are design variables rather than neutral
defaults.

## E3. Attention and Working Memory

Franconeri SL, Padilla LM, Shah P, Zacks JM, Hullman J. “The Science of Visual
Data Communication: What Works.” *Psychological Science in the Public Interest*
22, no. 2 (2021): 95–139.
https://doi.org/10.1177/15291006211051956

Supports: viewers extract broad visual statistics quickly but compare subsets
slowly; effective graphics avoid taxing working memory, guide attention, and
respect familiar conventions.

## E4. Small Multiples

Becker RA, Cleveland WS, Shyu M-J. “The Visual Design and Control of Trellis
Display.” *Journal of Computational and Graphical Statistics* 5, no. 2 (1996):
123–155. https://doi.org/10.1080/10618600.1996.10474701

Supports: conditional small multiples with shared scales make subgroup
comparisons easier than overloading one panel with every combination.

## E5. Scientific Figure Design

Rougier NP, Droettboom M, Bourne PE. “Ten Simple Rules for Better Figures.”
*PLOS Computational Biology* 10, no. 9 (2014): e1003833.
https://doi.org/10.1371/journal.pcbi.1003833

Supports: identify audience and message; adapt to the medium; use captions;
avoid defaults and chartjunk; use color intentionally; avoid misleading
encodings; message and readability outrank decoration.

## E6. Show Distributions, Not Only Summaries

Weissgerber TL, Milic NM, Winham SJ, Garovic VD. “Beyond Bar and Line Graphs:
Time for a New Data Presentation Paradigm.” *PLOS Biology* 13, no. 4 (2015):
e1002128. https://doi.org/10.1371/journal.pbio.1002128

Supports: bar and line summaries can hide skew, outliers, subgroups, unequal
variance, and paired structure; show raw observations for small samples.

## E7. Raincloud Plots

Allen M, Poggiali D, Whitaker K, Marshall TR, Kievit RA. “Raincloud Plots: A
Multi-Platform Tool for Robust Data Visualization.” *Wellcome Open Research*
4 (2019): 63. https://doi.org/10.12688/wellcomeopenres.15191.2

Supports: combining raw data, distribution, and key summaries can convey more
information with little redundancy than mean-and-error-bar summaries alone.

## E8. Forest Plots

Lewis S, Clarke M. “Forest Plots: Trying to See the Wood and the Trees.” *BMJ*
322, no. 7300 (2001): 1479–1480.
https://doi.org/10.1136/bmj.322.7300.1479

Supports: forest plots conventionally use point estimates, interval lines, and
an overall summary; they are designed for viewing many study or model
estimates and their uncertainty together.

## E9. Estimation Graphics

Ho J, Tumkaya T, Aryal S, Choi H, Claridge-Chang A. “Moving Beyond P Values:
Data Analysis with Estimation Graphics.” *Nature Methods* 16 (2019): 565–566.
https://doi.org/10.1038/s41592-019-0470-3

Supports: prioritize effect sizes and intervals in figures rather than reducing
evidence to p-value thresholds or star annotations.

## E10. Scientific Colour Maps

Crameri F, Shephard GE, Heron PJ. “The Misuse of Colour in Science
Communication.” *Nature Communications* 11 (2020): 5444.
https://doi.org/10.1038/s41467-020-19160-7

Supports: use perceptually uniform, ordered, color-vision-deficiency-aware
maps; avoid rainbow and red–green maps that distort contrast or fail in
grayscale.

## E11. Color-Vision-Deficiency Optimized Maps

Nuñez JR, Anderton CR, Renslow RS. “Optimizing Colormaps with Consideration
for Color Vision Deficiency to Enable Accurate Interpretation of Scientific
Data.” *PLOS ONE* 13, no. 8 (2018): e0199239.
https://doi.org/10.1371/journal.pone.0199239

Supports: perceptual uniformity and a linear lightness range produce more
consistent interpretation for viewers with and without red–green color-vision
deficiency.

## E12. Map Color Schemes

Brewer CA, Hatchard GW, Harrower MA. “ColorBrewer in Print: A Catalog of Color
Schemes for Maps.” *Cartographic Perspectives* 44 (2003): 5–32.
https://doi.org/10.1559/152304003100010929

Supports: use purpose-built sequential, diverging, and qualitative schemes;
match scheme type to the map's data ordering rather than choosing colors
decoratively.

## E13. Scientific Visualization Guidelines

Kelleher C, Wagener T. “Ten Guidelines for Effective Data Visualization in
Scientific Publications.” *Environmental Modelling & Software* 26, no. 6
(2011): 822–827. https://doi.org/10.1016/j.envsoft.2010.12.006

Supports: publication figures should be designed for the reader and medium,
make the data comparison salient, and avoid unnecessary visual complexity.

## E14. Event-Study Visualization

Freyaldenhoven S, Hansen C, Pérez JP, Shapiro JM. “Visualization,
Identification, and Estimation in the Linear Panel Event-Study Design.” NBER
Working Paper 29170 (2021). https://doi.org/10.3386/w29170

Supports: event-study figures should separate dynamic effects from identifying
assumptions, show a reference period, and make pre-trend patterns interpretable.

## E15. Data-Ink and Chartjunk

Tufte ER. *The Visual Display of Quantitative Information*. 2nd ed. Graphics
Press, 2001.

Supports: remove non-data ink that does not improve understanding and avoid
decoration that competes with the quantitative comparison.
