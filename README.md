# Mathematical Methods for Physicists (PHY 415)

Welcome to the course materials for PHY 415: Mathematical Methods for Physicists, a comprehensive exploration of mathematical approaches used throughout physics.

## 📚 About This Repository

This repository contains the complete course materials for [PHY 415 (Fall 2023)](https://openphysicsed.org/), a course designed to bring together mathematical approaches commonly used in physics and apply them to a variety of problems. The site is built with [Hugo](https://gohugo.io/) and features interactive notes, activities, and assignments.

- **Course Title:** Mathematical Methods for Physicists
- **Instructors:** Danny Caballero, Alia Valentine
- **Content:** Lecture notes, activities, problem sets, and projects
- **Audience:** Physics students and anyone interested in mathematical modeling in physics

## 🧭 Structure

- `content/` — All course content organized by unit
  - `0---intro-and-syllabus/` — Course overview, learning objectives, and syllabus
  - `1---mechanics-and-odes/` — Mechanics, differential equations, and phase space analysis
  - `2---em-and-pdes/` — Electromagnetism and partial differential equations
  - `3---waves-and-oscillations/` — Wave equations, Fourier methods, and FFT
  - `4---randomness-and-distributions/` — Probability, distributions, and stochastic models
  - `assignments/` — Problem sets and projects
  - `appendices/` — Reference materials and supplementary topics
- `layouts/` — Custom Hugo templates for course content
- `static/` — Images, diagrams, and static assets
- `config.toml` — Hugo configuration

## 📖 Course Units

**Unit 1: Mechanics and ODEs** – Covers coordinate systems, Lagrangian mechanics, numerical integration, phase space analysis, and nonlinear dynamics (linearization, Van der Pol oscillator, Duffing oscillator).

**Unit 2: E&M and PDEs** – Explores electromagnetic fields, electric potential, boundary value problems using separation of variables, relaxation methods, and numerical solutions in Cartesian and spherical coordinates.

**Unit 3: Waves and Oscillations** – Investigates coupled oscillations, wave equations, solving wave equations analytically, Fourier methods, signal analysis, and fast Fourier transforms (FFT).

**Unit 4: Randomness and Distributions** – Examines probability, probability distributions, statistical modeling, and stochastic differential equations.

## 🚀 Building the Site

This site uses [Hugo](https://gohugo.io/). To build and serve locally:

```sh
hugo server
```

The site will be available at `http://localhost:1313/`.

To build for production:

```sh
hugo
```

This generates the static site in the `public/` directory.

## 📄 License

Content is licensed under the [MIT License](https://opensource.org/licenses/MIT).
