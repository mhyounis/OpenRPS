The Continuous Slowing Down Approximation
=========================================

.. It is important to describe how NittanyPhysics treats the continuous slowing down approximation (CSDA). Many Boltzmann transport codes rely on this to describe, typically, low energy (or 'soft') inelastic scattering of massive particles, including collisions and radiative scattering. However, the operator is quite unlike the generic scattering operator, and its discretization is non-trivial. That is because the operator comes in the form:

.. .. math::
    
..     \hat{C}\psi = \frac{\partial}{\partial E}(L(E)\psi(E))

.. for some linear energy transfer $L(E)$ and the angular fluence $\psi(E)$. The trouble comes when you try to energy group this:

.. .. math::
    
..     \int_{E_{g+1}}^{E_{g}}dE \ \frac{\partial}{\partial E}(L(E)\psi(E)) = L(E_{g})\psi(E_{g}) - L(E_{g+1})\psi(E_{g+1})

.. The multigroup BTE involves solving for $\psi_{g} = \int_{g}dE \ \psi(E)$, not $\psi(E_{g})$ nor any other energy gridpoint. Thus, we need to figure out how to express the above in terms of $\psi_{g}$.

.. NittanyPhysics takes an approach which is a little bit unique incomparison to other treatments (or at least, treatments we have seen in the literature). The most common method is to convert the operator into a set of pseudo-cross sections using a differencing technique. We do this, however, the technique we have designed treats the stopping power exactly (methods seen in the literature [CITE] apply diamond differencing to the product $L(E)\psi(E)$, not to only $\psi(E)$). We also employ a boundary condition, i.e., explicit knowledge of $\psi(E_{1})$. It will be seen shortly why this is necessary (but also quite practical, provided the space-angle solver is aware of the resulting source term), but first we discuss why it is possible. In principle, we can split $\psi(E)$ into a collided and an uncollided portion:

.. .. math::
    
..     \psi(E) = \tilde{\psi}(E) + \tilde{\psi}^{0}(E)

.. where the first term, the collided fluence, is unknown, but the second term, the uncollided fluence, is known. A solver like Lionbolt uses the 'first collision scattering' (FCS) method, wherein the second term is constructed analytically and used to rephrase the Boltzmann transport problem for $\tilde{\psi}$. Nevertheless, it can be reasoned that precisely at $E_{1}$, the collided fluence is zero (with some considerations regarding how the particle is being sourced -- however, under the assumption that there is zero fluence beyond $E_{1}$, $\tilde{\psi}(E_{1})$ should still be assumed to be zero). Meanwhile, precisely at $E_{1}$, the uncollided fluence is known. Thus, we can indeed choose as a boundary condition $\psi(E_{1}) = \tilde{\psi}^{0}(E_{1})$, a quantity which is readily accessible in a typical Boltzmann transport solver.

.. We will now describe precisely how NittanyPhysics defines CSDA pseudo-cross sections as well as the boundary term resulting (which is in any case agnostic to the precise expression of the boundary condition).

.. Diamond Differencing Formulation
.. --------------------------------

.. Despite the tricky derivation, the goal is quite simple -- write:

.. .. math::
    
