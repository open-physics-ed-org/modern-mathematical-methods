# 4 Dec 23 - Notes: Markov Chain Monte Carlo Modeling

One of the principal tools we have at our disposal when it comes to systems with randomness is the Monte Carlo simulation. Monte Carlo is a large class of approaches that all rely on probabilistic outcomes to determine results. In physics, we often use Monte Carlo to find integrals or sums that we are unable to compute by hand. 

## Markov Chain Monte Carlo

We often find ourselves using a type of Monte Carlo simulation that makes use of a Markov Chain. This is called the MCMC model. The mathematical foundations of Markov Chains are well beyond the scope of this course, but the principal issue is that we want to describe is how this simulation works. The video below describes the conceptual backing of MCMC and how it was first used in physics in 1953 to develop a model of an ideal gas. We will make a similar model!

[![](https://markdown-videos-api.jorgenkh.no/youtube/12eZWG0Z5gY?width=720&height=405)](https://inv.tux.pizza/watch?v=12eZWG0Z5gY)

- Non-Commercial Link: [https://inv.tux.pizza/watch?v=12eZWG0Z5gY](https://inv.tux.pizza/watch?v=12eZWG0Z5gY)
- Commercial Link: [https://youtube.com/watch?v=12eZWG0Z5gY](https://youtube.com/watch?v=12eZWG0Z5gY)

## Statistical Mechanics

MCMC is used in lots of statistical mechanics problems because they are fundamentally probabilistic by nature. Starting with the "chance" of finding our system in a given state (with known energy, $E_i$) at a known temperature (T) given by the Boltzmann factor:

$$e^{-E_i/{k_b T}}$$

where $k_b$ is the Boltzmann constant. Through this, we developed a statistical model where we found that the normalized probability of finding your system in a state $s$ with energy $E_s$ (just using the $s$ to indicate a state) is given by:

$$P(s) = \dfrac{1}{Z} e^{-E_s/{k_b T}}$$

where $Z$ is the partition function, a constant for a given temperature that normalizes our calculation. It is a sum over all states:

$$Z = \sum_s e^{-E_s/{k_b T}}$$

Our analysis relied on the development of a statistical theory of mechanics, and we illustrated it with an ideal gas. 

Because $P(S)$ is a probability we can use it find average values (expectation values) of a thermodynamic system. We did this for energy using the thermodynamic relations in the notes. But we can also use statistical properties to find the same. For example, finding the expected internal energy of a system, $\langle U \rangle$, just involves adding up all the possible energy states multiplied by their probabilities!

$$\langle U \rangle = \sum_s E_s P(s)$$

When these sums are really hard to compute because there's lots of states or only a few that contribute substantially (as in the case for large systems), we can use selective sampling, which is the basis for MCMC. We will discuss that conceptually in class before using MCMC.

## Additional Resources

### Handwritten Notes

* [Introduction to Stat. Mech.](../assets/notes/Notes-Intro_to_Stat_Mech.pdf)
* [Markvov Chain Monte Carlo](../assets/notes/Notes-Markov_Chain.pdf)

### Lecture Videos

**MCMC for Data Science**

[![](https://markdown-videos-api.jorgenkh.no/youtube/yApmR-c_hKU?width=720&height=405)](https://inv.tux.pizza/watch?v=yApmR-c_hKU)

- Non-Commercial Link: [https://inv.tux.pizza/watch?v=yApmR-c_hKU](https://inv.tux.pizza/watch?v=yApmR-c_hKU)
- Commercial Link: [https://youtube.com/watch?v=yApmR-c_hKU](https://youtube.com/watch?v=yApmR-c_hKU)

**Details on the MCMC Algorithm**

[![](https://markdown-videos-api.jorgenkh.no/youtube/rZk2FqX2XnY?width=720&height=405)](https://inv.tux.pizza/watch?v=rZk2FqX2XnY)

- Non-Commercial Link: [https://inv.tux.pizza/watch?v=rZk2FqX2XnY](https://inv.tux.pizza/watch?v=rZk2FqX2XnY)
- Commercial Link: [https://youtube.com/watch?v=rZk2FqX2XnY](https://youtube.com/watch?v=rZk2FqX2XnY)


