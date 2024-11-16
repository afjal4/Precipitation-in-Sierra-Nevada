# Rainfall-in-Sierrea-Nevada

A consequence of the increasingly turbulant global climate is that the Sierra Nevada Moutnains, located in Eastern California, have undergone significant topographical change. In this project, we will explore specifically the change attributed to the abnormal precipitational patterns, and how the ecology of the mountain range develops accordingly.

We start by creating a DEM (Digital Elevation Model) for the range...

We then forecast the precipitational patterns in Sierra Nevada from historic data as a scalar field...

We observe that the type of precipitation that falls on a point depends on the point's altitude ie. snow will fall more frequently atop the mountain than on the mountain foot. In terms of the precipitations effect on the topography, rain errodes rock by bombardment, and the flow of waterdisplaces soil; whereas snow errodes once it melts, with overall errosion less significant than that of rain. Altitude clearly affects the effect of errosion from a given precipitation.

Steepness also affects the intensity of errosion, more specifically from bombardment from rain. We find the normal vector field to the mountain DEM, and use that to find the angle of a point with the vertical, and then the cosine of the angle as a scalar field that damps the effect of bombardment on the errosion.
