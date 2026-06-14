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
Hello everyone, my name is Zhongjian Zhang. Currently, I am a third-year Ph.D. student from Beijing University of Posts and Telecommunications (BUPT), supervised by [Prof. Chuan Shi](http://www.shichuan.org/ShiChuan_ch.html). My research interests primary focus on large language models and trustworthy graph machine learning. Specifically, my current research is mainly about the development of <strong>graph foundation model</strong>. <a class="scholar-stats" href="https://scholar.google.com/citations?user=XkeONm0AAAAJ" target="_blank" rel="noopener noreferrer" title="Google Scholar citations"><span class="scholar-stats__label"><i class="ai ai-google-scholar scholar-stats__icon" aria-hidden="true"></i>citations</span><span id="total_cit" class="scholar-stats__count">137</span></a><br /><span style="color: green;">If you have any questions regarding my work or are interested in collaborating with me, please feel free to contact me.</span>

<h1 id="-news" class="section-heading"><span class="section-heading__emoji">🔥</span><span class="section-heading__text">News</span></h1>

<div class="news-timeline">
  <div class="news-item news-item--featured">
    <div class="news-date">2026.03</div>
    <div class="news-content">🎉 Our papers <a href="https://dl.acm.org/doi/10.1145/3774904.3792832">FRiskGPT</a> and <a href="https://arxiv.org/abs/2603.01385">RGLM</a> are accepted to WWW 2026.</div>
  </div>
  <div class="news-item news-item--featured">
    <div class="news-date">2025.12</div>
    <div class="news-content">💼 I join the Hong Kong University of Science and Technology (Guangzhou) as a research intern, supervised by <a href="https://sites.google.com/view/lijia">Prof. Jia Li</a>.</div>
  </div>
  <div class="news-item news-item--featured">
    <div class="news-date">2025.12</div>
    <div class="news-content">🎉 My research is supported by the CAS Youth Talent Training Program for PhD Students.</div>
  </div>
  <div class="news-item">
    <div class="news-date">2025.10</div>
    <div class="news-content">🎉 I receive the National PhD Scholarship from the Ministry of Education of China.</div>
  </div>
  <div class="news-item">
    <div class="news-date">2025.04</div>
    <div class="news-content">🎉 My research is supported by the BUPT Excellent PhD Students Foundation: CX20251005.</div>
  </div>
  <div class="news-item">
    <div class="news-date">2024.12</div>
    <div class="news-content">🎉 Our paper <a href="https://arxiv.org/pdf/2501.03301">Spattack</a> is accepted to AAAI 2025.</div>
  </div>
  <div class="news-item">
    <div class="news-date">2024.11</div>
    <div class="news-content">🎉 Our paper <a href="https://arxiv.org/pdf/2408.08685">LLM4RGNN</a> is accepted to KDD 2025.</div>
  </div>
  <div class="news-item">
    <div class="news-date">2024.06</div>
    <div class="news-content">💼 I join China Telecommunications Corporation as a research intern.</div>
  </div>
  <div class="news-item">
    <div class="news-date">2024.01</div>
    <div class="news-content">🎉 Our paper <a href="https://arxiv.org/pdf/2402.12161">GraphPAR</a> is accepted to WWW 2024.</div>
  </div>
</div>

<h1 id="-publications" class="section-heading"><span class="section-heading__emoji">📝</span><span class="section-heading__text">Publications</span></h1>

<div class="paper-list">
  <article class="paper-item">
    <div class="paper-header">
      <div class="paper-title">FRiskGPT: A Generative Foundation Model for Financial Risk Detection</div>
      <span class="paper-badge">CCF-A</span>
    </div>
    <div class="paper-authors"><strong>Zhongjian Zhang</strong>, Mengmei Zhang, Dehua Xu, Rongjun Shi, Jianfeng Liu, Fuli Meng, Huajian Xu, Xiao Wang, Ruijia Wang, Junze Chen, Minwei Tang, Chuan Shi</div>
    <div class="paper-meta">WWW'26 · Deployed in China Telecom "BestPay" Risk Control System.</div>
    <div class="paper-links">
      <a href="https://dl.acm.org/doi/10.1145/3774904.3792832">Paper</a>
      <a href="https://mp.weixin.qq.com/s/1O1v2JeN_UvQuPzAjkp4Nw">Blog</a>
      <button class="bibtex-btn paper-link-button" data-bibtex="bibtex-friskgpt26" onclick="copyBibtex(this)">BibTeX</button>
    </div>
   {% raw %}<pre id="bibtex-friskgpt26" class="bibtex-content">@inproceedings{DBLP:conf/www/ZhangZXSLMXWWCT26,
  author       = {Zhongjian Zhang and
                  Mengmei Zhang and
                  Dehua Xu and
                  Rongjun Shi and
                  Jianfeng Liu and
                  Fuli Meng and
                  Huajian Xu and
                  Xiao Wang and
                  Ruijia Wang and
                  Junze Chen and
                  Minwei Tang and
                  Chuan Shi},
  editor       = {Hakim Hacid and
                  Yoelle Maarek and
                  Francesco Bonchi and
                  Ido Guy and
                  Emine Yilmaz},
  title        = {FRiskGPT: {A} Generative Foundation Model for Financial Risk Detection},
  booktitle    = {Proceedings of the {ACM} Web Conference 2026, {WWW} 2026, Dubai, United
                  Arab Emirates, originally scheduled for April 13-17, 2026, rescheduled
                  for June 29 - July 3, 2026},
  pages        = {7733--7744},
  publisher    = {{ACM}},
  year         = {2026},
  url          = {https://doi.org/10.1145/3774904.3792832},
  doi          = {10.1145/3774904.3792832},
  timestamp    = {Thu, 21 May 2026 17:35:30 +0200},
  biburl       = {https://dblp.org/rec/conf/www/ZhangZXSLMXWWCT26.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}</pre>{% endraw %}
  </article>

  <article class="paper-item">
    <div class="paper-header">
      <div class="paper-title">Toward Graph-Tokenizing Large Language Models with Reconstructive Graph Instruction Tuning</div>
      <span class="paper-badge">CCF-A</span>
    </div>
    <div class="paper-authors"><strong>Zhongjian Zhang</strong>, Xiao Wang, Mengmei Zhang, Jiarui Tan, Chuan Shi</div>
    <div class="paper-meta">WWW'26</div>
    <div class="paper-links">
      <a href="https://arxiv.org/abs/2603.01385">Paper</a>
      <a href="https://mp.weixin.qq.com/s/dlD4FAgOQM1LpFb1Ocogww">Blog</a>
      <a href="https://github.com/zhongjian-zhang/RGLM">Code</a>
      <button class="bibtex-btn paper-link-button" data-bibtex="bibtex-rglm26" onclick="copyBibtex(this)">BibTeX</button>
    </div>
   {% raw %}<pre id="bibtex-rglm26" class="bibtex-content">@inproceedings{DBLP:conf/www/ZhangWZTS26,
  author       = {Zhongjian Zhang and
                  Xiao Wang and
                  Mengmei Zhang and
                  Jiarui Tan and
                  Chuan Shi},
  editor       = {Hakim Hacid and
                  Yoelle Maarek and
                  Francesco Bonchi and
                  Ido Guy and
                  Emine Yilmaz},
  title        = {Toward Graph-Tokenizing Large Language Models with Reconstructive
                  Graph Instruction Tuning},
  booktitle    = {Proceedings of the {ACM} Web Conference 2026, {WWW} 2026, Dubai, United
                  Arab Emirates, originally scheduled for April 13-17, 2026, rescheduled
                  for June 29 - July 3, 2026},
  pages        = {430--441},
  publisher    = {{ACM}},
  year         = {2026},
  url          = {https://doi.org/10.1145/3774904.3792077},
  doi          = {10.1145/3774904.3792077},
  timestamp    = {Thu, 21 May 2026 17:35:20 +0200},
  biburl       = {https://dblp.org/rec/conf/www/ZhangWZTS26.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}</pre>{% endraw %}
  </article>

  <article class="paper-item">
    <div class="paper-header">
      <div class="paper-title">Can Large Language Models Improve the Adversarial Robustness of Graph Neural Networks?</div>
      <span class="paper-badge">CCF-A</span>
    </div>
    <div class="paper-authors"><strong>Zhongjian Zhang</strong>, Xiao Wang, Huichi Zhou, Yue Yu, Mengmei Zhang, Cheng Yang, Chuan Shi</div>
    <div class="paper-meta">KDD'25</div>
    <div class="paper-links">
      <a href="https://arxiv.org/pdf/2408.08685">Paper</a>
      <a href="https://mp.weixin.qq.com/s/P8e1n310Z08FJa65QGSjhQ">Blog</a>
      <a href="https://github.com/zhongjian-zhang/LLM4RGNN">Code</a>
      <button class="bibtex-btn paper-link-button" data-bibtex="bibtex-kdd25" onclick="copyBibtex(this)">BibTeX</button>
    </div>
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
  </article>

  <article class="paper-item">
    <div class="paper-header">
      <div class="paper-title">Rethinking Byzantine Robustness in Federated Recommendation from Sparse Aggregation Perspective</div>
      <span class="paper-badge">CCF-A</span>
    </div>
    <div class="paper-authors"><strong>Zhongjian Zhang</strong>, Mengmei Zhang, Xiao Wang, Lingjuan Lyu, Bo Yan, Junping Du, Chuan Shi</div>
    <div class="paper-meta">AAAI'25</div>
    <div class="paper-links">
      <a href="https://arxiv.org/pdf/2501.03301">Paper</a>
      <a href="https://mp.weixin.qq.com/s/5aicBY3UM9rv8KpDXYLrXQ">Blog</a>
      <a href="https://github.com/zhongjian-zhang/Spattack">Code</a>
      <button class="bibtex-btn paper-link-button" data-bibtex="bibtex-aaai25" onclick="copyBibtex(this)">BibTeX</button>
    </div>
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
  </article>

  <article class="paper-item">
    <div class="paper-header">
      <div class="paper-title">Endowing Pre-trained Graph Models with Provable Fairness</div>
      <span class="paper-badge">CCF-A</span>
    </div>
    <div class="paper-authors"><strong>Zhongjian Zhang</strong>, Mengmei Zhang, Yue Yu, Cheng Yang, Jiawei Liu, Chuan Shi</div>
    <div class="paper-meta">WWW'24</div>
    <div class="paper-links">
      <a href="https://arxiv.org/pdf/2402.12161">Paper</a>
      <a href="https://mp.weixin.qq.com/s/MUjScRy3FMxAHXIyuRqX5Q">Blog</a>
      <a href="https://github.com/BUPT-GAMMA/GraphPAR">Code</a>
      <button class="bibtex-btn paper-link-button" data-bibtex="bibtex-www24" onclick="copyBibtex(this)">BibTeX</button>
    </div>
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
  </article>

  <article class="paper-item">
    <div class="paper-header">
      <div class="paper-title">Data-centric graph learning: A survey</div>
      <span class="paper-badge">JCR-Q1</span>
    </div>
    <div class="paper-authors">Yuxin Guo, Deyu Bo, Cheng Yang, Zhiyuan Lu, <strong>Zhongjian Zhang</strong>, Jixi Liu, Yufei Peng, Chuan Shi</div>
    <div class="paper-meta">IEEE TBD'24</div>
    <div class="paper-links">
      <a href="https://arxiv.org/pdf/2310.04987">Paper</a>
      <a href="https://mp.weixin.qq.com/s/it15sa5TO0suZk2hj_Fkhw">Blog</a>
      <button class="bibtex-btn paper-link-button" data-bibtex="bibtex-tbd24" onclick="copyBibtex(this)">BibTeX</button>
    </div>
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
  </article>
</div>

<h1 id="-honors-and-awards" class="section-heading awards-list"><span class="section-heading__emoji">🎖</span><span class="section-heading__text">Honors and Awards</span></h1>

<div class="award-list">
  <div class="award-item"><span class="award-index">1</span><span class="award-title">CAST PhD Support Program, Youth Talent Development Initiative</span><span class="award-year">2025</span></div>
  <div class="award-item"><span class="award-index">2</span><span class="award-title">National PhD Scholarship, Ministry of Education of China</span><span class="award-year">2025</span></div>
  <div class="award-item"><span class="award-index">3</span><span class="award-title">BUPT Excellent Ph.D. Students Foundation (CX20251005)</span><span class="award-year">2025</span></div>
  <div class="award-item"><span class="award-index">4</span><span class="award-title">Outstanding Graduate Student, Beijing University of Posts and Telecommunications</span><span class="award-year">2024</span></div>
  <div class="award-item"><span class="award-index">5</span><span class="award-title">First-class Scholarship, Beijing University of Posts and Telecommunications</span><span class="award-year">2023</span></div>
  <div class="award-item"><span class="award-index">6</span><span class="award-title">Outstanding Student of Shandong Province (Top 0.5%)</span><span class="award-year">2022</span></div>
  <div class="award-item"><span class="award-index">7</span><span class="award-title">2nd Prize, 13th Lanqiao Cup National Finals, Java Software Development</span><span class="award-year">2022</span></div>
  <div class="award-item"><span class="award-index">8</span><span class="award-title">2nd Prize, National Final of Shandong Data Innovation Competition (Team Leader)</span><span class="award-year">2021</span></div>
  <div class="award-item"><span class="award-index">9</span><span class="award-title">1st Prize, Challenge Cup Shandong Province (Team Leader)</span><span class="award-year">2021</span></div>
  <div class="award-item"><span class="award-index">10</span><span class="award-title">Shandong Provincial Government Scholarship (Top 0.5%)</span><span class="award-year">2021</span></div>
</div>

<h1 id="-talks" class="section-heading"><span class="section-heading__emoji">💬</span><span class="section-heading__text">Talks</span></h1>

<div class="talk-list">
  <article class="talk-item">
    <div class="talk-date">2025.01</div>
    <div class="talk-body">
      <div class="talk-title">Rethinking Byzantine Robustness in Federated Recommendation from Sparse Aggregation Perspective</div>
      <div class="talk-meta">Invited Online Talk · AITIME</div>
    </div>
    <a class="talk-link" href="https://www.bilibili.com/video/BV1oGcEe6Eeq">Video</a>
  </article>
  <article class="talk-item">
    <div class="talk-date">2024.12</div>
    <div class="talk-body">
      <div class="talk-title">Can Large Language Models Improve the Adversarial Robustness of Graph Neural Networks?</div>
      <div class="talk-meta">Invited Online Talk · AITIME</div>
    </div>
    <a class="talk-link" href="https://www.bilibili.com/video/BV1uC6JY2E8U/">Video</a>
  </article>
</div>

<h1 id="-experiences" class="section-heading"><span class="section-heading__emoji">💻</span><span class="section-heading__text">Experiences</span></h1>

<div class="experience-list">
  <article class="experience-item">
    <div class="experience-side">
      <div class="experience-time">2024.06 - 2025.02</div>
      <span class="experience-logo-wrap"><img class="experience-logo" src="/images/Chinatelecom_logo.png" alt="China Telecom logo"></span>
    </div>
    <div class="experience-body">
      <div class="experience-heading">
        <div>
          <div class="experience-title">China Telecommunications Corporation</div>
          <div class="experience-location">Shanghai, China</div>
        </div>
      </div>
      <div class="experience-detail"><span>Research intern</span><strong>Financial Risk Service</strong></div>
      <div class="experience-detail"><span>Mentor</span><a href="https://scholar.google.com/citations?hl=zh-CN&user=8Qokm1IAAAAJ">Mengmei Zhang</a></div>
    </div>
  </article>
  <article class="experience-item">
    <div class="experience-side">
      <div class="experience-time">2025.12 - Now</div>
      <span class="experience-logo-wrap"><img class="experience-logo experience-logo--wide" src="/images/HKUST-GZ.svg" alt="HKUST Guangzhou logo"></span>
    </div>
    <div class="experience-body">
      <div class="experience-heading">
        <div>
          <div class="experience-title">Hong Kong University of Science and Technology (Guangzhou)</div>
          <div class="experience-location">Guangzhou, China</div>
        </div>
      </div>
      <div class="experience-detail"><span>Research intern</span><strong>Graph Foundation Model, Large Language Model</strong></div>
      <div class="experience-detail"><span>Mentor</span><a href="https://sites.google.com/view/lijia">Jia Li</a></div>
    </div>
  </article>
</div>
