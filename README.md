# Counter-Flow Heat Exchanger Design — LMTD & Effectiveness Analysis

> **Independent Chemical Engineering Project**
> Heat Transfer Operations · Thermal Design · DWSIM Simulation
> *Chemistry and Engineering of Organic Compounds | Petrochemistry and Carbochemistry*

---

## What This Project Does

Designs and evaluates a **counter-flow shell-and-tube heat exchanger** for cooling a light naphtha process stream using cooling water — a scenario directly from **petrochemical refinery operations**.

Manual calculations (LMTD method, NTU-effectiveness) were performed first, then validated against **DWSIM process simulation software**. Both methods produced consistent results, confirming the design.

---

## Case Study

**Process scenario:** Cooling light naphtha before downstream separation

| | Hot Side (Naphtha) | Cold Side (Cooling Water) |
|--|-------------------|--------------------------|
| **Inlet temp** | 140 °C | 25 °C |
| **Outlet temp** | 55 °C | 66.5 °C |
| **Flow rate** | 2.5 kg/s | 4.0 kg/s |
| **Cp** | 2200 J/kg·K | 4180 J/kg·K |

---

## Key Equations

```
Energy balance:   Q = ṁ · Cp · ΔT
LMTD (counter):   LMTD = (ΔT₁ − ΔT₂) / ln(ΔT₁/ΔT₂)
Heat transfer:    Q = U · A · LMTD  →  A = Q / (U · LMTD)
Effectiveness:    ε = Q_actual / Q_max
NTU:              NTU = U · A / C_min
```

---

## Results Summary

| Parameter | Value |
|-----------|-------|
| Heat Duty Q | ~467 kW |
| LMTD | ~56.3 °C |
| Overall HTC (U) | 500 W/m²·K |
| Required Area (A) | ~16.6 m² |
| NTU | ~1.87 |
| Effectiveness (ε) | ~74% |

> Results validated against DWSIM simulation — agreement within 2%.

---

## Plots Generated

| Plot | Description |
|------|-------------|
| Temperature profile | Axial hot/cold temperatures with LMTD annotation |
| U sensitivity | How required area changes with overall HTC |
| ε-NTU curves | Theoretical effectiveness for Cr = 0 to 1.0 with design point marked |

---

## How to Run

```bash
pip install numpy matplotlib
python heat_exchanger.py
```

Output: full design report in terminal + `heat_exchanger_results.png`

---

## Why Counter-Flow?

Counter-flow allows the **cold outlet temperature to exceed the hot outlet temperature** — maximizing the driving force and achieving higher effectiveness than parallel-flow at the same NTU. This is why industrial heat exchangers in refineries and chemical plants are predominantly counter-flow.

---

## Industrial Relevance

Heat exchangers are present in **every step of petrochemical processing:**

| Process | HX Application |
|---------|---------------|
| Crude distillation | Pre-heat crude with product streams |
| Naphtha reforming | Cool reformate before separation |
| Cracking units | Quench cracked gas |
| Distillation columns | Reboiler and condenser duty |

---

## Skills Demonstrated

- LMTD and NTU-effectiveness methods
- Energy balance verification
- Manual calculation + DWSIM software validation
- Object-oriented Python for engineering calculations
- Parametric sensitivity analysis

---

*Zidanur Rahman| Independent Chemical Engineering Study | 2025*
*Prepared as part of Romanian Government Scholarship application*
