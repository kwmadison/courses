% Put peak pairs into a histogram image

function [histogram] = createPeakHistogram(filename, height, width, rotation)
    ZERO_MARGIN = 10;

    peaks = round(readmatrix(filename));
    histogram = zeros(height, width);

    for peak = peaks'
        x = peak(1); y = peak(2);
        histogram(x, y) = histogram(x, y) + 1;
    end

    % gets rid of image margins, centroiding does badly there
    zeroMargin = zeros(height, width);
    zeroMargin(ZERO_MARGIN: end - ZERO_MARGIN, ZERO_MARGIN: end - ZERO_MARGIN) = 1;
    histogram = times(histogram, zeroMargin);

    if rotation ~= 0
        histogram = imrotate(histogram, rotation);
    end
end
