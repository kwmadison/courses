
function [array] = PPtoAngCov(inarr,centre_X,centre_Y,ThetaBin)
% inarr = PeakPairs;
% centre_X = 150;
% centre_Y = 150;
% height = 300;
% width = 300;
% ThetaBin = 6;

while mod(360,ThetaBin) ~= 0
    ThetaBin = ThetaBin + 1; %Force it to be an integer factor
end

%Thetabin in degrees

Cart_Ar(:,1) = inarr(:,1) - centre_X;
Cart_Ar(:,2) = inarr(:,2) - centre_Y;
Cart_Ar(:,3) = inarr(:,3);

[Theta Rho] = cart2pol(Cart_Ar(:,1),Cart_Ar(:,2));
Pol_Ar(:,1) = 180*Theta/pi;
Pol_Ar(:,2) = Rho;
Pol_Ar(:,3) = Cart_Ar(:,3);


Pol_Ar(:,1) = round(Pol_Ar(:,1)/ThetaBin)*ThetaBin;
Bin_Ind = Pol_Ar(:,1)/ThetaBin + 180/ThetaBin; %What Theta Array index does each count go to? 

Frames_With = sort(unique(Pol_Ar(:,3)));
S_Angular = zeros(round(360/ThetaBin)); %Prep covariance Mat
Th_Bar = hist(Pol_Ar(:,1),360/ThetaBin)/length(Frames_With);

Th_Hists = Frames_With.*zeros(1 + 360/ThetaBin,1)';
%%

% The slowness here seems to be that after doing peaks from frames, they still get
% searched in the future, and after finding an paek from a different frame,
% it still searches the rest
start = 1;
for indx = 1:length(Frames_With) %For the number of frames
    FSearch = Frames_With(indx);
    for PkSearch = start:length(Bin_Ind) %Search through list of peak coordiantes
        if Pol_Ar(PkSearch,3) == FSearch
            %Make a histogram for each frame
            Th_Hists(indx,round(Bin_Ind(PkSearch))+1) = Th_Hists(indx,round(Bin_Ind(PkSearch))+1) + 1;
        else
            start = PkSearch; % This is what I added
            break
        end
    end
end
%%
for i= 1:length(S_Angular)
    for j = 1:length(S_Angular)
        %i/length(S_Angular) + j/length(S_Angular).^2
        if j ~= i
            Summation = 0;
            %ang_ia = i*ThetaBin - 180;
            Th_aBar = Th_Bar(i);
            %ang_ib = j*ThetaBin - 180;
            Th_bBar = Th_Bar(j);
            
            for indx = 1:length(Frames_With) %For the number of frames
                
                Th_ia = Th_Hists(indx,i);
                Th_ib = Th_Hists(indx,j);
                
                Summation = Summation + (Th_ia-Th_aBar)*(Th_ib-Th_bBar);
            end
            S_Angular(i,j)  = (1/length(Frames_With))*Summation; % JDP 5.7
        else
            S_Angular(i,j) = 0;
        end
    end
end



array = flipud(S_Angular);
%imagesc(array)
 end
