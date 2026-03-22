---
permalink: /
title: ""
excerpt: ""
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

{% if site.google_scholar_stats_use_cdn %}
{% assign gsDataBaseUrl = "https://cdn.jsdelivr.net/gh/" | append: site.repository | append: "@" %}
{% else %}
{% assign gsDataBaseUrl = "https://raw.githubusercontent.com/" | append: site.repository | append: "/" %}
{% endif %}
{% assign url = gsDataBaseUrl | append: "google-scholar-stats/gs_data_shieldsio.json" %}

<span class='anchor' id='about-me'></span>

[//]: # (# 👨🏻‍🎓 About Me)
Hello everyone, my name is Zhongjian Zhang. Currently, I am a third-year Ph.D. student from Beijing University of Posts and Telecommunications (BUPT), supervised by [Prof. Chuan Shi](http://www.shichuan.org/ShiChuan_ch.html). My research interests primary focus on large language models and trustworthy graph machine learning. Specifically, my current research is mainly about the development of **graph foundation model**. <span style="color: green;">If you have any questions regarding my work or are interested in collaborating with me, please feel free to contact me via:</span>

- Email: zhangzj@bupt.edu.cn
- Wechat: zxc1957787636

# 🔥 News
- [*2026.03*] 🎉 Our papers [FRiskGPT]() and [RGLM](https://arxiv.org/abs/2603.01385) are accepted to WWW 2026.
- [*2025.12*] 💼  I join the Hong Kong University of Science and Technology (Guangzhou) as a research intern, supervised by [Prof. Jia Li](https://sites.google.com/view/lijia).
- [*2025.12*] 🎉 My research is supported by the CAS Youth Talent Training Program for PhD Students.
- [*2025.10*] 🎉 I receive the National PhD Scholarship from the Ministry of Education of China.
- [*2025.04*] 🎉 My research is supported by the BUPT Excellent PhD Students Foundation: CX20251005.
- [*2024.12*] 🎉 Our paper [Spattack](https://arxiv.org/pdf/2501.03301) is accepted to AAAI 2025.
- [*2024.11*] 🎉 Our paper [LLM4RGNN](https://arxiv.org/pdf/2408.08685) is accepted to KDD 2025.
- [*2024.06*] 💼 I join China Telecommunications Corporation as a research intern.
- [*2024.01*] 🎉 Our paper [GraphPAR](https://arxiv.org/pdf/2402.12161) is accepted to WWW 2024.

# 📝 Publications

1. FRiskGPT: A Generative Foundation Model for Financial Risk Detection (**<span style="color: red;">CCF-A</span>**)
   - **Zhongjian Zhang**, Mengmei Zhang, Dehua Xu, Rongjun Shi, Jianfeng Liu, Fuli Meng, Huajian Xu, Xiao Wang, Ruijia Wang, Junze Chen, Minwei Tang, Chuan Shi
   - WWW'26. Deployed in China Telecom "BestPay" Risk Control System.

2. Toward Graph-Tokenizing Large Language Models with Reconstructive Graph Instruction Tuning (**<span style="color: red;">CCF-A</span>**)
   - **Zhongjian Zhang**, Xiao Wang, Mengmei Zhang, Jiarui Tan, Chuan Shi
   - WWW'26 \[[Paper](https://arxiv.org/abs/2603.01385)\]\|[Code](https://github.com/zhongjian-zhang/RGLM)\]

3. Can Large Language Models Improve the Adversarial Robustness of Graph Neural Networks? (**<span style="color: red;">CCF-A</span>**)
   - **Zhongjian Zhang**, Xiao Wang, Huichi Zhou, Yue Yu, Mengmei Zhang, Cheng Yang, Chuan Shi
   - KDD'25 \[[Paper](https://arxiv.org/pdf/2408.08685)\]\|[Blog](https://mp.weixin.qq.com/s/P8e1n310Z08FJa65QGSjhQ)\]\|[Code](https://github.com/zhongjian-zhang/LLM4RGNN)\]\|[<button class="bibtex-btn" data-bibtex="bibtex-kdd25" onclick="copyBibtex(this)">BibTeX</button>\]
   {% raw %}<pre id="bibtex-kdd25" class="bibtex-content">@inproceedings{DBLP:conf/kdd/Zhang0Z0Z0025,
  author       = {Zhongjian Zhang and
                  Xiao Wang and
                  Huichi Zhou and
                  Yue Yu and
                  Mengmei Zhang and
                  Cheng Yang and
                  Chuan Shi},
  title        = {Can Large Language Models Improve the Adversarial Robustness of Graph
                  Neural Networks?},
  booktitle    = {Proceedings of the 31st {ACM} {SIGKDD} Conference on Knowledge Discovery
                  and Data Mining, V.1, {KDD} 2025, Toronto, ON, Canada, August 3-7,
                  2025},
  pages        = {2008--2019},
  publisher    = {{ACM}},
  year         = {2025},
  url          = {https://doi.org/10.1145/3690624.3709256},
  doi          = {10.1145/3690624.3709256}
}</pre>{% endraw %}

4. Rethinking Byzantine Robustness in Federated Recommendation from Sparse Aggregation Perspective (**<span style="color: red;">CCF-A</span>**)
   - **Zhongjian Zhang**, Mengmei Zhang, Xiao Wang, Lingjuan Lyu, Bo Yan, Junping Du, Chuan Shi
   - AAAI'25 \[[Paper](https://arxiv.org/pdf/2501.03301)\]\|[Blog](https://mp.weixin.qq.com/s/5aicBY3UM9rv8KpDXYLrXQ)\]\|[Code](https://github.com/zhongjian-zhang/Spattack)\]\|[<button class="bibtex-btn" data-bibtex="bibtex-aaai25" onclick="copyBibtex(this)">BibTeX</button>\]
   {% raw %}<pre id="bibtex-aaai25" class="bibtex-content">@inproceedings{DBLP:conf/aaai/ZhangZWL00025,
  author       = {Zhongjian Zhang and
                  Mengmei Zhang and
                  Xiao Wang and
                  Lingjuan Lyu and
                  Bo Yan and
                  Junping Du and
                  Chuan Shi},
  title        = {Rethinking Byzantine Robustness in Federated Recommendation from Sparse
                  Aggregation Perspective},
  booktitle    = {Thirty-Ninth {AAAI} Conference on Artificial Intelligence, {AAAI} 2025, Philadelphia, PA, USA, February 25 - March 4, 2025},
  pages        = {13331--13338},
  publisher    = {{AAAI} Press},
  year         = {2025},
  url          = {https://doi.org/10.1609/aaai.v39i12.33455},
  doi          = {10.1609/AAAI.V39I12.33455}
}</pre>{% endraw %}

5. Endowing Pre-trained Graph Models with Provable Fairness (**<span style="color: red;">CCF-A</span>**)
   - **Zhongjian Zhang**, Mengmei Zhang, Yue Yu, Cheng Yang, Jiawei Liu, Chuan Shi
   - WWW'24 \[[Paper](https://arxiv.org/pdf/2402.12161)\]\|[Blog](https://mp.weixin.qq.com/s/MUjScRy3FMxAHXIyuRqX5Q)\]\|[Code](https://github.com/BUPT-GAMMA/GraphPAR)\]\|[<button class="bibtex-btn" data-bibtex="bibtex-www24" onclick="copyBibtex(this)">BibTeX</button>\]
   {% raw %}<pre id="bibtex-www24" class="bibtex-content">@inproceedings{DBLP:conf/www/ZhangZYYLS24,
  author       = {Zhongjian Zhang and
                  Mengmei Zhang and
                  Yue Yu and
                  Cheng Yang and
                  Jiawei Liu and
                  Chuan Shi},
  title        = {Endowing Pre-trained Graph Models with Provable Fairness},
  booktitle    = {Proceedings of the {ACM} on Web Conference 2024, {WWW} 2024, Singapore,
                  May 13-17, 2024},
  pages        = {1045--1056},
  publisher    = {{ACM}},
  year         = {2024},
  url          = {https://doi.org/10.1145/3589334.3645703},
  doi          = {10.1145/3589334.3645703}
}</pre>{% endraw %}

6. Data-centric graph learning: A survey
   - Yuxin Guo, Deyu Bo, Cheng Yang, Zhiyuan Lu, **Zhongjian Zhang**, Jixi Liu, Yufei Peng, Chuan Shi
   - IEEE TBD'24 \[[Paper](https://arxiv.org/pdf/2310.04987)\]\|[Blog](https://mp.weixin.qq.com/s/it15sa5TO0suZk2hj_Fkhw)\]\|[<button class="bibtex-btn" data-bibtex="bibtex-tbd24" onclick="copyBibtex(this)">BibTeX</button>\]
   {% raw %}<pre id="bibtex-tbd24" class="bibtex-content">@article{DBLP:journals/tbd/GuoBYLZLPS25,
  author       = {Yuxin Guo and
                  Deyu Bo and
                  Cheng Yang and
                  Zhiyuan Lu and
                  Zhongjian Zhang and
                  Jixi Liu and
                  Yufei Peng and
                  Chuan Shi},
  title        = {Data-Centric Graph Learning: {A} Survey},
  journal      = {{IEEE} Trans. Big Data},
  volume       = {11},
  number       = {1},
  pages        = {1--20},
  year         = {2025},
  url          = {https://doi.org/10.1109/TBDATA.2024.3489412},
  doi          = {10.1109/TBDATA.2024.3489412}
}</pre>{% endraw %}

# 🏆 Honors and Awards
{: .awards-list}

1. <span class="award-item"><span class="award-title">CAST PhD Support Program, Youth Talent Development Initiative</span><span class="award-year">2025</span></span>
2. <span class="award-item"><span class="award-title">National PhD Scholarship, Ministry of Education of China</span><span class="award-year">2025</span></span>
3. <span class="award-item"><span class="award-title">BUPT Excellent Ph.D. Students Foundation (CX20251005)</span><span class="award-year">2025</span></span>
4. <span class="award-item"><span class="award-title">Outstanding Graduate Student, Beijing University of Posts and Telecommunications</span><span class="award-year">2024</span></span>
5. <span class="award-item"><span class="award-title">First-class Scholarship, Beijing University of Posts and Telecommunications</span><span class="award-year">2023</span></span>
6. <span class="award-item"><span class="award-title">Outstanding Student of Shandong Province (Top 0.5%)</span><span class="award-year">2022</span></span>
7. <span class="award-item"><span class="award-title">2nd Prize, 13th Lanqiao Cup National Finals, Java Software Development</span><span class="award-year">2022</span></span>
8. <span class="award-item"><span class="award-title">2nd Prize, National Final of Shandong Data Innovation Competition (Team Leader)</span><span class="award-year">2021</span></span>
9. <span class="award-item"><span class="award-title">1st Prize, Challenge Cup Shandong Province (Team Leader)</span><span class="award-year">2021</span></span>
10. <span class="award-item"><span class="award-title">Shandong Provincial Government Scholarship (Top 0.5%)</span><span class="award-year">2021</span></span>

# 💬 Talks
- *2025.01*, Rethinking Byzantine Robustness in Federated Recommendation from Sparse Aggregation Perspective, Invited Online Talk at AITIME. \[[video](https://www.bilibili.com/video/BV1oGcEe6Eeq)\]
- *2024.12*, Can Large Language Models Improve the Adversarial Robustness of Graph Neural Networks?, Invited Online Talk at AITIME. \[[video](https://www.bilibili.com/video/BV1uC6JY2E8U/)\]

# 💻 Experiences
- *2024.06 - 2025.02*, China Telecommunications Corporation, China
  - Research intern: Financial Risk Service
  - Mentor: [Mengmei Zhang](https://scholar.google.com/citations?hl=zh-CN&user=8Qokm1IAAAAJ)

- *2025.12 - Now*, Hong Kong University of Science and Technology (Guangzhou), China
  - Research intern: Graph Foundation Model, Large Language Model
  - Mentor: [Jia Li](https://sites.google.com/view/lijia)