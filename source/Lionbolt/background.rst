.. _lbbackground:

Background
==========

Lionbolt is a code dedicated to solving the monoenergetic Boltzmann transport problem, at the moment specializing in transport of ionizing radiation. It uses the discontinuous finite element method (FEM).

Lionbolt ships as both a library and a program, with the program relying on the library to construct a solution of the *polyenergetic*, coupled-particle Boltzmann transport problem, informed by a user-provided input file. Beyond this, the library's API is meant to be sufficiently flexible and intuitive that a user can generalize to other Boltzmann transport problems. Internally, the design of the library is such that users can also rather easily implement their own operators if they so choose, extending the utility of Lionbolt even further.

Below we describe the theory of Boltzmann transport as it pertains to polyenergetic transport of ionizing radiation, describing ultimately the basic capabilities of Lionbolt. However, note that a much more in-depth document has been written during the construction of *wiscobolt*, the predecessor of Lionbolt and NittanyPhysics, which is publicly archived at https://github.com/mhyounis/wiscobolt (released Oct 2023). Although wiscobolt's use is not encouraged, its documents may be particularly interesting to those focused on the physics and theory rather than computation.

Theory
------

.. attention:: This section is WIP.

The following is derived from several sources. If you are interested, you can find more elaborate derivations in the references that follow :cite:`Battista2019, Demaziere, Podgorsak, Passage, Absorbeddose`.

The Polyenergetic Boltzmann Transport Equation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We start from the time-independent Boltzmann transport equation, an integro-differential equation in six dimensions, in the particular form most familiar to the study of ionizing radiation transport:

