clear, clc
hold off

DATA = 'thesis_assets/data';
BASENAME = '20200902_NO_test*0.0.dat';
DELAYS = [10, 20, 30, 40, 50, 60, 70];
i = 1;
WIDTH = 960; HEIGHT = 600;
ROTATE = 0;
CENTER = [300, 520];  % [HEIGHT / 2, WIDTH / 2];
RMIN = 50; RMAX = 200;

image = zeros(HEIGHT, WIDTH);
files = dir(fullfile(DATA, BASENAME));

for file = files'    
    filename = fullfile(file.folder, file.name);
    image = createPeakHistogram(filename, HEIGHT, WIDTH, ROTATE);

    if CENTER(1) > HEIGHT / 2
        image = image(2 * CENTER(1) - HEIGHT: end, :);
    elseif CENTER(1) < HEIGHT / 2
        image = image(1: 2 * CENTER(1), :);
    end

    if CENTER(2) > WIDTH / 2
        image = image(:, 2 * CENTER(2) - WIDTH: end);
    elseif CENTER(2) < WIDTH / 2
        image = image(:, 1: 2 * CENTER(2), :);
    end

    [cosSquared, average] = calcCosSquared(image, RMIN, RMAX);
    
    imagesc(image)
    pbaspect([WIDTH / HEIGHT, 1, 1])
    title(['delay = ', num2str(DELAYS(i)),...
        'ps, cos^2(\theta) = ', num2str(average)])
    pause(1)
    i = i + 1;
end
