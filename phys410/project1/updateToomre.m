function [rc, rs] = updateToomre(i, rc, rs, m_cores, dt)
% Perform iteration step by updating core and star positions.
    rc(:, :, i + 1) = 2 * rc(:, :, i)  - rc(:, :, i - 1) + accelCores(m_cores, rc(:, :, i)) * dt ^ 2;
    rs(:, :, i + 1) = 2 * rs(:, :, i) - rs(:, :, i - 1) + accelStars(m_cores, rc(:, :, i), rs(:, :, i)) * dt ^ 2;
end