.. math::
    
    \big(\mathbf{\hat{k}}\cdot\nabla + & \Sigma_{t}(\mathbf{r},E)\big)\psi(\mathbf{r},\mathbf{\hat{k}},E) \\
    & - \int dE'd\Omega' \ \Sigma_{s}(\mathbf{r},\mu_{s},E'\rightarrow E)\psi(\mathbf{r},\mathbf{\hat{k}}',E') = s(\mathbf{r},\mathbf{\hat{k}},E)

where:

- $\psi$ is the angular fluence of radiation particles at position $\mathbf{r}$, in angular direction $\mathbf{\hat{k}}$, and with energy $E$. These three variables form '*phase space*'. Furthermore, the angular fluence is related to a more generic *density* of particles in phase space $n$, via $\psi(\mathbf{r},\mathbf{\hat{k}},E) = v(E)n(\mathbf{r},\mathbf{\hat{k}},E)$, where $v(E)$ is the velocity of particles at energy $E$.

- $\Sigma_{t}$ is the total attenuation coefficient of the medium at location $\mathbf{r}$, for particles of energy $E$. The physical meaning of the attenuation coefficient is that it describes the number of particles, per unit path length, that undergo some reaction (such as scattering, absorption, production, etc.), that results in loss of particles at the slice of phase space $(\mathbf{r},E)$.

- $\Sigma_{s}$ is the scattering coefficient of the medium at location $\mathbf{r}$, for particles with scattering angle cosine $\mu_{s} = \mathbf{\hat{k}}\cdot\mathbf{\hat{k}}{'}$, and initial and final energies $E'$ and $E$ respectively. This describes the number of particles, per unit path length per unit solid angle per unit energy, undergoing scattering reactions that map from $E'\rightarrow E$, and involve a change in scattering angle $\mu_{s}$. Notably, we can rely on $\mu_{s}$ to describe the angular distribution of a scattering event because we assume unpolarized radiation fields and thus scattering mechanisms that are in the aggregate independent of polarization (i.e., averaged over polarizations). Finally, integrals of the scattering coefficient contribute to the attenuation coefficient.

- $\mathbf{\hat{k}}\cdot\nabla$ physically causes '*streaming*', i.e., the straight-line motion of particles through physical space $\mathbf{r}$, along their angular coordinate $\mathbf{\hat{k}}$, inbetween scattering and other loss events.

- $s$ is the source. It describes the density of phase space particles being produced at a particular location in phase space. Notably, it very well can involve production of radiation particles due to the interactions of a different type of particle, referred to as '*coupling*' in which case the source is created via:

.. math::
    
    \int dE'd\Omega' \ \Sigma_{s}^{\alpha\beta}(\mathbf{r},\mu_{s},E'\rightarrow E)\psi^{\beta}(\mathbf{r},\mathbf{\hat{k}}',E') = s^{\alpha}(\mathbf{r},\mathbf{\hat{k}},E)
    
for the production of particles of kind $\alpha$ due to particles of kind $\beta$.

We emphasize therefore that we do not employ the Fokker-Planck approximation. However, in the case of massive particles, Lionbolt is compatible with multigroup moments generated via the restricted continuous slowing down approximation (CSDA), wherein 'soft' inelastic scattering events (i.e., events with energy loss less than some threshold $\Delta$) are incorporated in Boltzmann transport via:

.. math::
    
    \frac{\partial}{\partial E}\big(L_{\Delta}(\mathbf{r},E)\psi(\mathbf{r},\mathbf{\hat{k}},E)\big) = s_{\Delta}(\mathbf{r},\mathbf{\hat{k}},E)
    
where $L_{\Delta}$ is the linear stopping power, related to the first moment of $\Sigma_{s}$ in energy, isotropically averaged over angle. Notably, this term involves no deflection. Thus, the extent of Lionbolt's treatment of these terms is a specifically located array entry for all cross sections that involve forward-scattering, which is treated differently from a general scattering operation. Nevertheless, generation of such moments is of course relegated to a code such as :ref:`NittanyPhysics <nittanyphysics>`.

The Multigroup Approximation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On this note, from this Boltzmann transport equation we employ the multigroup approximation. In this approximation, we take the scattering coefficients and attenuation coefficients and assume that, within a range of energy, they are constant (albeit discontinuous). We further make this assumption about our source and solution. Thus, we form a matrix problem in the energy dependence:

.. math::
    
    \big(\mathbf{\hat{k}}\cdot\nabla + \Sigma_{t,g}(\mathbf{r})\big)\psi_{g}(\mathbf{r},\mathbf{\hat{k}}) - \sum_{g'=1}^{G}\int d\Omega' \ \Sigma_{s,g'g}(\mathbf{r},\mu_{s})\psi_{g'}(\mathbf{r},\mathbf{\hat{k}}') = s_{g}(\mathbf{r},\mathbf{\hat{k}})

However, upon the assumption that scattering never results in an increase in energy of the radiation particle (i.e., on the assumption that our medium is stationary), we ultimately recognize that the matrix that couples energies $\Sigma_{s,g'g}$ has a triangular structure, and thus we can iteratively run over energies and allow them to source downstream energies via:

.. math::
    :label: monoenergetic
    
    \big(\mathbf{\hat{k}}\cdot\nabla + \Sigma_{t,g}(\mathbf{r})\big)\psi_{g}(\mathbf{r},\mathbf{\hat{k}}) - \int d\Omega' \ \Sigma_{s,gg}(\mathbf{r},\mu_{s})\psi_{g}(\mathbf{r},\mathbf{\hat{k}}') = s_{g}(\mathbf{r},\mathbf{\hat{k}}) + s_{g}^{\text{EI}}(\mathbf{r},\mathbf{\hat{k}})
    
where $s_{g}^{\text{EI}}$ is the 'energy iteration' source, i.e., the source of fluence at group $g$ due to particles at all groups $g'$ with higher energies. Its form, taking $g = 1$ to be the *most* energetic group and $g = G$ to be the *least*, is of course:

.. math::
    
    s_{g}^{\text{EI}}(\mathbf{r},\mathbf{\hat{k}}) = \sum_{g'=1}^{g - 1}\int d\Omega' \ \Sigma_{s,g'g}(\mathbf{r},\mu_{s})\psi_{g'}(\mathbf{r},\mathbf{\hat{k}}')

We note therefore, that :eq:`monoenergetic` is a *monoenergetic* Boltzmann transport problem.

Spherical Harmonics Expansion of Scattering Operator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We consider the monoenergetic scattering operator:

.. math::
    
    \hat{K}\psi = \int d\Omega' \ \Sigma_{s}(\mathbf{r},\mu_{s})\psi(\mathbf{r},\mathbf{\hat{k}}')

Now, in order to perform this angular integration, we must discretize this operator. We do so independent of the method of discretization we ultimately choose for the angular variables $\mathbf{\hat{k}}$, which are to be discussed shortly. We rely upon spherical harmonics expansions truncated to order $N$, referred to as the $P_{N}$ scattering method, yielding:

.. math::
    :label: pnscat
    
    \hat{K}\psi = \sum_{\ell=0}^{N}\sum_{m=-\ell}^{\ell}Y^{m}_{\ell}\Sigma_{s,\ell}\psi^{m}_{\ell}

If $N$ is taken to $\infty$ then :eq:`pnscat` is exact. We note the conventions here are:

.. math::
    
    Y^{m}_{\ell}(\mu,\phi) = \sqrt{\frac{(2\ell + 1)}{4\pi}\frac{(\ell - m)!}{(\ell + m)!}}P^{m}_{\ell}(\mu)e^{im\phi}

.. math::
    
    P^{m}_{\ell}(\mu) = (-1)^{m}(1-\mu^{2})^{m/2}\frac{d^{m}}{d\mu^{m}}P_{\ell}(\mu)

.. math::
    
    \Sigma_{s,\ell} = 2\pi\int_{-1}^{1}d\mu \ \Sigma_{s}(\mu)P_{\ell}(\mu)

.. math::
    
    \psi^{m}_{\ell} = \int d\Omega \ Y^{m}_{\ell}(\mu,\phi)\psi(\mathbf{\hat{k}})

with $P_{\ell}(\mu)$ the typical Legendre polynomial and $\mu = \cos\theta$. Note also that one can instead use the real spherical harmonics instead of $Y^{m}_{\ell}$ and find the same relationships.

Discrete Ordinates
~~~~~~~~~~~~~~~~~~

Now, for general discretization of angle, at the moment Lionbolt relies on the use of 'discrete ordinates' of order $N$ ($S_{N}$). There exists a spherical harmonics expansion for the general problem as well, referred to as $P_{N}$, however this is not yet implemented in Lionbolt (it is, however, :ref:`planned <lbroadmap>`)


The Finite Element Method
~~~~~~~~~~~~~~~~~~~~~~~~~

.. _normalization:

Sources and Normalization of Results
------------------------------------

It is important to discuss the external beam sources currently available in Lionbolt, as well as normalization of these sources (and thus all results linearly dependent on the source) in Lionbolt.

Nowhere are you asked to provide, e.g., a beam intensity, to get real, numerical results. This is consistent with many Monte Carlo radiation transport codes --- if you use these codes (or Terpdose) you may recognize that many quantities are plotted 'per fluence' or 'per incident fluence.' Here, we describe what this means, as it is an important convention and may inform your definition of the beam.

Consider first the simpler, one-beam case. The idea is that we choose to normalize our beam to a certain fluence value. We will outline first the spherical case and then move onto the planar case (which applies to the slab case as well).

Spherical beam
~~~~~~~~~~~~~~

In the spherical beam case, otherwise called a point-source, we have a rather straightforward expression for our source:

.. math::
    
    s(\mathbf{r},\mathbf{\hat{k}},E) = s_{0}f(E)\delta^{3}(\mathbf{r} - \mathbf{R}_{0})g(\mathbf{\hat{k}})

where $f(E)$ is a normalized energy distribution, and $g(\mathbf{\hat{k}})$ is a normalized angular distribution, thus, making $s_{0}$ the total phase-space integral of s:

.. math::
    
    s_{0} = \int d\Gamma \ s

Now, for this point source case, we consider the angular distributions which describe an isotropic beam that is perfectly collimated within some region on the unit sphere $C$:

.. math::
    
    g(\mathbf{\hat{k}}) = \frac{1}{\Delta\Omega}\begin{cases}
        1, & \mathbf{\hat{k}} \in C \\
        0, & \text{else}
    \end{cases}

where $1/\Delta\Omega$ is the solid angle spanned by the cutout, thus depending on the quantities which define the cutout itself (i.e., ``cutoutparams`` in user input). This is indeed normalized over the unit sphere.

Nevertheless, the uncollided angular fluence, evaluated in vacuum, can be given analytically as:

.. math::
    
    \tilde{\psi}^{0}\big|_{\text{vac}} = s_{0}f(E)\frac{1}{\Delta\Omega|\mathbf{r} - \mathbf{R}_{0}|^{2}}\delta^{2}\big(\mathbf{\hat{k}} - \mathbf{\hat{k}}_{0}(\mathbf{r})\big)

where $\mathbf{\hat{k}}_{0}(\mathbf{r})$ points from the source origin to the point of interest $\mathbf{r}$:

.. math::
    
    \mathbf{\hat{k}}_{0}(\mathbf{r}) = \frac{\mathbf{r} - \mathbf{R}_{0}}{|\mathbf{r} - \mathbf{R}_{0}|}

Note also we take $\text{vac}$ to mean you are also within the uncollimated region (for notational simplicity). Now, we integrate out the energy and angular variables to obtain a fluence:

.. math::
    
    \tilde{\Phi}^{0}\big|_{\text{vac}} = \frac{s_{0}}{\Delta\Omega|\mathbf{r} - \mathbf{R}_{0}|^{2}}

The key is that we *define* this quantity, at some location, to be $\bar{\Phi}^{0}$, and through that specify $s_{0}$. Say we take the location at which $\bar{\Phi}^{0}$ is defined to be the cutout. In that case, the inverse square factor in $\tilde{\Phi}^{0}$ becomes just the source-to-cutout-definition distance (i.e., the first entry of ``cutoutparams``), say, $S$. Then:

.. math::
    
    s_{0} = S^{2}\Delta\Omega\bar{\Phi}^{0}

by definition. We thus go all the way back to the source with this new expression:

.. math::
    
    s(\mathbf{r},\mathbf{\hat{k}},E) = S^{2}\Delta\Omega\bar{\Phi}^{0}f(E)\delta^{3}(\mathbf{r} - \mathbf{R}_{0})g(\mathbf{\hat{k}})

Since we are working with the linear BTE, we can just normalize our problem to $\bar{\Phi}^{0}$, yielding:

.. math::
    
    s^{\text{Lionbolt}} = s / \bar{\Phi}^{0}

Under this convention then, and still in the one-beam case, all post-processing quantities such as dose are determined like:

.. math::
    
    D^{\text{Lionbolt}} = D / \bar{\Phi}^{0}

Thereby giving the units of per fluence.

Numerically, this amounts to doing our solve assuming that one particle crosses the cutout per square centimeter.

Planar beam
~~~~~~~~~~~

In the planar beam case the source expression is a little different, but its resulting uncollided fluence is actually very simple. Thus, we will start with that:

.. math::
    
    \tilde{\psi}^{0}\big|_{\text{vac}} = s_{0}f(E)\frac{1}{A}\delta^{2}\big(\mathbf{\hat{k}} - \mathbf{\hat{k}}_{0}\big)

where here $A$ is the cross-sectional area of the planar beam (which could be arbitrarily large, as in the slab case) and $\mathbf{\hat{k}}_{0}$ is the beam axis. The resulting fluence is simply:

.. math::
    
    \tilde{\Phi}^{0}\big|_{\text{vac}} = \frac{s_{0}}{A}

Here, it does not matter where we define the fluence, as every particle emitted by the beam effectively travels in a straight line and thus the beam never spreads out. We can consequently take:

.. math::
    
    \tilde{\psi}^{0}\big|_{\text{vac}} = \bar{\Phi}^{0}f(E)\delta^{2}\big(\mathbf{\hat{k}} - \mathbf{\hat{k}}_{0}\big)

and then again define our quantities by dividing out $\bar{\Phi}^{0}$.

Note, one could suggest an easier definition of uniformly taking $s_{0} = 1$, which indeed wiscobolt does, however, this was decided against in Lionbolt because it would lead the wide-open planar beam/slab cases to result in different units than the collimated planar and spherical beam, as the factor of $1/A$ in the former cases would blow up to infinity, so we'd need to normalize those to fluence. Furthermore, in the context of radiation therapy, clinicians often calibrate linear accelerators to fluence values at known distances, which thus works very nicely with the fluence normalization convention.

Multiple beams
~~~~~~~~~~~~~~

In the case of multiple beams, the user must define weighting factors that relate the normalizations of different beams to one universal fluence $\bar{\Phi}^{0}$. 

Consider first the case where only one particle type has beams (i.e., no contamination beam, but more than one primary beam). Let $\bar{\Phi}^{0}_{i}$ be the fluence definition for beam $i$, whether this beam is spherical or planar. The user will have to reason, taking into account the cutout surface at which the fluences are defined, appropriate (relative) weights $w_{i}$ for their beams. So, if they want beam 1 to be half as strong as beam 2, they must specify the weight for beam as 1 and of beam 2 as 2, or any factor of these. Then, the $i$th source term is written with:

.. math::
    :label: multiplebeams
    
    \bar{\Phi}^{0}_{i} = \frac{w_{i}}{\sum_{j}w_{j}}\bar{\Phi}^{0}

and by 'per fluence' we subsequently will mean $1/\bar{\Phi}^{0}$.

What if you now introduce contaminant beams? The weight convention for these differs significantly, as they are considered to be absolute, not necessarily normalized, weights with respect to $\bar{\Phi}^{0}$ as defined above.

**Example**

For a somewhat more practical example, suppose you are working with a primary photon beam and then a 'contaminant' electron beam. Physically, these contaminants arise from the fact that collimation is not at all perfect. The lead blocks used to shape X-ray beams generate electrons as a consequence of irradiation, and these electrons are then indeed capable of delivering noteworthy amounts of dose. Now, suppose a user can describe their contaminant electron spectrum, and determine, for instance, the number of electrons generated per fluence at the collimator head, $n$. How should they weigh it?

One way they can figure this out is to start with their beam definition in Lionbolt. If they define their collimation at the collimator head then they can skip a step, however, if not, they can map between the two using:

.. math::
    
    \bar{\Phi}^{\text{Head}} = \frac{S_{\text{L}}^{2}}{S_{\text{Head}}^{2}}\bar{\Phi}^{\text{L}}

where L stands for 'Lionbolt.' We now assume the geometry of this electron beam is identical to that of the photon beam, including in user definition (if this is not the case, the following can be generalized easily). Now, the number of electrons in this beam is:

.. math::
    
    N = n\bar{\Phi}^{\text{Head}}

while the desired fluence of this beam at the Lionbolt definition is thus:

.. math::
    
    \bar{\Phi}^{\text{contam.}} = \frac{N}{S_{\text{L}}^{2}} = \frac{n}{S_{\text{Head}}^{2}}\bar{\Phi}^{\text{L}}

Consequently, the absolute weight factor they seek for this beam is the ratio of this to $\bar{\Phi}^{\text{L}}$, or:

.. math::
    
    w^{\text{abs}} = \frac{n}{S_{\text{Head}}^{2}}

Then, all results will remain scaled to $\bar{\Phi}^{\text{L}}$, which in this case describes the photon fluence at the user's collimator definition.

.. bibliography::
    :filter: docname in docnames
    :style: unsrt