# The Long Term Effects of the Varying Precipitation in Sierra Nevada

A consequence of the increasingly turbulent global climate is that the Sierra Nevada Mountain Region (Eastern California) has undergone significant topographical change. In this project, we explore the long term topographical changes attributed to the ever-changing precipitation patterns, and how the ecology of the mountain range develops accordingly. We specifically analyse the <b>long term</b> effects of the varied rainfall in this project, focusing especially on annual (or even decade-wide) fluctuations, as opposed to smaller seasonal changes.

> "...global climate models don’t capture the fine-scale topography and regional characteristics that we know shape our weather and climate around us." (Niel Berg), on the tumultuous topography of Sierra Nevada 

We start by creating a <b>DEM (Digital Elevation Model)</b> for the mountain range. We used data from the JAXA global satellite imaging database<sup>[1]</sup> and collated it using QGIS Mapping Software<sup>[2]</sup>. This contains 7200x7200 30mx30m points.

<p align="center">
  <img src="https://github.com/user-attachments/assets/fe508619-f97e-4a34-bd10-70871ee8eca9"/></p>
</p>
<p align="center">
Map of Sierra Nevada from the JAXA global satellite
</p>

We then forecast the precipitation patterns in Sierra Nevada from historic data across 400 regions within the DEM<sup>[2.1]</sup>, represented by a 20x20 Matrix := P(y), where y is the precipitation by year. This <b>lower resolution is much more appropriate</b> for this context as it is much more viable to store 2000 20x20 matrices (3MB) as opposed to 2000 7200x7200 matrices (392GB) when we proceed with using these matrices for future forecasts. 
![output](https://github.com/user-attachments/assets/d05bb357-1cc3-45a8-919e-edbaf348fdc2)
Historical precipitation data in Sierra Nevada (1924 - 2024)

We applied a <b>random forest/ML (machine learning) based algorithm</b><sup>[2.2]</sup> to the data in each of these regions to forecast a precipitation matrix that fully utilises all 400 time series for each subregion, so that the y parameter within P(y) grants varied precipitation P based on the Random Forest forecast. Initially running this algorithm using a pure random forest approach led the P matrices to converge towards uniformity (ie. λJ). We modelled the noise in this process through the addition of a <b>gaussian stochastic parameter</b>, which let P(t) maintain desirable similarities with the historic data (like being affected by mountain ridges and shadows) whilst still demonstrating clear development (that incorporated spatial growth against spontaneous growth). This is also partially because a forecast of the temperature := T is also used determine P, in order to represent how <b>more water is in the system</b>; eastern winds from the Pacific<sup>[3]</sup> grant a greater net income of water into the mountain range - as well as water melting from ice - thus freeing it from storage. We can now find values for P(y) for y in the future. We now define P(t) := the matrix P, t years after today (i.e. as of 2024). 

The DEM Model can be represented as a 7200x7200 Matrix := Ca (California). Ca(0) := The initial state of Sierra Nevada, and the state of Sierra Nevada after n years is Ca(n) := P(n) ∘ C(n-1), (or Ca(n) = P(n) ∘ P(n-1) ∘ ... ∘ P(1) ∘ P(0) ∘ Ca(0)). We now need to define <b>P ∘ Ca</b>, or the effect of a year of precipitation on the erosion of Sierra Nevada's terrain. (P<sub>1</sub> ∘ P<sub>2</sub> = P<sub>1</sub> + P<sub>2</sub> which is summing the rainfall from 2 years)

Through the further exploration of the geology and topography of Sierra Nevada's terrain, we can specifically identify how the precipitation affects annual erosion (defining P ∘ Ca). We model erosion here through 2 primary mechanisms<sup>[4.1][4.2]</sup>; erosion due to bombardment from precipitation and through the flow of water down high terrain features, like mountains. 

$$
\Delta h = \Delta h_b + \Delta h_f
$$

We first model Δh<sub>b</sub>:</br>
A notable parameter that affects the intensity of bombardment due to precipitation is the <b>slope</b>. We find a vector field ∇ Ca to the mountain range DEM matrix, which we use to find the angle to the horizontal, from which we infer that the effect of bombardment on the erosion is damped by a factor of the cosine of the angle as a scalar field. Essentially, steeper hills erode less from bombardment due to precipitation as the droplet has a smaller force component perpendicular to the ground.

<p align="center">
  <img src="https://github.com/user-attachments/assets/2104dd34-6c93-4e2d-8d99-fda76790484b" />
  California Matrix Ca and ∇ Ca  
  <img src="https://github.com/user-attachments/assets/2cc7c551-04b8-4ff2-8f90-c834261c76b5" />
  Scalar field of cosθ for each θ subtended by the vertical and v ∈ ∇Ca
</p>

Different geological factors also impact this erosion; namely the rock density ρ<sub>r</sub> and its corresponding rate of detachability D<sub>r</sub>, which is a measure of its willingness to 'erode' or detach itself from the surface on which it rests <sup> [4.3] </sup>. The rate of detachability is the product of its porosity ϕ, saturation s, and erosion coefficient k. We decided find the average porosity and saturation values of rocks sampled uniformly throughout the mountain range<sup>[4]</sup> to arrive at ϕ = 0.0947 and s = 0.487. As for our value of k, we decided to use a value of 0.75(kg)(yr)/m², based on literature values from previous papers on rocks of similar composition and porosities <sup> [4.1][4.2] </sup>. We note that these values are similar value to that of granite <sup> [4.4] </sup>, which agrees with literature, since Sierra Nevada was formed volcanically <sup> [4.5] </sup> (and is rich in granite and granitic material), and granite is igneous.

$$
\Delta h_b = \frac{k \phi s \cos\theta}{\rho_r}P
$$ 

We now model Δh<sub>f</sub>:</br>
An assumption we make when modelling erosion due to water downflow is that the granite impact on granite is negligible, which comes as an assumption that the granite is smooth, which exists to simplify our model. As a result, our model instead takes into account the downflow of snow due to precipitation, where snow is dragged away by rainfall. We can consider the snow line - which is the lower topographic limit of permanent snow cover on high terrain features <sup> [4.6] </sup>- to work out where snow can fall. 

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

k<sup>[5,6,7]</sup> = 0.0748 (the value of which was determined through the considerations of the average density and viscosity of loosely packed snow)

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
One obvious ecological feature that can be observed from this data is the effect on the physical elevations/topography of the mountain range. We can observe that diminishing organic matter in soil, or more generally, overall soil quality leads to decreased biomass productivity. As a result, we can expect to see a reduction in animal/plant/any form of life diversity in the ecosystem. Another effect that may not appear as obvious occurs as a result of plant species (Tilman and Downing 1994). As plant specie count dropped to 5 from 25, local grassland was less resistant to drought and the total amount of biomass had dropped by more than fourfold<sup>[8]</sup>. 

![image](https://github.com/user-attachments/assets/001bc187-ebfa-4284-8431-d357cd93e213)
---
We also analysed the effect of varied precipitation on a more local scale to analyse the dynamics of the population of the Ponderosa Pine, a species of tree that is very commonly found in Sierra Nevada. We did this using a local interaction model, which is similar to the automaton model used in [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life). 

The heart of this code is an implementation of the Mixture Density Network (MDN). MDNs are a class of neural networks designed to predict a mixture of probability distributions [14]. This model is particularly suitable for predicting outputs that are probabilistic and lack sufficient train data. Following the implementation in [15], the MDNDecisionMaker class is a neural network that is designed to predict both the mean and covariance parameters of a Gaussian distribution. This is achieved through three key components. Feed-forward Network: The first part of the network is a series of fully connected layers interspersed with activation functions (SiLU) and dropout layers. The purpose of this network is to learn the general structure of the data and generate a hidden representation of the input features. Batch normalisation is applied to normalise the input and hidden layers, which improves our training speed and stability. After the feed-forward network, the next step is to predict the means of the output distribution. The mean network takes the hidden representation from the previous layers and uses a fully connected network to output the predicted means. Finally, Cholesky decomposition: For the covariance matrix, the model predicts the lower triangular elements of the Cholesky decomposition (i.e., the matrix that is used to construct the covariance matrix). The final output of the network consists of the predicted mean vector and the Cholesky decomposition of the covariance matrix. The $\verb|forward()|$ function of the class returns these outputs, with an option to return the covariance matrix if requested. This output forms the basis for modeling the uncertainty in the precipitation data looking forward.

<p align="center">
  <img width="600" alt="Screenshot 2024-11-17 at 02 33 46" src="https://github.com/user-attachments/assets/a8c53c5b-d8ae-4d0a-8f13-7cdb65661a8c">
</p>

<p align="center">
  <img width="600" alt="Screenshot 2024-11-17 at 02 33 46" src="https://github.com/user-attachments/assets/12c7d003-1044-4749-8549-3c471a43c2ee">
</p>

<p align="center">
  <img width="350" alt="Screenshot 2024-11-17 at 02 33 46" src="https://github.com/user-attachments/assets/fb2fed92-b135-4c35-b780-b17ac217c776">
</p>

-----
A final interesting thing we can observe in the long term is how different migratory paths might change as the landscape changes. We use an algorithm inspired by the <b>A* Pathfinding Algorithm</b>, which is an extension of Djaikstra's shortest path that uses a heuristic. By establishing a vector field using the DEM Model and by making the assumption that animals tend to take easier paths, one can then predict their movement and their paths of migration. 
<p align="center">
  <img width="543" alt="Screenshot 2024-11-17 at 02 33 46" src="https://github.com/user-attachments/assets/ddcab02c-a6aa-461f-b37a-2f7168e99a63">
</p>
We can apply the path finding algorithm to Ca(t) to visualise how these migratory paths will shift with time. 
<p align="center">
  <img width="543" alt="Screenshot 2024-11-17 at 02 33 46" src="https://github.com/user-attachments/assets/bc0aa14a-2919-482d-8538-be68caae4b63">
  Path after 50 years
</p>
When 50 years passes, the migratory path looks roughly similar. This is as errosion is typically a slow process<sup>[4.1]</sup> so 50 years is unlikely to see any/much change.
<p align="center">
  <img width="543" alt="Screenshot 2024-11-17 at 02 33 46" src="https://github.com/user-attachments/assets/55a4fe0b-bc8a-48de-9d00-22298e0abf02">
  Path after 1000 years
</p>

We can see a drastic change in the migratory path over this much longer period of time. One recent study found that current sea surface temperature extremes driven by El Niño have intensified by around 10% compared to pre-1960 levels.[9] This builds on previous studies which predicted that the frequency of extreme El Niño events could double over the next century due to faster surface warming of the eastern Pacific Ocean brought on by global temperature rises.[10] The increase in the intensity of El Niño can result in more frequent and stronger summer storms which further erode the landscape and changes the topology. This can cause further changes in the migration routes due to changes in the availability of certain vegetation and any newly formed physical barriers. 

Furthermore, animals changing migration routes can lead to disruption of nutrient cycling, alter habitat availability, and impact pollination and seed dispersal. Many migratory species contribute significantly to nutrient cycling. For example, large herbivores (e.g.: mule deer) that migrate across landscapes help cycle nutrients through their droppings, enriching soil fertility. If these species change their routes, the flow of nutrients could be altered, leading to shifts in soil health, plant productivity, and the overall resilience of ecosystems.[11] 

Many species play key roles in pollination and seed dispersal, both of which are critical for maintaining plant diversity and ecosystem stability. For example, migratory birds and insects often transport pollen or seeds across vast distances. If their migration routes are disrupted, plants may face reduced pollination or struggle to spread their seeds to suitable environments, leading to changes in plant community composition and potentially the loss of certain species[12].

by Afjal C, Arvind C, Tom A, Sahil B, Tianzong C, Connie C

[1] Access Jaxa Satellite Data (no date) JAXA Earth-graphy / Space Technology Directorate I. Available at: https://earth.jaxa.jp/en/data/index.html (Accessed: 17 November 2024). 
[2] Spatial without compromise · Qgis Web Site (no date) · QGIS Web Site. Available at: https://www.qgis.org/ (Accessed: 17 November 2024). 
[2.1] Time Series Values for Individual Locations (no date) Prism Climate Group at Oregon State University. Available at: https://prism.oregonstate.edu/explorer/ (Accessed: 17 November 2024). 
[2.2 AnalytixLabs (2023) Random Forest regression - how it helps in predictive analytics?, Medium. Available at: https://medium.com/@byanalytixlabs/random-forest-regression-how-it-helps-in-predictive-analytics-01c31897c1d4 (Accessed: 17 November 2024). 
[3] Density and Magnetic Properties of Selected Rock Samples from the Western U.S. and Alaska (2021) ScienceBase. Available at: https://www.sciencebase.gov/catalog/item/60356a96d34eb120311748e8 (Accessed: 17 November 2024). 
[4] Climate (no date) Yosemite Field Station. Available at: https://snrs.ucmerced.edu/natural-history/climate (Accessed: 17 November 2024). 
[4.1] Selby, M.J. (1993): Hillslope materials and processes. 
[4.2] Montgomery, D.R., and Dietrich, W.E. (1992): Channel initiation studies that provide context for erosion processes in granitic landscapes. 
[4.3] Montgomery DR, Dietrich WE: Channel initiation and the problem of landscape scale
[4.4] Gao, Lan, and Guo: Pore Structural Features of Granite under Different Temperatures
[5] Pomeroy, J., Gray, D., & Toth, B. (1998). "The role of snow accumulation in the Sierra Nevada snowpack." Journal of Hydrology. Sturm, M., & Liston, G. (2003). 
[6] "Snow mechanics: A review of simple models." Cold Regions Science and Technology.
[7]Kry, P.R. (2017) The relationship between the visco-elastic and structural properties of fine-grained snow: Journal of Glaciology, Cambridge Core. Available at: https://www.cambridge.org/core/journals/journal-of-glaciology/article/relationship-between-the-viscoelastic-and-structural-properties-of-finegrained-snow/90206CDC1A6FCA880E8A38FD674CCCB2 (Accessed: 17 November 2024). 
[8] Ecology of Soil Erosion in Ecosystems, David Pimentel* and Nadia Kounang, College of Agriculture and Life Sciences
[9] Cai, W. et al. (2023) Anthropogenic impacts on twentieth-century ENSO variability changes, Nature News. Available at: https://www.nature.com/articles/s43017-023-00427-8 (Accessed: 17 November 2024). 
[10] Increasing frequency of extreme El Nino events due to greenhouse warming | request PDF. Available at: https://www.researchgate.net/publication/259868282_Increasing_Frequency_of_Extreme_El_Nino_Events_due_to_Greenhouse_Warming (Accessed: 17 November 2024). 
[11] Wilmshurst, J. M., et al. (2004). "Migration of large herbivores and its effects on ecosystem function." Nature, 429, 130-132.
[12] Bascompte, J., & Jordano, P. (2007). "Plant-animal mutualistic networks: the architecture of biodiversity." Annual Review of Ecology, Evolution, and Systematics, 38, 567-593.
[13] Sáez-Cano, G. et al. (2021) Modelling tree growth in monospecific forests from Forest Inventory Data, MDPI. Available at: https://www.mdpi.com/1999-4907/12/6/753 (Accessed: 17 November 2024). 
[14] https://publications.aston.ac.uk/id/eprint/373/1/NCRG_94_004.pdf
[15] https://github.com/dusenberrymw/mixture-density-networks/blob/master/mixture_density_networks.ipynb
[16] Press, William H.; Saul A. Teukolsky; William T. Vetterling; Brian P. Flannery (1992). Numerical Recipes in C: The Art of Scientific Computing (second ed.). Cambridge University England EPress. p. 994. ISBN 0-521-43108-5. Retrieved 2009-01-28.


