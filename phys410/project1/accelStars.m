function a = accelStars(mc, rc, rs)
% Calculate the acceleration of stars given core mass and positions, and
% star positions.
    a = zeros(size(rs, 1), 3);
    for i = 1: length(mc)
        delta_r = rc(i) - rs;
        a = a + mc(i) .* delta_r ./ vecnorm(delta_r, 2, 2) .^ 3;
    end
end