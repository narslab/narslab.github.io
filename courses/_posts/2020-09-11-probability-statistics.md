---
layout: course
title: "Probability and Statistics for Civil Engineers"
term: Fall 2020
sites:
  - term: Fall 2026
    url: https://fa26.probstats.narslab.org/
  - term: Fall 2025
    url: https://fa25.probstats.narslab.org/
---

Course websites:

{% for web in page.sites %}
- [{{ web.term }}]({{ web.url }})
{% endfor %}
