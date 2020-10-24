clear, clc, clf;

% ----- problem constants -----
n_cores = 2;
m_cores = [1, 1];
n_stars = [0, 1];
range_r_stars = [0.3, 1; 0.2, 0.8];
range_theta_stars = [pi/2, pi/2; pi/2, pi/2];
range_phi_stars = [0, 2 * pi; 0, 2 * pi];
range_va_stars = [pi/2, pi/2; pi/2, pi/2];

% ----- initial conditions -----
r0_cores = [-1, 0, 0; 1, 0, 0];
v0_cores = [0, -1.5, 0; 0, 0.5, 0];
r0_stars = cell(1, n_cores);
v0_stars = cell(1, n_cores);

% uniform random sampling of star positions and velocities
for i = 1: n_cores
    r = randsInRange(range_r_stars(i, :), n_stars(i));
    etheta = pi/2 - randsInRange(range_theta_stars(i, :), n_stars(i));
    phi = randsInRange(range_phi_stars(i, :), n_stars(i));
    [x, y, z] = sph2cart(phi, etheta, r);
    r0_stars(1, i) = {[x, y, z] + r0_cores(i, :)};
    
    va = randsInRange(range_va_stars(i, :), n_stars(i));
    vhat = [-sin(va) .* sin(phi) - cos(va) .* sin(etheta) .* cos(phi), ...
             sin(va) .* cos(phi) - cos(va) .* sin(etheta) .* sin(phi), ...
             cos(va) .* cos(etheta)];
    v0_stars(1, i) = {sqrt(m_cores(i) ./ r) .* vhat + v0_cores(i, :)};
end

% ----- discretization constants -----
tmax = 6;
level = 8;
ts = linspace(0, tmax, 2^level + 1);
dt = ts(2) - ts(1);

% ----- options -----
show_save = true;
delay = 0;
padding = 4;
limits = [min(r0_cores, [], 1) - padding; max(r0_cores, [], 1) + padding]';
save_fps = 25;
save_name = 'toomre.avi';

color_stars = ['b', 'r'];
color_cores = [[9, 18, 110] / 255; [173, 3, 3] / 255];
size_core = 10;
size_star = 3;

% ----- iteration setup -----
rc = cell(1, 3);
rs = cell(1, 3);
rc{1} = r0_cores;
rs{1} = r0_stars;
rc{2} = rc{1} + dt * v0_cores + 0.5 * dt^2 * accelCores(m_cores, rc{1});
for i = 1: n_cores
    rs{2}{i} = rs{1}{i} + dt * v0_stars{i} + 0.5 * dt^2 * accelStars(m_cores, rc{1}, rs{1}{i});
end

% ----- convergence testing -----
[~, x0] = trackToomre(rc, rs, m_cores, tmax, level);
[~, x1] = trackToomre(rc, rs, m_cores, tmax, level - 1);
[~, x2] = trackToomre(rc, rs, m_cores, tmax, level - 2);
[t3, x3] = trackToomre(rc, rs, m_cores, tmax, level - 3);
dx1 = 16 * (x0(1: 8: end) - x1(1: 4: end));
dx2 = 4 * (x1(1: 4: end) - x2(1: 2: end));
dx3 = x2(1: 2: end) - x3;

clf, hold on;
% plot(t3, dx1, '-.k');
% plot(t3, dx2, '-.b');
% plot(t3, dx3, '-.r');
plot(t3, x0(1: 8: end), '-.k');
plot(t3, x1(1: 4: end), '-.b');
plot(t3, x2(1: 2: end), '-.r');
plot(t3, x3, '-.m');
xlabel('time');
ylabel('scaled \Deltax between adjacent levels');
pause(3);
stop

% ----- animation and video -----
if show_save
   writer = VideoWriter(save_name);
   open(writer);
end

for t = ts(1: end - 1)
   if show_save
        clf, hold on, box on, axis equal, axis manual;
        xlim(limits(1, :));
        ylim(limits(2, :));
        zlim(limits(3, :));
        title(sprintf('Step: %d  Time: %.2f', round(t / dt), t));

        for i = 1: n_cores
          plot(rs{1}{i}(:, 1), rs{1}{i}(:, 2), '.', ...
              'MarkerSize', size_star, 'MarkerEdgeColor', color_stars(i));
          plot(rc{1}(i, 1), rc{1}(i, 2), '.', 'MarkerSize', size_core, ...
              'MarkerEdgeColor', color_cores(i, :));
          xlabel('x');
          ylabel('y');
        end
        drawnow;

        if show_save
            writeVideo(writer, getframe(gcf));
        end
        pause(delay);
   end
   
   [rc, rs] = updateToomre(rc, rs, m_cores, dt);
end

if show_save
   close(writer);
   fprintf('Saved to video file: %s\n', save_name);
end
close all;