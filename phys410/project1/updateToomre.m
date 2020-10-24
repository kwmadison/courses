function [rc, rs] = updateToomre(rc, rs, mc, dt)
% Perform iteration step by updating core and star positions.
    nc = size(rc{1}, 1);
    rc{3} = 2 * rc{2} + dt^2 * accelCores(mc, rc{2}) - rc{1};
    for i = 1: nc
        rs{3}{i} = 2 * rs{2}{i} + dt^2 * accelStars(mc, rc{2}, rs{2}{i}) - rs{1}{i};
    end
    
    rc{1} = rc{2};
    rc{2} = rc{3};
    rs{1} = rs{2};
    rs{2} = rs{3};
end