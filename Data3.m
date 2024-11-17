clc;
clear;

% Load and preprocess data
data = readtable('data.csv');
ppt = reshape(data.ppt, [21, 21, 100]);
temp = reshape(data.temp, [21, 21, 100]);
ppt = ppt(1:20, 1:20, :);
temp = temp(1:20, 1:20, :);

% Reshape for training
pptTrain = reshape(ppt, [400, 100]);
tempTrain = reshape(temp, [400, 100]);

% Generate features (rolling window)
windowSize = 5; % 5-year rolling window
[X, Y] = meshgrid(1:20, 1:20);
grid = [X(:), Y(:)];
past = 1924:2023;
future = 2024:2073;
totalYears = [past, future];

% Add rolling window features
featuresP = [];
featuresT = [];
labelsP = [];
labelsT = [];
for i = windowSize:length(past)
    yearWindow = past(i - windowSize + 1:i);
    yearIndex = ismember(past, yearWindow);
    pptWindow = pptTrain(:, yearIndex);
    tempWindow = tempTrain(:, yearIndex);
    
    rollingFeaturesP = [reshape(repmat(yearWindow, 400, 1), [], 1), repmat(grid, windowSize, 1)];
    rollingFeaturesT = rollingFeaturesP; % Separate features for temperature and precipitation
    
    featuresP = [featuresP; rollingFeaturesP];
    featuresT = [featuresT; rollingFeaturesT];
    
    labelsP = [labelsP; pptWindow(:)];
    labelsT = [labelsT; tempWindow(:)];
end

% Train-test split
trainP = featuresP(:, 1) <= 2003;
trainT = featuresT(:, 1) <= 2003;

xTrainP = featuresP(trainP, :);
xTrainT = featuresT(trainT, :);
yPTrain = labelsP(trainP);
yTTrain = labelsT(trainT);

% Train Random Forest Models
Pmodel = TreeBagger(100, xTrainP, yPTrain, 'Method', 'regression', 'MinLeafSize', 2, 'OOBPrediction', 'on');
Tmodel = TreeBagger(100, xTrainT, yTTrain, 'Method', 'regression', 'MinLeafSize', 2, 'OOBPrediction', 'on');

% Forecasting
tempForecast = zeros(20, 20, length(future));
pptForecast = zeros(20, 20, length(future));

% Adjust noise parameters
pptStd = std(pptTrain, 0, 2) * 0.5; % Reduce noise level for precipitation
tempStd = std(tempTrain, 0, 2) * 0.25; % Ensure spatial variations in temperature

% Iterative forecasting
for i = 1:length(future)
    year = future(i);
    yearFeaturesP = [repmat(year, 400, 1), grid];
    yearFeaturesT = [repmat(year, 400, 1), grid];
    
    % Random Forest predictions
    pptPred = predict(Pmodel, yearFeaturesP);
    tempPred = predict(Tmodel, yearFeaturesT);
    
    % Add Gaussian noise
    pptPred = max(0, pptPred + randn(size(pptPred)) .* pptStd); % Ensure non-negative precipitation
    tempPred = tempPred + randn(size(tempPred)) .* tempStd; % Add temperature variability
    
    % Save forecasts
    pptForecast(:, :, i) = reshape(pptPred, [20, 20]);
    tempForecast(:, :, i) = reshape(tempPred, [20, 20]);
end

% Combine historical and forecasted data
pptTotal = cat(3, ppt, pptForecast);
tempTotal = cat(3, temp, tempForecast);

% Display output
disp('Forecasting complete. Data combined into total dataset.');

% Generate GIFs
filenameP = 'precipitation_forecast.gif';
filenameT = 'temperature_forecast.gif';
%% 

for t = 1:size(pptTotal, 3)
    % Precipitation GIF
    imagesc(pptTotal(:, :, t));
    colormap('jet');
    clim([0, max(pptTotal(:))]);
    colorbar;
    axis off;
    title(['Precipitation, Year: ', num2str(1924 + t - 1)]);
    frame = getframe(gcf);
    [A, map] = rgb2ind(frame.cdata, 256);
    if t == 1
        imwrite(A, map, filenameP, 'gif', 'LoopCount', inf, 'DelayTime', 0.1);
    else
        imwrite(A, map, filenameP, 'gif', 'WriteMode', 'append', 'DelayTime', 0.1);
    end
    
   
end
