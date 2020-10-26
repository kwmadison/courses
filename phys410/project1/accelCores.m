function a = accelCores(mc, rc)
% Calculate the acceleration of cores given their mass and positions.
    nc = size(mc, 1);
    a = zeros(nc, 3);
    for i = 1: nc
        for j = 1: nc
            if j ~= i
                delta_r = rc(j, :) - rc(i, :);
                a(i, :) = a(i, :) + mc(j) .* delta_r / norm(delta_r) ^ 3;
            end
        end
    end
end