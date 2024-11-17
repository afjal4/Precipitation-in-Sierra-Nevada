clc
clear

elev = readgeoraster("final_map.tif");
elev1 = elev(1:100,1:100);
figure
imagesc(elev1)


[dx,dy] = gradient(elev1);

figure
quiver(1:100,flip(1:100),dx,dy);

angle = cos(atan(sqrt(dx.^2+dy.^2)./30));


figure
imagesc(angle);
colormap("jet")
clim([0.78 1])
axis off; 
colorbar;

min(angle(:))