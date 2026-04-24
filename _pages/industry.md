---
layout: archive
title: "R&D Experience"
permalink: /industry/
author_profile: true
---

After my postdoc in 2021, I moved into industry for a few years, driven by caring responsibilities that required more stability at the time.

---

## AI Innovation Senior Engineer — Verkor, Grenoble (2023–2024)

I worked on predictive ML systems for battery cell performance, at one of Europe's first large-scale gigafactories, during a critical scale-up phase.

The core scientific challenge was coordinating analysis from multiple physical machines across a pilot production line, while minimising the cost and complexity of approaches to allow their scaling in a gigafactory context. All of this in a fast-changing environment, where processes were continuously evolving and large volumes of data were accumulating in parallel.

I built monitoring and drift detection frameworks to track model performance over time in live production environments. I also developed internal reporting dashboards using Streamlit. The parallels with clinical research are real. In both settings, the data is noisy, the ground truth is hard to obtain, and the people who need to use the outputs are not data scientists. The stack included Python, Spark and Databricks, Docker, and Git/GitHub.

---

## Application Engineer – Data Scientist — Araymond Networks, Grenoble (2021–2023)

I worked on AI-based systems for manufacturing quality control, embedded within an internal startup incubator dedicated to translating scientific AI projects into field-deployable products.

The core problem was one of *machine health engineering*: detecting and characterising anomalous behaviour in production lines from multi-source sensor data, combining audio sensors and inertial sensors. The pipeline operated in stages. A first gate performed anomaly detection to flag abnormal signals. A second layer combined unsupervised clustering and supervised classification to characterise the nature of each defect. I also worked on optimising Design of Experiments (DoE) using Reinforcement Learning, reducing the number of physical tests needed during product qualification.

What I genuinely enjoyed in this role was working on the embedded sensors installed directly on production line equipment, which were the source of the raw signals I analysed. A key outcome was moving from blind, opportunistic data acquisition to a qualified, controlled acquisition strategy, selecting better-targeted data samples. This improved both the performance of the detection models and the cost-efficiency of the Design of Experiments in feasibility study scenarios. Working across data acquisition strategy, model development, and stakeholder communication required as much care on the engineering side as on the modelling side — and, it turns out, a fair amount of French-style diplomatic persistence. The stack included Python, MongoDB, Docker, and Git/GitHub.

---

What I took away from both experiences is simple. Getting a model to work in a real environment is a different problem from getting it to work on a dataset. The gap is mostly about engineering rigour, honest validation, and understanding the people who will actually use the outputs. I also learned the value of ambitious but well-designed research roadmaps: clear milestones, first-principles thinking, and fast iteration. Failing fast and learning faster is the shortest path from early prototype to mature, deployable solution. That has stayed with me in how I approach research.
