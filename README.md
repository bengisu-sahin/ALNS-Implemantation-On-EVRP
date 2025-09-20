# Adaptive Large Neighborhood Search Algorithm on EVRP

## 📖 Introduction

This repository has been prepared as part of our **graduation project** at **Eskişehir Osmangazi University**, in collaboration with **[OPEVA](https://www.opeva.eu/)**, within the scope of a **European-supported project**.

The project focuses on the implementation of the **Adaptive Large Neighborhood Search (ALNS)** algorithm for the **Electric Vehicle Routing Problem (EVRP)**. While the final target is to optimize routes on the **Eskişehir Osmangazi University Campus**, the methodology was first tested on **benchmark datasets** from the literature.

In addition to the standard ALNS framework, extra requirements defined by the European project have been incorporated.

---

## 🎯 Research Objectives

* Implement and evaluate the **ALNS algorithm** on EVRP.
* Validate the algorithm using **benchmark datasets**.
* Apply the solution to **Eskişehir Osmangazi University Campus** data.
* Extend ALNS with **problem-specific operators and constraints**.

---

## 📂 Repository Structure

```bash
├── AlnsObjects/             # Data structures for ALNS
├── AlnsOperators/           # Destroy & repair operators
├── DataObjects/             # Input/output data utilities
├── EVRPTW_Verifier/         # EVRP with Time Windows verifier
├── SchneiderData/           # Benchmark dataset (Schneider instances)
├── html/                    # Visualization and reports
│
├── alnsSolution.py          # ALNS main solution file
├── initialsolution.py       # Initial solution construction
├── main.py                  # Entry point to run experiments
├── problemInstances.py      # Problem instance definitions
├── readProblemInstances.py  # Dataset parsing functions
├── test_funcs.py            # Functions for testing operators
├── visualize_solution.py    # Visualization of EVRP routes
│
├── requirements.txt         # Python dependencies
├── solution.txt             # Example solution output
├── LICENSE                  # License file
└── README.md                # Documentation
```

# Methodology

The methodology of this project is based on the **Adaptive Large Neighborhood Search (ALNS)** algorithm, applied to the **Electric Vehicle Routing Problem (EVRP)**. The benchmark datasets used are the Schneider instances, in addition to a custom dataset representing the Eskişehir Osmangazi University Campus. For solution verification, an **EVRPTW verifier** has been implemented to ensure correctness. Furthermore, the project includes visualization of routes and solution comparisons.

The ALNS framework iteratively improves solutions by applying **destroy and repair operators** in a controlled adaptive manner. The campus-based EVRP scenario introduces additional constraints such as **charging station limitations** and **campus-specific vehicle routing requirements**, making the problem more realistic and challenging.

---

## 🚀 Usage

Clone the repository:

```bash
git clone https://github.com/bengisu-sahin/ALNS-Implemantation-On-EVRP
cd repo-name
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the main experiment:

```bash
python main.py
```

---

## 📊 Research Materials

* 🎤 [Project Presentation (Google Drive)](https://docs.google.com/presentation/d/1ZwO0gDlUvesnyPzUUhBVpq6lENX3-nRXwtNdbIHDjTo/edit?usp=sharing)

---

## 👥 Contributors

* 👨‍💻 [Yağız Harman](https://github.com/yagizharman) – Eskişehir Osmangazi University (Computer Engineering), BSc.
* 👩‍💻 [Bengisu Şahin](https://github.com/bengisu-sahin) – Eskişehir Osmangazi University (Computer Engineering), BSc.

---

## 🏢 Collaboration with **[OPEVA](https://www.opeva.eu/)**

We were the two students specially selected by our professors to complete our graduation project within the scope of the Horizon European program called Optimization of Electric Vehicle Autonomy (OPEVA). This project included Eskişehir Osmangazi University, the only participating university from our country, and involved 35 participants from 9 countries, jointly supported by the national authorities of the participating countries. As part of this project, we worked under the supervision of Asst. Prof. Sinem Bozkurt Keser and the management of Prof. Dr. Ahmet Yazıcı.

---

## 📜 Citation

If you use this work in your research, please cite as:

```text
[[Bengisu Şahin](https://github.com/bengisu-sahin)], [[Yağız Harman](https://github.com/yagizharman)], "Adaptive Large Neighborhood Search Algorithm Implementation on EVRP", 
Graduation Project, Eskişehir Osmangazi University, 2024.
```

---

## 📄 License

This repository is released under the **MIT License**.
