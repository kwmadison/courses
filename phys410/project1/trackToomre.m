function [ts, x_hist] = trackToomre(rc, rs, m_cores, tmax, level)
% Track the x position of the first particle throughout a full simulation
% for the given initial conditions and parameters.
    N = 2 ^ level + 1;
    ts = linspace(0, tmax, N);
    dt = ts(2) - ts(1);
    
    x_hist = zeros(1, N);
    x_hist(1) = rs(1, 1, 1);
    
    for i = 2: N
        x_hist(i) = rs(1, 1, i);
        [rc, rs] = updateToomre(i, rc, rs, m_cores, dt);
    end
end