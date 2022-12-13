---
title: "Research"
weight: 2
katex: true



# bookFlatSection: false
# bookToc: true
# bookHidden: false
# bookCollapseSection: false
# bookComments: false
# bookSearchExclude: false
---
# Research Interests

{{< hint danger >}}
**In progress**  
{{< /hint >}}

{{< hint info >}}
**See the GitHub links for a bit more technical details.**  
{{< /hint >}}

## Tensor Networks, Renormalization, and Phase Transitions 
[[GitHub]](https://github.com/letallbewell/Tensor-Network-Contraction)

Tensor Networks are a new computational tool that finds applications in quantum many body physics and machine learning. Among many of its applications it allows to efficiently parametrize high dimensional Hilbert spaces of quantum sytems of interests and also provides a computationally tractable representation of partition functions involving lattice Hamiltoniancs (see [Ising Model](https://github.com/letallbewell/Ising_Model) for an application to the Ising Hamiltonian using the Google's Tensor Network library).

The network can be thought of a graph represntation of a complicated array contraction, like a long series of matrix miltiplication. Since contraction is associative, the order does not make a differnece to the answer but the computational cost hevily relies on the order. Finding the optimal order is a discrete optimization problem(tough) and renormalization approaches can iteratively simplify the graph to give approximate answers.

The follwong tensor network contraction gives the partition function for the Ising Hamiltonian on a  lattice with periodic boundary conditions (larger networks failed to contract on my laptop).



![Naive contraction](/images/TN_contraction.jpg)

We can see that the code works by checking the thermodynamic variables (these results are exact).


![Energy and Specific Heat Capacity](/images/TN_E&Cv.jpg)

Results can be compared against a Monte-Carlo simulation. See [Ising Model](https://github.com/letallbewell/Ising_Model) for the results of an 8*8 lattice:

![MC Samples](/images/MC_Samples.jpg)
![MC Results](/images/MC_Results.jpg)


## Cosmology

![Nbody Simulation Picture](/images/gadget_visualization.jpg)

We would not be here if not for dark matter. Matter cannot aggregate gravitationally to form structures due to radiation pressure until the universe could cool down considerably. However, dark matter interacts gravitationally alone so that it could form bound structures and form gravitational potential buckets for matter to fall in later when the universe cooled down. Stars later lighted up the 'dark' dark matter haloes!

Understanding the nature of primordial fluctuations, the seed of all structures in the universe is a fundamental problem in modern physics. One tool to study this is the N-body simulation codes like the [Gadget-II](https://wwwmpa.mpa-garching.mpg.de/gadget/), which connects these fluctuations to present-day large-scale structure.


{{< youtube Dguvi2uA_KU >}}



## Fluid Dynamics 
[[GitHub]](https://github.com/letallbewell/Lattice-Boltzmann)

The Navier-Stokes equations (mass, momentum, and energy continuity. equations in fluids) can describe everything from stirring a cup of coffee to the earth's climate. Predicting the fluid flow is challenging even with the complete knowledge of initial conditions. Most algorithms require massive parallelization, and there are many pesky numerical instabilities in simulations. 

For my MSc thesis, I studied the driven lid cavity problem (think of a 2D box stirred from the top edge) using the Lattice Boltzmann method (LBM). LBM is a numerical scheme stemming from kinetic theory using a discretized version of the Boltzmann equation with an ad-hoc collision operator defined to emulate fluid behavior. Since it only uses array movements and arithmetic operations, LBM is economical in the low Reynolds number regime where the LBM approximation is more faithful.

{{% columns %}}

{{< youtube 4Aa55GaYGbQ >}}

<--->

{{< youtube pkpIo9ZMNyg >}}

{{% /columns %}}

## Quantum Mechanics 
[[GitHub]](https://github.com/letallbewell/Shrodinger_Equation-Finite_Difference_Solutions)

Deriving the spectrum and the eigenvalues of the Hydrogen atom using the series solution to the Schrodinger equation is an analytical nightmare. The operator method (see section 6.2 of  [Principles of Quantum Mechanics, David Skinner](http://www.damtp.cam.ac.uk/user/dbs26/PQM.html)) is also much work. I enjoyed both approaches, but you can use the finite difference approximation if you really need a feel of the solutions in no time.

In 1 dimension, the second derivative can be approximated as a difference, and the Schrodinger equation equates to a matrix eigenvalue problem after discretizing the potential. This formalism can easily be extended to 3d using tensor products, and voila, you have the answers!

{{% columns %}}

![Nbody Simulation Picture](/images/Hydrogen_Atom.png)

<--->

![Nbody Simulation Picture](/images/Harmonic_Oscillator.png)

{{% /columns %}}

## Chaos in the Lorenz Attractor System 
[[GitHub]](https://github.com/letallbewell/Lorenz-System)


The Lorenz system is arised in a simplified description of atmospheric convection and probably the best known example of chaotic system. It is defined by the following system of differential equations:


{{< katex display >}} \frac{dx}{dt} = \sigma \left( y - x \right),{{< /katex >}}

{{< katex display >}} \frac{dy}{dt} = x \left( \rho - z \right)  - y \text{ , and, } {{< /katex >}}
 
{{< katex display >}} \frac{dz}{dt} = xy - \beta z.{{< /katex >}}

{{< katex display >}} \alpha, \beta \text{ and } \sigma \text{ are parameters of the system.} {{< /katex >}}

The defining property of chaotic systems is **approximate initial conditions cannot predict approximate futures whereas exact initial conditions can predict exact future**.

The popular notion of the butterfy effect (the flap of a butterfly's wing affecting a tornado weeks later) is a metaphorical version of this phenomenon of sensitive dependence on initial conditions. The shape of the solutions also resmble a butterfly to the romanticization's merit.

A particle cloud of N = 1000, points starting about [1, 1, 1] is integrated this way. You can see how quickly these particles (red dots) diverge from the solution for the strating point [1, 1, 1] (golden curve).



{{< youtube RIgKHnjR-XE >}}



## Patent Landscape Study of Quantum Technologies

In 2021, I wrote a patent landscape study report for [Relecura Technologies](https://relecura.com/), analyzing around 50k patents in quantum technologies using natural language processing tools. The report includes elementary physics explanations of the technologies aimed at policy makers and investors.

{{< tabs "QT_tabs" >}}

{{< tab "Report" >}} 
### [Quantum Technologies: A Review of the Patent Landscape](https://arxiv.org/abs/2102.04552), Mathew Alex, 2021. 

{{< /tab >}}

{{< tab "Taxonomy" >}} 

### Taxonomy of the technologies [(Interactive Version)](https://search2.relecura.com/index.php/taxonomy/loadPublicTaxonomy/de8b3d26-651f-11eb-919d-023ada72e4ef)
![Quantum Technologies Taxonomy](/images/Quantum_Technologies_Taxonomy.png)

{{< /tab >}}

{{< /tabs >}}

