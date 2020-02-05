% Find the marginals (firing rates and correlations) of
% sample data, and compare them against the maximum entropy
% model predictions.

% Load example spiking data of 15 neurons.
load example15

% Randomly divide it into a training set and a test set 
% (so we can verify how well we trained).
[ncells,nsamples] = size(spikes15);
idx_train = randperm(nsamples,ceil(nsamples/2));
idx_test = setdiff(1:nsamples,idx_train);
samples_train = spikes15(:,idx_train);
samples_test = spikes15(:,idx_test);

% Create a k-pairwise model (pairwise maxent with synchrony constraints).
model = maxent.createModel(ncells,"kising");

% Train the model to a threshold of 1.5 standard deviations from the 
% error of computing the marginals. Because the distribution is larger 
% (50 dimensions) we cannot explicitly iterate over all 5^20 states
% in memory and will use markov chain monte carlo (MCMC) methods to obtain an approximation
model = maxent.trainModel(model,samples_train,"threshold",1.5);

% Get the marginals (firing rates and correlations) of the test data and see 
% how they compare to the model predictions. Here the model marginals could not be 
% computed exactly so they will be estimated using monte-carlo. We specify the
% number of samples we use so that their estimation will have the same amoutn noise as the empirical marginal values
marginals_data = maxent.getEmpiricalMarginals(samples_test,model);
marginals_model = maxent.getMarginals(model,'nsamples',size(samples_test,2));
