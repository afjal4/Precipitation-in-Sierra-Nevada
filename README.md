# Precipitation-in-Sierrea-Nevada

A consequence of the increasingly turbulant global climate is that the Sierra Nevada Moutnains, located in Eastern California, have undergone significant topographical change. In this project, we will explore specifically the change attributed to the abnormal precipitational patterns, and how the ecology of the mountain range develops accordingly.
> "global climate models don’t capture the fine-scale topography and regional characteristics that we know shape our weather and climate around us." (Niel Berg)

We start by creating a DEM (Digital Elevation Model) for the range. We used data from the JAXA global sattelite imaging database<sup>[1]</sup> and collated it using QGIS Mapping Software<sup>[2]</sup>.
![actual_photo](https://github.com/user-attachments/assets/fe508619-f97e-4a34-bd10-70871ee8eca9)

We then forecast the precipitational patterns in Sierra Nevada from historic data across 400 regions within the DEM, represented by a 20x20 Matrix := P(t). We applied ARIMA to the data in each of these regions to forecast the precipitation in each region individually, so the t parameter within P(t) grants varied precipitation P based on the ARIMA forecast. 

The DEM Model can be represented as a 7200x7200 Matrix := Ca (California). Ca(0) = The initial state of Sierra Nevada, and the state of Sierra Nevada after n years is Ca(n) := P(n) ∘ P(n-1) ∘ ... ∘ P(1) ∘ Ca. We now need to define the P ∘ Ca, or the effect of a year of Precipitation on California.

We observe that the type of precipitation that falls on a point depends on the point's altitude ie. snow will fall more frequently atop the mountain than on the mountain foot. In terms of the precipitations effect on the topography, rain errodes rock by bombardment, and the flow of waterdisplaces soil; whereas snow errodes once it melts, with overall errosion less significant than that of rain. Altitude clearly affects the effect of errosion from a given precipitation.

Steepness also affects the intensity of errosion, more specifically from bombardment from rain. We find the normal vector field to the mountain DEM, and use that to find the angle of a point with the vertical, and then the cosine of the angle as a scalar field that damps the effect of bombardment on the errosion.

[1]https://earth.jaxa.jp/en/data/index.html
[2]https://www.qgis.org
