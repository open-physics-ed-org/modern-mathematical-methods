# 17 Oct 23 - Activity: Normal Modes

As we begin to work with multi-particle systems, we begin to open the number of degrees of freedom of the system. We increase the complexity of it and the challenge of modeling it. We will increasingly need tools that help us take less tractable issues and make them palatable. One such tool that forms the basis of many others is **Normal Modes**.

Normal modes are ways of breaking up our understanding of a system into discrete (potentially infinite and hopefully vanishingly small) pieces. This lets us get at the big picture of the system and characterize how much we are neglecting. The concept of normal modes underlies much of the analysis done in quantum mechanics, field theory, fluid mechanics, and signal processing. In fact, numerical routines often make use of forms of these modes to do economize calculations -- *especially when we move beyond a few hundred bodies in the system*. This stuff is part and parcel of most research in physics. For example, how we understand the [Cosmic Background Radiation](https://en.wikipedia.org/wiki/Cosmic_background_radiation) relies on a [normal mode like analysis](https://www.quantamagazine.org/how-ancient-light-reveals-the-universes-contents-20200128/).


## Canonical Coupled Oscillators


There is still plenty of room for pencil and paper. We will explore this numerically later. 

We will start with a form of guided lecture and build the understanding of these methods together. Then you will apply what you learned to a new system.

Let's assume you have a chain of two mass connected by springs (all the same $k$) as below.

![Coupled Oscillator set up. Two oscillators connected by three springs in a horizontal line.](../images/activity-CoupledOsc-NormalModes_two-coupled-gliders-diagram.png)


### Deriving the Equations of Motion

Let's write the Lagrangian for this system to get equations of motion. The kinetic and potential energies are:

$$T=\frac{1}{2}m\dot{x}_1^2+\frac{1}{2}m\dot{x}_2^2$$
$$U=\frac{1}{2}k{x_1}^2+\frac{1}{2}k(x_2-x_1)^2 + \frac{1}{2}k{x_2}^2$$

Thus the Lagrangian is for this system is:

$$L = \frac{1}{2}m\dot{x}_1^2+\frac{1}{2}m\dot{x}_2^2 - \frac{1}{2}k{x_1}^2-\frac{1}{2}k(x_2-x_1)^2 - \frac{1}{2}k{x_2}^2$$

Which produces two equations of motion:

$$\frac{d}{dt}\left(\frac{\partial L}{\partial \dot{x}_1}\right) - \frac{\partial L}{\partial x_1} = 0$$
$$\frac{d}{dt}\left(\frac{\partial L}{\partial \dot{x}_2}\right) - \frac{\partial L}{\partial x_2} = 0$$

Which we can write as:

$$m\ddot{x}_1 = -kx_1 + k(x_2-x_1)$$
$$m\ddot{x}_2 = -kx_2 + k(x_1-x_2)$$

Or

$$\ddot{x}_1 = -\frac{2k}{m}x_1 + \frac{k}{m}x_2$$
$$\ddot{x}_2 = -\frac{2k}{m}x_2 + \frac{k}{m}x_1$$



### Finding Normal Modes

#### Method 1: Assume a Solution

A normal mode solution is one in which all parts of a system oscillate with the same frequency. For linear systems, this can be a very useful approach because any solution can be represented as a linear combination of normal modes. In general,

$$f(t) = \sum_n c_n \psi_n(t)$$

where $f(t)$ is the solution, $c_n$ are constants, and $\psi_n(t)$ are the normal modes. This kind of normal mode analysis forms the basis for signal analysis, image processing, and many other fields. For non-linear systems, we lose superposition and thus, we lose out ability to employ normal modes. However, near equilibria and in other limits, normal modes are still used. We will start by assuming a normal mode solution for both masses and plug that into our equations of motion. 

Assume:

$$x_1(t) = A_1\cos(\omega t + \phi_1)$$
$$x_2(t) = A_2\cos(\omega t + \phi_2)$$

where $A_1$, $A_2$, $\phi_1$, and $\phi_2$ are constants to be determined. We can plug these into our differential equations and find the normal modes. We made a chose for the form of the solution. Other forms are acceptable as long as they have two free parameters; it's a second order differential equation.

We can plug these into our differential equations and get:

$$-\omega^2A_1\cos(\omega t + \phi_1) = -\frac{k}{m}A_1\cos(\omega t + \phi_1) + \frac{k}{m}(A_2\cos(\omega t + \phi_2)-A_1\cos(\omega t + \phi_1))$$
$$-\omega^2A_2\cos(\omega t + \phi_2) = -\frac{k}{m}A_2\cos(\omega t + \phi_2) + \frac{k}{m}(A_1\cos(\omega t + \phi_1)-A_2\cos(\omega t + \phi_2))$$

which we can collect the terms $A_1$ and $A_2$ and get:

$$-\omega^2A_1\cos(\omega t + \phi_1) + 2\frac{k}{m}A_1\cos(\omega t + \phi_1) = \frac{k}{m}A_2\cos(\omega t + \phi_2)$$
$$-\omega^2A_2\cos(\omega t + \phi_2) + 2\frac{k}{m}A_2\cos(\omega t + \phi_2) = \frac{k}{m}A_1\cos(\omega t + \phi_1)$$

Which we rewrite as:

$$\left(2\frac{k}{m}-\omega^2\right)A_1\cos(\omega t + \phi_1) = \frac{k}{m}A_2\cos(\omega t + \phi_2)$$
$$\frac{k}{m}A_1\cos(\omega t + \phi_1)=\left(2\frac{k}{m}-\omega^2\right)A_2\cos(\omega t + \phi_2)$$

Assuming non-zero solutions, we can divide the equations:

$$\dfrac{\left(2\frac{k}{m}-\omega^2\right)}{\frac{k}{m}} = \dfrac{\frac{k}{m}}{\left(2\frac{k}{m}-\omega^2\right)}$$

So that,

$$\left(2\frac{k}{m}-\omega^2\right)^2 = \left(\frac{k}{m}\right)^2$$

Or, 

$$\omega^2 = \frac{2k}{m} \pm \frac{k}{m}$$

So, if solution is a normal mode, there's actually two of them it could be: one with $\omega = \sqrt{\frac{3k}{m}}$ and one with $\omega = \sqrt{\frac{k}{m}}$.


**&#9989; Do this** 

1. Given the frequencies of the normal mode solutions, find the relative amplitudes of the two masses for each mode. How do the masses move relative to each other?
2. Consider the following initial conditions, the left mass ($x_1$) is displaced by $x_0$. Everything else is at rest. Find the particular solution for each mass ($x_1$ and $x_2$).
3. Plot their motion.
4. (later, if time) develop a numerical solution for $x_1$ and $x_2$ for any choice of conditions.


```python
## Your code here
```

#### Method 2: Matrix Analysis (the Eigenvalue Problem)

That analysis to find the normal modes was a bit of a pain in algebra. As we add more objects, that pain will grow. We can use a matrix approach to make this easier. It's also a systematic approach that as we will see plays nicely with computing. 

Starting from the equations of motion:

$$\ddot{x}_1 = -\frac{2k}{m}x_1 + \frac{k}{m}x_2$$
$$\ddot{x}_2 = -\frac{2k}{m}x_2 + \frac{k}{m}x_1$$

We rewrite them as a set of matrix equations for the vector $\mathbf{x} = \begin{bmatrix}x_1\\x_2\end{bmatrix}$:

$$\ddot{\mathbf{x}} = \begin{bmatrix}-\frac{2k}{m} & \frac{k}{m}\\\frac{k}{m} & -\frac{2k}{m}\end{bmatrix}\mathbf{x}$$

This is a form of the equation $\ddot{\mathbf{x}} = \pmb{A} \mathbf{x}$ where $\pmb{A}$ is the coefficient matrix. We can solve this equation by finding the eigenvalues and eigenvectors of $\pmb{A}$. The eigenvalues are the frequencies of the normal modes and the eigenvectors are the relative amplitudes of the masses. The reason is that the determinant of the coefficient matrix when there is a normal mode solution vanishes. That is,

$$\det(\pmb{A}+\omega^2\pmb{I}) = 0$$

where $\pmb{I}$ is the identity matrix. This is a polynomial equation in $\omega^2$ and the roots of that polynomial are the normal mode frequencies.  This technique is very common in theoretical physics with different guesses for the solution forms giving rise to different eigenvalue problems (e.g., [Bessel functions for 2D surface problems](https://en.wikipedia.org/wiki/Bessel_function) or [Hermite polynomials for the Quantum Harmonic Oscillator](https://en.wikipedia.org/wiki/Hermite_polynomials).

**&#9989; Do this** 

1. Using the "determinant of the coefficient matrix" (really the eigenvalues of $\pmb{A}$ solved by $\det(\pmb{A}+\omega^2\pmb{I})$), find the normal mode $\omega^2$.
2. Find the eigenvectors of the coefficient matrix. These are the relative amplitudes of the masses.
3. These results should agree with the previous method. Do they?
4. Plot the normal modes solutions.


```python
## your code here
```

## Applying Normal Modes to a New System

### Two vertical pendulums connected by a spring

Consider two vertical pendulums of length $l$ connected via their masses $M$ by a weak spring $k$. By weak, we mean that the spring constant is small. See below for a canonical setup:

![Coupled pendulua diagram](../images/activity-CoupledOsc-NormalModes_coupled_diag.jpg)

**&#9989; Do this** 

1. In this limit, write down the pair of second order linear differential equations for the horizontal motion of each pendulum bob around its equilibrium.
2. Find and describe the normal modes. Use plots of your choosing to explain what you found.


```python
## your code here
```

## Three Coupled Oscillators

Consider the setup below consisting of three masses connected by springs to each other. We intend to find the normal modes of the system by denoting each mass's displacement ($x_1$, $x_2$, and $x_3$).

![3 Coupled Oscillators](../images/activity-CoupledOsc-NormalModes_3_coupled_osc.png)

## Finding the Normal Mode Frequencies

**&#9989; Do this** 

This is not magic as we will see, it follows from our choices of solution. Here's the steps and what you might notice about them:

1. Guess what the normal modes might look like? Write your guesses down; how should the masses move? (It's ok if you are not sure about all of them, try to determine one of them)
2. Write down the energy for the whole system, $T$ and $U$ (We have done this before, but not for this many particles)
3. Use the Euler-Lagrange Equation to find the equations of motion for $x_1$, $x_2$, and $x_3$. (We have done this lots, so make sure it feels solid)
4. Reformulate the equations of motion as a matrix equation $\ddot{\mathbf{x}} = \mathbf{A} \mathbf{x}$. What is $\mathbf{A}$? (We have done this, but only quickly, so take your time)
5. Consider solutions of the form $Ce^{i{\omega}t}$, plug that into $x_1$, $x_2$, and $x_3$ to show you get $\mathbf{A}\mathbf{x} = -\omega^2 \mathbf{x}$. (We have not done this, we just assumed it works! It's ok if this is annoying, we only have to show it once.)
6. Find the normal mode frequencies by taking the determinant of $\mathbf{A} - \mathbf{I}\lambda$. Note that this produces the following definition: $\lambda = -\omega^2$ (We have not done this together and we can if it's confusing.)

## Finding the Normal Modes Amplitudes

Ok, now we need to find the normal mode amplitudes. That is we assumed sinusoidal oscillations, but at what amplitudes? We will show how to do this with one frequency ($\omega_1$), and then break up the work of the the other two. These frequencies are:

$$\omega_A = 2\dfrac{k}{m}; \qquad \omega_B = \left(2-\sqrt{2}\right)\dfrac{k}{m}; \qquad \omega_C = \left(2+\sqrt{2}\right)\dfrac{k}{m}\qquad$$

**&#9989; Do this** 

After we do the first one, pick another frequencies and repeat. Answer the follow questions:

1. What does this motion physically look like? What are the masses doing?
2. How does the frequency of oscillation make sense? Why is it higher or lower than $\omega_A$?

* [Partial Solution to Activity](../assets/notes/Notes-Three_Coupled_Oscillators.pdf)


