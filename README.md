# The-Long-Term-Effects-of-the-Varying-Precipitation-in-Sierra-Nevada

A consequence of the increasingly turbulent global climate is that the Sierra Nevada Mountain Region - located in Eastern California - has undergone significant topographical change. In this project, we  explore the long term topographical changes attributed to the ever-changing precipitational patterns, and how the ecology of the mountain range develops accordingly. We specifically analyse the <b>long term</b> effects of the varied rainfall in this project, focusing especially on annual (or even decade-wide) fluctuations, as opposed to smaller seasonal changes.

> "...global climate models don’t capture the fine-scale topography and regional characteristics that we know shape our weather and climate around us." (Niel Berg), on the tumultuous topography of Sierra Nevada 

We start by creating a <b>DEM (Digital Elevation Model)</b> for the mountain range. We used data from the JAXA global sattelite imaging database<sup>[1]</sup> and collated it using QGIS Mapping Software<sup>[2]</sup>. This contains 7200x7200 30mx30m points.

<p align="center">
  <img src="https://github.com/user-attachments/assets/fe508619-f97e-4a34-bd10-70871ee8eca9" />
</p>

We then forecast the precipitation patterns in Sierra Nevada from historic data across 400 regions within the DEM, represented by a 20x20 Matrix := P(y), where y is the precipitation by year. This <b>lower resolution is much more appropriate</b> for this context as it is much more viable to store 2000 20x20 matricies (3MB) as opposed to 2000 7200x7200 matricies (392GB) when we proceed with using these matrices for future forecasts. 
![output](https://github.com/user-attachments/assets/d05bb357-1cc3-45a8-919e-edbaf348fdc2)

We applied a <b>random forest/ML based algorithm</b> to the data in each of these regions to forecast a precipitation matrix that fully utilises all 400 time series for each subregion, so that the y parameter within P(y) grants varied precipitation P based on the Random Forest forecast. Initially running this algorithm using a pure random forest approach led the P matricies to converge towards uniformity (ie. λJ). We modelled the noise in this process through the addition of a <b>gaussian stochastic parameter</b>, which let P(t) maintaining desirable similarities with the historic data whilst still having clear changes (that incorporated spatial growth against spontaneous growth). This is also partially because a forecast of the temperature := T is also used determine P, in order to represent how <b>more water is in the system</b>; eastern winds from the pacific<sup>[3]</sup> grant a greater net income of water into the mountain range - as well as water melting from ice - thus freeing it from storage. We can now find values for P(y) for y in the future. We now define P(t) := the matrix P, t years after today (i.e. as of 2024). 

The DEM Model can be represented as a 7200x7200 Matrix := Ca (California). Ca(0) := The initial state of Sierra Nevada, and the state of Sierra Nevada after n years is Ca(n) := P(n) ∘ C(n-1), (or Ca(n) = P(n) ∘ P(n-1) ∘ ... ∘ P(1) ∘ P(0) ∘ Ca(0)). We now need to define <b>P ∘ Ca</b>, or the effect of a year of Precipitation on the erosion of California. (P<sub>1</sub> ∘ P<sub>2</sub> = P<sub>1</sub> + P<sub>2</sub> which is summing the rainfall from 2 years)

Through the further exploration of the geology and topography of Sierra Nevada's terrain, we can specifically identify how the precipitation affects annual erosion (defining P ∘ Ca). We model erosion here through 2 primary mechanisms; <b>bombardment</b> of raindrops on the mountain surface and through the flow of water <b>flow</b> down high terrain features, like mountains. 

$$
\Delta h = \Delta h_b + \Delta h_f
$$

We first model Δh<sub>b</sub>:</br>
A notable parameter that affects the intensity of bombardment due to precipitation is the <b>slope</b>. We find a vector field ∇Ca to the mountain range DEM matrix, which we use to find the angle to the horizontal, from which we infer that the effect of bombardment on the erosion is damped, by a factor of the cosine of the angle as a scalar field. Essentially, steeper hills erode less from bombardment due to precipitation as the droplet has less of a force component into the ground.

<p align="center">
  <img src="https://github.com/user-attachments/assets/2104dd34-6c93-4e2d-8d99-fda76790484b" />
  Ca, ∇Ca  
  <img src="https://github.com/user-attachments/assets/2cc7c551-04b8-4ff2-8f90-c834261c76b5" />
  cosθ, where θ is the angle between the vertical and v ∈ ∇Ca
</p>

Different geological factors also impact this errosion, namely the rock density ρ<sub>r</sub> rate of detachability D<sub>r</sub>, which is the product of porosity ϕ, saturation s and errosion coefficient k = 0.75. We decided find the average of rocks sampled uniformly throughout the mountain range<sup>[4]</sup> to achieve ϕ = 0.0947, s = 0.487, which is similar value to that of granite, which makes sense as Sierra Nevada was formed volcanically and granite is igneous.

$$
\Delta h_b = \frac{k \phi s \cos\theta}{\rho_r}P
$$

We now model Δh<sub>f</sub>:</br>
An assumption we make when modelling errosion due to water flow is that the granite will be negligably affected, which comes as an assumption that the granite is smooth: it is difficult to model a rough surface. Instead, this takes into account elevation loss due to snow melting, where snow is dragged away by rainfall. We can consider the snow line, which is the elevation level where snow settles on a mountain, to work out where snow can fall. 

<p align="center">
  <img width="1541" alt="Screenshot 2024-11-17 at 06 39 41" src="https://github.com/user-attachments/assets/c7b7746a-5af3-4723-99d3-7dae52073c5b">
</p>

 Here, only data from the peaks (above the snow line) is able to melt and reduce; being above this threshold is a mask which can be represented using a <b>piecewise function</b>.

$$
\Delta h_f = 
\begin{cases} 
0 & h < z_{\text{snow}} \\
k \sin(\theta) P \left( \Gamma h - T_0 \right) & h \geq z_{\text{snow}}
\end{cases}
$$

where

$$
z_{\text{snow}} = z_{0} + \frac{T_0 - T_{\text{freeze}}}{\Gamma}
$$

k<sup>[5,6,7]</sup> = 0.0748

h: Height of the point (m)

z<sub>0</sub>:: Reference altitude (m)

z<sub>snow</sub>: Elevation of the snowline (m)

θ: Angle of the slope (rad)

Γ: Lapse rate (°C/m)

T<sub>0</sub>: Reference temperature (at sea level)

P = Precipitation

A resultant Δh may look like the graph below. A final method of smoothing is applied by assigning P to be a linear interpolation of the 4 grid spaces it lies nearest to. This prevents blocky/patchy rain, which could result in the terrain looking minecraft-y.
<p align="center">
  <img src="https://github.com/user-attachments/assets/0d11d538-a3de-43a6-8aa6-61e417d5fc03">
</p>


We can finally visualise Ca(t) as P ∘ Ca has been defined.
--Gif of the future, long into the future

## The Effect on the Long-Term Ecology
One obvious ecological feature that can be observed from this data is the effect on the physical elevations/topography of the mountain range. We can observe that diminishing organic matter in soil, or more generally, overall soil quality leads to decreased biomass productivity. As a result, we can expect to see a reduction in animal/plant/any form of life diversity in the ecosystem<sup>[8]</sup>.

We also analysed the effect of varied precipitation on a more local scale to analyse the dynamics of the population of the Ponderosa Pine, a species of tree that is very commonly found in Sierra Nevada. We did this using a local interaction model, which is similar to the automaton model used in [Conoway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).
<p align="center">
  <img width="600" alt="Screenshot 2024-11-17 at 02 33 46" src="https://github.com/user-attachments/assets/a8c53c5b-d8ae-4d0a-8f13-7cdb65661a8c">
</p>


A final interesting thing we can observe in the long term is how different migratory paths might change as the landscape changes. We use an algorithm inspired by the <b>A* Pathfinding Algorithm</b>, which is an extention of Djaikstra's shortest path that uses a heuristic. By establishing a vector field using the DEM Model and by making the assumption that animals tend to take easier paths, one can then predict their movement and their paths of migration. 
<p align="center">
  <img width="543" alt="Screenshot 2024-11-17 at 02 33 46" src="https://github.com/user-attachments/assets/ddcab02c-a6aa-461f-b37a-2f7168e99a63">
</p>
We can apply the path finding algorithm to Ca(t) to visualise how these migratory paths will shift with time. 


From the above two images, we can see a clear difference between the two migration routes conducted in the present time and prediction in a thousand years. This is mainly caused by climate change which is causing shifts in temperature and precipitation patterns, affecting topography as we showed in the previous section. One recent study found that current sea surface temperature extremes driven by El Niño have intensified by around 10% compared to pre-1960 levels.[9] This builds on previous studies which predicted that the frequency of extreme El Niño events could double over the next century due to faster surface warming of the eastern Pacific Ocean brought on by global temperature rises.[10] The increase in the intensity of El Niño can result in more frequent and stronger summer storms which further erode the landscape and changes the topology. This can cause further changes in the migration routes due to changes in availability of certain vegetation and any new-formed physical barriers. 




by Afjal C, Arvind C, Tom A, Sahil B, Tianzong C, Connie C

[1]https://earth.jaxa.jp/en/data/index.html
[2]https://www.qgis.org
[3]https://www.sciencebase.gov/catalog/item/60356a96d34eb120311748e8
[4]https://snrs.ucmerced.edu/natural-history/climate
[5]Pomeroy, J., Gray, D., & Toth, B. (1998). "The role of snow accumulation in the Sierra Nevada snowpack." Journal of Hydrology. Sturm, M., & Liston, G. (2003). 
[6]"Snow mechanics: A review of simple models." Cold Regions Science and Technology.
[7]https://www.cambridge.org/core/services/aop-cambridge-core/content/view/1B4E44F8B47C1A39934475B264AF8F35/S0260305500263271a.pdf/rheological-measurements-of-the-viscoelastic-properties-of-snow.pdf
[8]Ecology of Soil Erosion in Ecosystems, David Pimentel* and Nadia Kounang, College of Agriculture and Life Sciences
[9]https://doi.org/10.1038/s43017-023-00427-8
[10]https://doi.org/10.1038/nclimate2100
