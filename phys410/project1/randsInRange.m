function xs = randsInRange(range, count)
% Generate random numbers in given range
% range: [min, max] bounds for generated numbers
% count: number of randoms
    xs = (range(2) - range(1)) .* rand(count, 1) + range(1);
end