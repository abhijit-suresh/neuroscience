function sys = LinearODE()
    % LinearODE  Linear Ordinary Differential Equation in two variables
    %   Implements the system of linear ordinary differential equations
    %        x'(t) = a*x(t) + b*y(t)
    %        y'(t) = c*x(t) + d*y(t)
    %   for use with the Brain Dynamics Toolbox.
    %
    % Example 1: Using the Brain Dynamics graphical toolbox
    %   sys = LinearODE();      % construct the system struct
    %   gui = bdGUI(sys);       % open the Brain Dynamics GUI
    % 
    % Example 2: Using the Brain Dynamics command-line solver
    %   sys = LinearODE();                              % system struct
    %   sys.pardef = bdSetValue(sys.pardef,'a',1);      % parameter a=1
    %   sys.pardef = bdSetValue(sys.pardef,'b',-1);     % parameter b=-1
    %   sys.pardef = bdSetValue(sys.pardef,'c',10);     % parameter c=10
    %   sys.pardef = bdSetValue(sys.pardef,'d',-2);     % parameter d=-2
    %   sys.vardef = bdSetValue(sys.vardef,'x',rand);   % variable x=rand
    %   sys.vardef = bdSetValue(sys.vardef,'y',rand);   % variable y=rand
    %   tspan = [0 10];                                 % soln time span
    %   sol = bdSolve(sys,tspan);                       % call the solver
    %   tplot = 0:0.1:10;                               % plot time domain
    %   Y = bdEval(sol,tplot);                          % extract solution
    %   plot(tplot,Y);                                  % plot the result
    %   xlabel('time'); ylabel('x,y');
    % Handle to our ODE function
    sys.odefun = @odefun;
    
    % ODE parameter definitions
    sys.pardef = [ struct('name','a', 'value', 1);
                   struct('name','b', 'value',-1);
                   struct('name','c', 'value',10);
                   struct('name','d', 'value',-2) ];
    
    % ODE variable definitions
    sys.vardef = [ struct('name','x', 'value',2*rand-1);
                   struct('name','y', 'value',2*rand-1) ];

    % Latex (Equations) panel
    sys.panels.bdLatexPanel.title = 'Equations'; 
    sys.panels.bdLatexPanel.latex = { 
        '\textbf{LinearODE}';
        '';
        'System of linear ordinary differential equations';
        '\qquad $\dot x(t) = a\,x(t) + b\,y(t)$';
        '\qquad $\dot y(t) = c\,x(t) + d\,y(t)$';
        'where $a,b,c,d$ are scalar constants.';
        };

    % Time Portrait panel 
    sys.panels.bdTimePortrait = [];

    % Phase Portrait panel
    sys.panels.bdPhasePortrait = [];
  
    % Solver panel
    sys.panels.bdSolverPanel = [];
    
    % Default time span (optional)
    sys.tspan = [0 20]; 

    % Specify the relevant ODE solvers (optional)
    sys.odesolver = {@ode45,@ode23,@odeEul};
    
    % ODE solver options (optional)
    sys.odeoption.RelTol = 1e-6;        % Relative Tolerance
    sys.odeoption.Jacobian = @jacfun;   % Handle to Jacobian function 
end

% The ODE function.
% The variables Y and dYdt are both (2x1) vectors.
% The parameters a,b,c,d are scalars.
function dYdt = odefun(t,Y,a,b,c,d) 
    dYdt = [a b; c d] * Y;              % matrix multiplication
end

% The Jacobian function (otional).
function J = jacfun(t,Y,a,b,c,d)  
    J = [a b; c d];
end

