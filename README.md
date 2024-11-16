# Precipitation-in-Sierrea-Nevada

A consequence of the increasingly turbulant global climate is that the Sierra Nevada Moutnains, located in Eastern California, have undergone significant topographical change. In this project, we will explore specifically the change attributed to the abnormal precipitational patterns, and how the ecology of the mountain range develops accordingly.
> "...global climate models don’t capture the fine-scale topography and regional characteristics that we know shape our weather and climate around us." (Niel Berg), on the tumultuous topography of Sierra Nevada

We start by creating a DEM (Digital Elevation Model) for the mountain range. We used data from the JAXA global sattelite imaging database<sup>[1]</sup> and collated it using QGIS Mapping Software<sup>[2]</sup>.

<p align="center">
  <img src="https://github.com/user-attachments/assets/fe508619-f97e-4a34-bd10-70871ee8eca9" />
</p>

We then forecast the precipitational patterns in Sierra Nevada from historic data across 400 regions within the DEM, represented by a 20x20 Matrix := P(y), where y is the precipitation by year. 

We applied ARIMA to the data in each of these regions to forecast the precipitation in each region individually, so the t parameter within P(t) grants varied precipitation P based on the ARIMA forecast. Using this, we can find values for P(y) for y in the future. We now define P(t) := the matrix P, t years after today (in 2024).

The DEM Model can be represented as a 7200x7200 Matrix := Ca (California). Ca(0) := The initial state of Sierra Nevada, and the state of Sierra Nevada after n years is Ca(n) := P(n) ∘ P(n-1) ∘ ... ∘ P(1) ∘ P(0) ∘ Ca(0). We now need to define the P ∘ Ca, or the effect of a year of Precipitation on California. (P<sub>1</sub> ∘ P<sub>2</sub> = P<sub>1</sub> + P<sub>2</sub> which is summing the rainfall from 2 years)

Steepness also affects the intensity of errosion, more specifically from bombardment from rain. We find the a vector field to the mountain DEM, and use that to find the angle of a point with the horizontal, and then the cosine of the angle as a scalar field that damps the effect of bombardment on the errosion. Essentially, steeper hills errode less to bombardment as the droplet has less of a force component into the ground.

<p align="center">
  <img src="https://github.com/user-attachments/assets/2104dd34-6c93-4e2d-8d99-fda76790484b" />
</p>

Now, by researching the geology of Sierra Nevada, we can identify specifically how the precipitation and steepness of the hill affect year on year errosion (defining P ∘ Ca).

by Afjal C, Arvind, Tom, Sahil B, Tianzong C, Connie
[1]https://earth.jaxa.jp/en/data/index.html
[2]https://www.qgis.org