..     L(E_{g})\psi(E_{g}) - L(E_{g+1})\psi(E_{g+1}) \approx - \Sigma_{t,g}\psi_{g} + \sum_{g' < g}\Sigma_{s,g'\rightarrow g}\psi_{g'}

.. The sign convention is because we take this term to come on the same side of the BTE as the scattering operator. Also, the scattering cross sections are assumed to be delta-down, i.e., straight-forward, involving no angular deflection, so we neglect any angular indices/description. Finally, we emphasize that g' is the incident energy group index while g is thus the outgoing group index (the group being solved).

.. The scheme is as follows: We form a system of equations to be solved for $\psi(E_{g})$ and $\psi(E_{g+1})$ using as the 'knowns,' $\psi_{g}$ values. In order to do this, we Taylor expand $\psi(E)$ about the respective energy gridpoints, and then energy group these. For instance, for $\psi(E_{g})$, we take:

.. .. math::
    
..     \psi(E) \approx \psi(E_{g}) + (E - E_{g})\psi'(E_{g}) + \frac{1}{2}(E - E_{g})^{2}\psi''(E_{g})

.. Then:

.. .. math::
    
..     & \int_{g}dE \ \psi(E) = \Delta E_{g}\psi(E_{g}) + \psi'(E_{g})\int_{g}dE \ (E - E_{g}) + \psi''(E_{g})\int_{g}dE \ \frac{1}{2}(E - E_{g})^{2} \\
..     & \int_{g - 1}dE \ \psi(E) = \Delta E_{g - 1}\psi(E_{g}) + \psi'(E_{g})\int_{g - 1}dE \ (E - E_{g}) + \psi''(E_{g})\int_{g - 1}dE \ \frac{1}{2}(E - E_{g})^{2} \\
..     & \int_{g - 2}dE \ \psi(E) = \Delta E_{g - 2}\psi(E_{g}) + \psi'(E_{g})\int_{g - 2}dE \ (E - E_{g}) + \psi''(E_{g})\int_{g - 2}dE \ \frac{1}{2}(E - E_{g})^{2}

.. This here is a second-order expansion. An $n$th order expansion thus involves $\psi_{g}$ to $\psi_{g - n}$. Note however, the above treatment cannot be taken for $g \leq 2$ (or $g \leq n$ in the $n$th order case). We will discuss those cases separately later on. Nevertheless, the above forms a matrix problem:

.. .. math::
    
..     \begin{pmatrix}
..         \psi_{g} \\ \psi_{g - 1} \\ \psi_{g - 2}
..     \end{pmatrix}
..     =
..     \begin{pmatrix}
..         C_{11} & C_{12} & C_{13} \\
..         C_{21} & C_{22} & C_{23} \\
..         C_{31} & C_{32} & C_{33}
..     \end{pmatrix}
..     \begin{pmatrix}
..         \psi(E_{g}) \\ \psi'(E_{g}) \\ \psi''(E_{g})
..     \end{pmatrix}

.. The derivation of the matrix coefficients is straightforward. We leave these unspecified. Nevertheless, we only really want $\psi(E_{g})$, so we can invert the matrix and keep only the first row, yielding:

.. .. math::
    
..     \psi(E_{g}) = v_{C,1}\psi_{g} + v_{C,2}\psi_{g - 1} + v_{C,3}\psi_{g - 2}

.. where $v_{C,i}$ is the $i$th column of the first row of $C^{-1}$. We emphasize that all of these coefficients can be determined solely based on energy group structure, no information regarding fluence nor even LETs is needed.

.. Now, to form $\psi(E_{g+1})$, we repeat this formulation but with our expansion centered about $E_{g+1}$:

.. .. math::
    
..     \psi(E) \approx \psi(E_{g+1}) + (E - E_{g+1})\psi'(E_{g+1}) + \frac{1}{2}(E - E_{g+1})^{2}\psi''(E_{g+1})

.. Then:

.. .. math::
    
..     & \int_{g}dE \ \psi(E) = \Delta E_{g}\psi(E_{g+1}) + \psi'(E_{g+1})\int_{g}dE \ (E - E_{g+1}) + \psi''(E_{g+1})\int_{g}dE \ \frac{1}{2}(E - E_{g+1})^{2} \\
..     & \int_{g - 1}dE \ \psi(E) = \Delta E_{g - 1}\psi(E_{g+1}) + \psi'(E_{g+1})\int_{g - 1}dE \ (E - E_{g+1}) + \psi''(E_{g+1})\int_{g - 1}dE \ \frac{1}{2}(E - E_{g+1})^{2} \\
..     & \int_{g - 2}dE \ \psi(E) = \Delta E_{g - 2}\psi(E_{g+1}) + \psi'(E_{g+1})\int_{g - 2}dE \ (E - E_{g+1}) + \psi''(E_{g+1})\int_{g - 2}dE \ \frac{1}{2}(E - E_{g+1})^{2}

.. This yields a different matrix problem:

.. .. math::
    
..     \begin{pmatrix}
..         \psi_{g} \\ \psi_{g - 1} \\ \psi_{g - 2}
..     \end{pmatrix}
..     =
..     \begin{pmatrix}
..         D_{11} & D_{12} & D_{13} \\
..         D_{21} & D_{22} & D_{23} \\
..         D_{31} & D_{32} & D_{33}
..     \end{pmatrix}
..     \begin{pmatrix}
..         \psi(E_{g + 1}) \\ \psi'(E_{g + 1}) \\ \psi''(E_{g + 1})
..     \end{pmatrix}

.. and a different solution:

.. .. math::
    
..     \psi(E_{g + 1}) = v_{D,1}\psi_{g} + v_{D,2}\psi_{g - 1} + v_{D,3}\psi_{g - 2}

.. Now we are ready to form $L(E_{g})\psi(E_{g}) - L(E_{g+1})\psi(E_{g+1})$ and thus write the pseudo-cross sections. We find:

.. .. math::
    
..     g > 2 \ : \ \ \ L(E_{g})\psi(E_{g}) - L(E_{g+1})\psi(E_{g+1}) & = (L(E_{g})v_{C,1} - L(E_{g+1})v_{D,1})\psi_{g} \\
..     & + (L(E_{g})v_{C,2} - L(E_{g+1})v_{D,2})\psi_{g - 1} \\
..     & + (L(E_{g})v_{C,3} - L(E_{g+1})v_{D,3})\psi_{g - 2}

.. or:

.. .. math::
    
..     g > 2 \ : \ \ \ \Sigma_{t,g} & = - (L(E_{g})v_{C,1} - L(E_{g+1})v_{D,1}) \\
..     \Sigma_{s,g - 1\rightarrow g} & = L(E_{g})v_{C,2} - L(E_{g+1})v_{D,2} \\
..     \Sigma_{s,g - 2\rightarrow g} & = L(E_{g})v_{C,3} - L(E_{g+1})v_{D,3}

.. Boundary Terms
.. ~~~~~~~~~~~~~~

.. We must now discuss the cases $g = 1$ and $g = 2$. Let's deal with $g = 2$ first.

.. If we go to write our system of equations for $g = 2$, we realize that we cannot form more than $\psi_{2}$ and $\psi_{1}$ as our knowns. Thus, we just need a third condition for this system. This condition is most conveniently taken as $\psi(E_{1}) = B$, the boundary condition, for reasons we discussed earlier in this document. Therefore, the third line of our system for $E_{2}$ reads:

.. .. math::
    
..     B = \psi(E_{2}) + (E_{1} - E_{2})\psi'(E_{2}) + \frac{1}{2}(E_{1} - E_{2})^{2}\psi''(E_{2})

.. and for $E_{3}$ it is:

.. .. math::
    
..     B = \psi(E_{3}) + (E_{1} - E_{3})\psi'(E_{3}) + \frac{1}{2}(E_{1} - E_{3})^{2}\psi''(E_{3})

.. These are just the Taylor expansions evaluated at $E_{1}$. Anyway, our system of equations is then for example:

.. .. math::
    
..     \begin{pmatrix}
..         \psi_{2} \\ \psi_{1} \\ B
..     \end{pmatrix}
..     =
..     \begin{pmatrix}
..         C_{11} & C_{12}          & C_{13} \\
..         C_{21} & C_{22}          & C_{23} \\
..         1      & (E_{1} - E_{2}) & \frac{1}{2}(E_{1} - E_{2})^{2}
..     \end{pmatrix}
..     \begin{pmatrix}
..         \psi(E_{2}) \\ \psi'(E_{2}) \\ \psi''(E_{2})
..     \end{pmatrix}

.. and similarly for $E_{3}$. We can then form:

.. .. math::
    
..     \psi(E_{2}) = v_{D,1}\psi_{2} + v_{D,2}\psi_{1} + v_{D,3}B

.. In the end, we are left with:

.. .. math::
    
..     L(E_{2})\psi(E_{2}) - L(E_{3})\psi(E_{3}) & = (L(E_{2})v_{C,1} - L(E_{3})v_{D,1})\psi_{2} \\
..     & + (L(E_{2})v_{C,2} - L(E_{3})v_{D,2})\psi_{1} \\
..     & + (L(E_{2})v_{C,3} - L(E_{3})v_{D,3})B

.. or:

.. .. math::
    
..     \Sigma_{t,2} & = - (L(E_{2})v_{C,1} - L(E_{3})v_{D,1}) \\
..     \Sigma_{s,1\rightarrow 2} & = L(E_{2})v_{C,2} - L(E_{3})v_{D,2} \\
..     \Sigma_{B,2} & = L(E_{2})v_{C,3} - L(E_{3})v_{D,3}

.. where $\Sigma_{B,g}$ is a special cross section to be used only on the boundary term. NittanyPhysics generates these and stores them separately from $\Sigma_{s}$ and $\Sigma_{t}$.

.. For $g = 1$ the case is much simpler. As much as we can do is assume:

.. .. math::
    
..     \psi_{1} = \frac{\Delta E_{1}}{2}(\psi(E_{1}) + \psi(E_{2})) = \frac{\Delta E_{1}}{2}(B + \psi(E_{2}))

.. and thus:

.. .. math::
    
..     L(E_{1})\psi(E_{1}) - L(E_{2})\psi(E_{2}) = (L(E_{1}) + L(E_{2}))B - \frac{2L(E_{2})}{\Delta E_{1}}\psi_{1}

.. or:

.. .. math::
    
..     \Sigma_{t,1} & = \frac{2L(E_{2})}{\Delta E_{1}} \\
..     \Sigma_{B,1} & = L(E_{1}) + L(E_{2})

.. Summary
.. -------

.. We summarize the results. The pseudo-cross sections are:

.. .. math::
    
..     g > 2 \ : \ \ \ \Sigma_{t,g} & = - (L(E_{g})v_{C,1} - L(E_{g+1})v_{D,1}) \\
..     \Sigma_{s,g - 1\rightarrow g} & = L(E_{g})v_{C,2} - L(E_{g+1})v_{D,2} \\
..     \Sigma_{s,g - 2\rightarrow g} & = L(E_{g})v_{C,3} - L(E_{g+1})v_{D,3}

.. .. math::
    
..     \Sigma_{t,2} & = - (L(E_{2})v_{C,1} - L(E_{3})v_{D,1}) \\
..     \Sigma_{s,1\rightarrow 2} & = L(E_{2})v_{C,2} - L(E_{3})v_{D,2}
    
.. .. math::
    
..     \Sigma_{t,1} = \frac{2L(E_{2})}{\Delta E_{1}}

.. where $v_{C,i}$ and $v_{D,i}$ are described in the text. They are generally group-dependent, except for $g > 2$ linear groups (due to the boundary terms, the $g = 2$ case will be different from the rest).

.. The boundary scattering cross sections are:

.. .. math::
    
..     \Sigma_{B,1} & = L(E_{1}) + L(E_{2}) \\
..     \Sigma_{B,2} & = L(E_{2})v_{C,3} - L(E_{3})v_{D,3}

.. where the cross section $\Sigma_{B,g}$ is to be multiplied with $B = \psi(E_{1})$ to form a contribution to the source for group $g$. 

.. Concluding Remarks
.. ------------------

.. We note, this result is distinct from those of CEPXS [CITE] and Drumm et al. [CITE] (totaling three different formulations), however, the steps in this derivation are identical to the second-order scheme of Drumm et al., which was used in the first version of NittanyPhysics, with three significant exceptions: One, we do not difference $L(E)\psi(E)$ as a whole, which would require ultimately assuming that $(L(E)\psi(E))_{g} = L_{g}\psi_{g}/\Delta E_{g}$, two, we do not assume linear energy groups, and three, we treat the boundary conditions more explicitly rather than using 'ghost groups.' While ghost groups are not explicitly discussed by Drumm et al., it is implied if their formulation results in taking the respective cross sections to zero when $g - 1 < 0$ or $g - 2 < 0$. This would result from inventing two evenly-sized groups at energies higher than $E_{1}$, extending the grid artificially but ultimately being able to derive a Taylor expansion in these ghost groups.

.. The reason that we have neglected to use ghost groups, and thus introduced a boundary condition, is because we found, though we have not recorded exact numerics, that in several validation cases, logarithmically spaced groups seem to require a large number of groups for fluences to converge to the EGS benchmark compared to linearly spaced groups, provided enough linearly spaced groups are being used in the first place of course. We are not aware of whether or not this is an accepted/common issue with these formulations, as we do not have access to any other codes that generate these cross sections, however, we were able to show that there were problems with the discretization for the first and second energy groups, i.e., the groups relying on ghost groups. We found this using a manufactured solution of the CSDA operator as implemented in NittanyPhysics. 

.. This is something we've put in a driver file, which is available in ``$NITTANY/examples/drivers/CSDA/CSDAMMS.f90``. It allows a user to specify an energy group structure, as well as a linear energy transfer function, and an angular fluence function (functions of energy only). Then, it determines whether or not:

.. .. math::
    
..     L(E_{g})\psi(E_{g}) - L(E_{g+1})\psi(E_{g+1}) \approx - \Sigma_{t,g}\psi_{g} + \sum_{g' < g}\Sigma_{s,g'\rightarrow g}\psi_{g'}

.. including boundary terms for $g = 1$ and $g = 2$. The above is quantified by percent error, for each energy group. Using ghost groups it was not found that $\psi(E)$ given by a polynomial up to order 2 was well-represented by the above, however, with the inclusion of the boundary term this is well satisfied. Furthermore, for more complex functions, and regardless of the expression for $L(E)$, we find satisfactory agreement overall using our scheme, though we will not here dive into the numerical evidence, as it has not been documented. This may be done at a later date.