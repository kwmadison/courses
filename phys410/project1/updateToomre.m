function [rc, vc, rs, vs] = updateToomre(rc, vc, rs, vs, mc, dt)
% Perform iteration step by updating core and star positions and velocities
    nc = size(rc, 1);
    rc = rc + vc .* dt;    
    for i = 1: nc
        a = zeros(1, 3);
        for j = 1: nc
            if j ~= i
                delta_r = (rc(j, :) - rc(i, :));
                a = a + mc(j) .* delta_r / norm(delta_r) ^ 3;
            end
        end
        vc(i, :) = vc(i, :) + a .* dt;
    end
    
    for i = 1: nc
        rs{1, i} = rs{1, i} + vs{1, i} .* dt;
        a = zeros(size(rs{1, i}));
        for j = 1: nc
            delta_r = (rc(j, :) - rs{1, i});
            a = a + mc(j) .* delta_r ./ vecnorm(delta_r, 2, 2) .^ 3;
        end
        vs{1, i} = vs{1, i} + a .* dt;
    end
end