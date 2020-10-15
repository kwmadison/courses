% Find cosine squared for a square image across a range of radii. Calculates
% about the center of image. !Only calculates up until the smallest dimension.!

function [array, weightedMean] = calcCosSquared(image, rmin, rmax)
[height, width] = size(image);
radii = rmin: rmax;

[x, y] = meshgrid((1: width) - width / 2, (1: height) - height / 2);
[theta, r] = cart2pol(x, y);
r = round(r);

thetaDistrib = [];
fDistrib = cell(size(radii));
array = [];

for i = 1: length(radii)
    mask1 = (r == radii(i));
    fDistrib{i} = image(mask1);
    thetaDistrib = theta(mask1);
    array(1, i) = sum(fDistrib{i} ./ sum(fDistrib{i}) .* cos(thetaDistrib) .^ 2);
    thetaDistrib = [];
end

for i = 1: length(radii)
    weight(i) = sum(fDistrib{i});
end
weightedMean = sum(weight .* array) / sum(weight);
end
