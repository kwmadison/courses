clear, clc, clf, hold on;

% ----- CONSTANTS & INITIAL CONDITIONS -----
m_cores = [1; 1];
n_stars = [1; 2];

r0_cores = [-2, 0, 0; 2, 0, 0];
v0_cores = [0, -1.5, 0; 0, 0.5, 0];

range_r_stars = [0.3, 0.6; 0.2, 0.8];
range_theta_stars = [pi/2, pi/2; pi/2, pi/2];
range_phi_stars = [0, 2 * pi; 0, 2 * pi];
range_va_stars = [pi/2, pi/2; pi/2, pi/2];

% ----- DISCRETIZATION -----
tmax = 6;
level = 8;

% ----- SIMULATION OPTIONS -----
save = true;
delay = 0;
padding = 4;
save_name = 'toomre.avi';

color_stars = ['b'; 'r'];
color_cores = [[9, 18, 110] / 255; [173, 3, 3] / 255];
size_core = 10;
size_star = 3;

% ----- INITIAL SETUP CALCULATIONS -----
nc = length(m_cores);
ns = sum(n_stars);
N = 2 ^ level + 1;
ts = linspace(0, tmax, N);
dt = ts(2) - ts(1);
limits = [min(r0_cores, [], 1) - padding; max(r0_cores, [], 1) + padding]';

% uniform random sampling of star positions and velocities
r0_stars = zeros(0, 3);
v0_stars = zeros(0, 3);

for i = 1: nc
   r = randsInRange(range_r_stars(i, :), n_stars(i));
   etheta = pi/2 - randsInRange(range_theta_stars(i, :), n_stars(i));
   phi = randsInRange(range_phi_stars(i, :), n_stars(i));
   [x, y, z] = sph2cart(phi, etheta, r);
   r0_stars = cat(1, r0_stars, [x, y, z] + r0_cores(i, :));

   va = randsInRange(range_va_stars(i, :), n_stars(i));
   vhat = [-sin(va) .* sin(phi) - cos(va) .* sin(etheta) .* cos(phi), ...
            sin(va) .* cos(phi) - cos(va) .* sin(etheta) .* sin(phi), ...
            cos(va) .* cos(etheta)];
   v0_stars = cat(1, v0_stars, sqrt(m_cores(i) ./ r) .* vhat + v0_cores(i, :));
end

rc = zeros(nc, 3, N);
rs = zeros(ns, 3, N);
rc(:, :, 1) = r0_cores;
rs(:, :, 1) = r0_stars;
rc(:, :, 2) = rc(:, :, 1) + dt * v0_cores + 0.5 * dt ^ 2 * accelCores(m_cores, rc(:, :, 1));
rs(:, :, 2) = rs(:, :, 1) + dt * v0_stars + 0.5 * dt ^ 2 * accelStars(m_cores, rc(:, :, 1), rs(:, :, 1));

% ----- CONVERGENCE TESTING -----
[~, x0] = trackToomre(rc, rs, m_cores, tmax, level);
[~, x1] = trackToomre(rc, rs, m_cores, tmax, level - 1);
[~, x2] = trackToomre(rc, rs, m_cores, tmax, level - 2);
[t3, x3] = trackToomre(rc, rs, m_cores, tmax, level - 3);
dx1 = 16 * (x0(1: 8: end) - x1(1: 4: end));
dx2 = 4 * (x1(1: 4: end) - x2(1: 2: end));
dx3 = x2(1: 2: end) - x3;

plot(t3, dx1, '-.k');
plot(t3, dx2, '-.b');
plot(t3, dx3, '-.r');
xlabel('time');
ylabel('scaled \Deltax between adjacent levels');
pause(2);

% ----- animation and video -----
if save
   writer = VideoWriter(save_name);
   open(writer);
end

for i = 2: N
   if save
        clf, hold on, box on, axis equal, axis manual;
        xlim(limits(1, :));
        ylim(limits(2, :));
        zlim(limits(3, :));
        title(sprintf('Step: %d  Time: %.2f', round(ts(i) / dt), ts(i)));

        plot(rs(:, 1, i), rs(:, 2, i), '.', ...
            'MarkerSize', size_star, 'MarkerEdgeColor', color_stars);
        plot(rc(:, 1, i), rc(:, 2, i), '.', 'MarkerSize', size_core, ...
            'MarkerEdgeColor', color_cores);
        xlabel('x');
        ylabel('y');
      
        drawnow;

        if save
            writeVideo(writer, getframe(gcf));
        end
        pause(delay);
   end
   
   [rc, rs] = updateToomre(i, rc, rs, m_cores, dt);
end

if save
   close(writer);
   fprintf('Saved to video file: %s\n', save_name);
end
close all;