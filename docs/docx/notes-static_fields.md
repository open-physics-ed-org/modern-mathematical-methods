# 26 Sept 23 - Notes: Static Fields

## Vector Calculus

[Maxwell's Equations](https://en.wikipedia.org/wiki/Maxwell%27s_equations), even in their static form (i.e., static charges or steady currents), are a set of coupled partial differential equations. In order to develop solutions and models to approximate the behavior of electromagnetic fields, we need to be able to use vector calculus. 

The video below from [3Blue1Brown](https://www.3blue1brown.com/) provides a conceptual introduction to the vector calculus that we are going to need for this.

[
> **[Image not embedded: remote images are not included in PDF export. Check the original file for the image.]**
![Image not embedded: remote image](https://markdown-videos-api.jorgenkh.no/youtube/rB83DpBJQsE?width=720&height=405)](https://inv.tux.pizza/watch?v=rB83DpBJQsE)

- Non-Commercial Link: [https://inv.tux.pizza/watch?v=rB83DpBJQsE](https://inv.tux.pizza/watch?v=rB83DpBJQsE)
- Commercial Link: [https://youtube.com/watch?v=rB83DpBJQsE](https://youtube.com/watch?v=rB83DpBJQsE)

## Electrostatic fields

The electrostatic field is one that is created by static (stationary) charges. This is often the first type of field that we encounter, where $\rho(\mathbf{r},t)) = \rho(\mathbf{r})$. Because the charges are stationary, the current density is zero, $\mathbf{J}(\mathbf{r},t) = \mathbf{0}$. 

### The electric field

The relevant Maxwell equations for $\mathbf{E}$ that govern an electrostatic situation are the following:


$$\nabla \cdot \mathbf{E} = \frac{\rho}{\varepsilon_0}$$

$$\nabla \times \mathbf{E} = 0$$


You might recognize the first equation as the differential form of [Gauss's Law](https://en.wikipedia.org/wiki/Gauss%27s_law).


> **[Image not embedded: remote images are not included in PDF export. Check the original file for the image.]**
![Image not embedded: remote image](https://subratachak.files.wordpress.com/2017/12/gauss-law-diagram-03.jpg?w=782)

As you can see from the figure above, Gauss's Law is always true, but almost never useful in solving problem outside specific geometries. The integral form of that equation is:

$$\oint \mathbf{E} \cdot d\mathbf{A} = \frac{Q_{enc}}{\varepsilon_0}$$

It is from considering the integral form of Gauss' Law that we can obtain the electric field produced by a single point charge, $Q$, at a location $\mathbf{r}'$:

$$\mathbf{E}(\mathbf{r}) = \frac{Q}{4\pi\varepsilon_0} \frac{\mathbf{r} - \mathbf{r}'}{|\mathbf{r} - \mathbf{r}'|^3}$$


The second relevant equation is a statement that the curl of the electrostatic field is zero. This indicates that an electrostatic field is a [conservative field](https://en.wikipedia.org/wiki/Conservative_vector_field). This means that the electrostatic field can be written as the gradient of a scalar potential, $\mathbf{E} = -\nabla V$, as we will see later.

There is a general integral solution the electrostatic problem, which is built up from the concept of a point charge. That solution, which can be used in certain integrable situations and adapted to numerical methods is:

$$d\mathbf{E} = \frac{1}{4\pi\varepsilon_0} \frac{dq}{|\mathbf{r} - \mathbf{r}'|^3} (\mathbf{r} - \mathbf{r}')$$

$$\mathbf{E}(\mathbf{r}) = \frac{1}{4\pi\varepsilon_0} \int \frac{dq}{|\mathbf{r} - \mathbf{r}'|^3} (\mathbf{r} - \mathbf{r}')$$

We will find later that the [electric potential](https://en.wikipedia.org/wiki/Electric_potential) ($V$) is a better choice if we can use it. It simplifies our vector problem to a scalar problem.

### The magnetic field

The relevant Maxwell equations for $\mathbf{B}$ that govern an electrostatic situation are the following:

$$\nabla \cdot \mathbf{B} = 0$$

$$\nabla \times \mathbf{B} = 0$$

Notice that these equations are solved when $\mathbf{B}$ = 0. This is because there are no magnetic monopoles, so if the divergence and curl of the field are zero everywhere, then the field must be zero everywhere. There's simply no sources of magnetic field. So in an electrostatic situation, the magnetic field is zero and we are purely focused on the electric field.



## Magnetostatic fields

In a magnetostatic situation, there have to be currents; that is, moving charges. That is the only make to generate magnetic field from particles. So you are going to have a non-zero current density. But we argue that the currents are steady, so $\mathbf{J}(\mathbf{r},t) = \mathbf{J}(\mathbf{r})$. Now, of course, there will be electric field, but we will discuss how we consider that in a moment.

### The magnetic field

The relevant Maxwell equations for $\mathbf{B}$ that govern a magnetostatic situation are the following:

$$\nabla \cdot \mathbf{B} = 0$$

$$\nabla \times \mathbf{B} = \mu_0 \mathbf{J}$$

The first equation always holds; there are no [magnetic monopoles](https://en.wikipedia.org/wiki/Magnetic_monopole), despite much research into the area [including searches](https://en.wikipedia.org/wiki/Magnetic_monopole#Searches_for_magnetic_monopoles) and a [theory of electromagnetism](https://en.wikipedia.org/wiki/Magnetic_monopole#In_SI_units) that posits them. Here's a nice article summarizing the state of the magnetic monopole research from 2016, [The mysterious missing magnetic monopole](https://phys.org/news/2016-08-mysterious-magnetic-monopole.html), and an [article from the IceCube experiment](https://icecube.wisc.edu/news/research/2022/01/icecube-and-the-mystery-of-the-missing-magnetic-monopoles/), which a number of our [faculty, grad students, and undergrads are involved in](https://pa.msu.edu/high-energy-physics/icecube-neutrino-observatory.aspx).

The second equation is [Ampere's Law](https://en.wikipedia.org/wiki/Amp%C3%A8re%27s_circuital_law) in it's differential form. Much like Gauss's law, it is always true, but rarely useful outside of specific geometries. Note that for the magnetostatic situation that current density can vary with space only. The integral form of Ampere's Law is can be used to solve problems with symmetry:

$$\oint \mathbf{B} \cdot d\mathbf{l} = \mu_0 I_{enc}$$

And it is from considering this form for a single current carrying wire that we can determine the magnetic field produced by a single current carrying wire, $I$, at a location $\mathbf{r}'$:

$$\mathbf{B}(\mathbf{r}) = \frac{\mu_0 I}{4\pi} \frac{\hat{\mathbf{\phi}}}{|\mathbf{r} - \mathbf{r}'|^2}$$

Because of the curly nature of magnetic field, we find that the general solution to the magnetostatic problem is given by the [Biot-Savart Law](https://en.wikipedia.org/wiki/Biot%E2%80%93Savart_law):

$$d\mathbf{B} = \frac{\mu_0}{4\pi} \frac{I d\mathbf{l} \times (\mathbf{r} - \mathbf{r}')}{|\mathbf{r} - \mathbf{r}'|^3}$$

$$\mathbf{B}(\mathbf{r}) = \frac{\mu_0}{4\pi} \int \frac{I d\mathbf{l} \times (\mathbf{r} - \mathbf{r}')}{|\mathbf{r} - \mathbf{r}'|^3}$$

In practice, we rarely use this form of the qeuation directly because it requires integrable solutions. Instead, we use the integral form of Ampere's Law to solve problems with symmetry, we use the differential forms to solve problems numerically, and we develop other theoretical approaches. Because the divergence of the magnetic field is zero, we can write the magnetic field as the curl of a [vector potential](https://en.wikipedia.org/wiki/Magnetic_vector_potential), $\mathbf{B} = \nabla \times \mathbf{A}$. This has a integral form that is similar to the Biot-Savart Law, but directly proportional to the current density, which is much nicer:

$$\mathbf{A} = \frac{\mu_0}{4\pi} \int_V \frac{\mathbf{J}(\mathbf{r}')}{|\mathbf{r} - \mathbf{r}'|} d\tau'$$

It turns out this is a better method for solving problems, especially computationally. That is beyond the scope of this course.

### The electric field

Because there is a magnetic field, the relevant Maxwell equations for $\mathbf{E}$ that govern a magnetostatic situation are the following:

$$\nabla \cdot \mathbf{E} = \frac{\rho}{\varepsilon_0}$$

$$\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}$$

Notice now we have to consider a changing magnetic field. In the magnetostatic situation, we argue the current densities are setup such that the magnetic field is static (i.e., $\frac{\partial \mathbf{B}}{\partial t} = 0$).  This means the relevant equations for the electric field remain those in the electrostatic situation:

$$\nabla \cdot \mathbf{E} = \frac{\rho}{\varepsilon_0}$$

$$\nabla \times \mathbf{E} = 0$$

And all the relevant tools we will develop for the electrostatic situation for $\mathbf{E}$ apply here as well.

## Additional Resources

### Handwritten Notes
 - [Vector Calculus](../../assets/notes/Notes-Vector_Calculus.pdf)
 - [Electrostatics and Superposition](../../assets/notes/Notes-Electrostatics_and_Superposition.pdf)
 - [Gauss's Law](../../assets/notes/Notes-Gauss_Law.pdf)
 - [Magnetostatics](../../assets/notes/Notes-Magnetostatics.pdf)
 - [Ampere's Law](../../assets/notes/Notes-Amperes_Law.pdf)


