clear, clc, clf;

% ----- problem constants -----
n_cores = 2;
m_cores = [1, 1];
n_stars = [2000, 2000];
range_r_stars = [0.3, 1; 0.2, 0.8];
range_theta_stars = [pi/2, pi/2; pi/2, pi/2];
range_phi_stars = [0, 2 * pi; 0, 2 * pi];
range_va_stars = [pi/2, pi/2; pi/2, pi/2];

% ----- intial conditions -----
r_cores = [0, 0, 0; 2, -2, 0];
v_cores = [0, -1, 0; 0, 1, 0];
r_stars = cell(1, n_cores);
v_stars = cell(1, n_cores);

% uniform random sampling of star positions and velocities
for i = 1: n_cores
    r = randsInRange(range_r_stars(i, :), n_stars(i));
    etheta = pi/2 - randsInRange(range_theta_stars(i, :), n_stars(i));
    phi = randsInRange(range_phi_stars(i, :), n_stars(i));
    [x, y, z] = sph2cart(phi, etheta, r);
    r_stars(1, i) = {[x, y, z] + r_cores(i, :)};
    
    va = randsInRange(range_va_stars(i, :), n_stars(i));
    vhat = [-sin(va) .* sin(phi) - cos(va) .* sin(etheta) .* cos(phi), ...
             sin(va) .* cos(phi) - cos(va) .* sin(etheta) .* sin(phi), ...
             cos(va) .* cos(etheta)];
    v_stars(1, i) = {sqrt(m_cores(i) ./ r) .* vhat + v_cores(i, :)};
end

% ----- simulation constants -----
tmax = 6;
level = 10;
dt = tmax / (2 ^ level + 1);

% ----- options -----
show = true;
is_3d = false;
delay = 0;
padding = 4;
limits = [min(r_cores, [], 1) - padding; max(r_cores, [], 1) + padding]';

save = true;
save_fps = 25;
save_name = 'toomre.avi';

color_stars = ['b', 'r'];
color_cores = [[9, 18, 110] / 255; [173, 3, 3] / 255];
size_core = 10;
size_star = 3;

% ----- execution -----
if save
   writer = VideoWriter(save_name);
   open(writer);
end

for t = 0 : dt : tmax
   if show
        clf, hold on, box on, axis equal, axis manual;
        xlim(limits(1, :));
        ylim(limits(2, :));
        zlim(limits(3, :));
        title(sprintf('Step: %d  Time: %.2f', round(t / dt), t));

        for i = 1: n_cores
          if is_3d
              view(3);
              scatter3(r_stars{1, i}(:, 1), r_stars{1, i}(:, 2), r_stars{1, i}(:, 3), ...
                  size_star, '.', 'MarkerEdgeColor', color_stars(i));
              scatter3(r_cores(i, 1), r_cores(i, 2), r_cores(i, 3), ...
                  size_core, '.', 'MarkerEdgeColor', color_cores(i, :));
          else
              plot(r_stars{1, i}(:, 1), r_stars{1, i}(:, 2), '.', ...
                  'MarkerSize', size_star, 'MarkerEdgeColor', color_stars(i));
              plot(r_cores(i, 1), r_cores(i, 2), '.', 'MarkerSize', size_core, ...
                  'MarkerEdgeColor', color_cores(i, :));
          end
        end
        drawnow;

        if save
         writeVideo(writer, getframe(gcf));
        end
        pause(delay);
   end
   
   [r_cores, v_cores, r_stars, v_stars] = ...
       updateToomre(r_cores, v_cores, r_stars, v_stars, m_cores, dt);
end

if save
   close(writer);
   fprintf('Saved to video file: %s\n', save_name);
end
close all;