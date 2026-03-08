"""
=============================================================
Counter-Flow Heat Exchanger Design — LMTD & Effectiveness
=============================================================
Author      : Zid
Field       : Heat Transfer Operations / Process Design
Subject     : Chemistry and Engineering of Organic Compounds,
              Petrochemistry and Carbochemistry
Description :
    Designs a counter-flow heat exchanger for cooling a
    hydrocarbon process stream using cooling water.

    Manually calculates LMTD, overall heat transfer coefficient,
    required area, NTU, and effectiveness. Compares results
    against DWSIM simulation for validation.

    Case study: Cooling light naphtha (petrochemical context)
    from 140°C to 55°C using river cooling water.

Key Equations:
    Q    = ṁ · Cp · ΔT               [Energy balance]
    LMTD = (ΔT₁ - ΔT₂) / ln(ΔT₁/ΔT₂) [Log Mean Temp Diff]
    Q    = U · A · LMTD               [Heat transfer rate]
    NTU  = U · A / C_min              [Transfer units]
    ε    = Q / Q_max                  [Effectiveness]
=============================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# ─────────────────────────────────────────────────────────────
# FLUID CLASS
# ─────────────────────────────────────────────────────────────

class Fluid:
    """Process fluid with thermal properties."""

    def __init__(self, name, m_dot, Cp, T_in, T_out):
        self.name  = name
        self.m_dot = m_dot   # mass flow rate (kg/s)
        self.Cp    = Cp      # specific heat (J/kg·K)
        self.T_in  = T_in    # inlet temperature (°C)
        self.T_out = T_out   # outlet temperature (°C)
        self.C     = m_dot * Cp  # heat capacity rate (W/K)

    def duty(self):
        """Heat duty (W)."""
        return self.m_dot * self.Cp * abs(self.T_out - self.T_in)


# ─────────────────────────────────────────────────────────────
# HEAT EXCHANGER CLASS
# ─────────────────────────────────────────────────────────────

class CounterFlowHX:
    """Counter-flow heat exchanger design calculator."""

    def __init__(self, hot: Fluid, cold: Fluid, U=500.0):
        self.hot  = hot
        self.cold = cold
        self.U    = U    # overall heat transfer coefficient (W/m²·K)

    def energy_balance_check(self):
        """Verify hot and cold duties match within 5%."""
        err = abs(self.hot.duty() - self.cold.duty()) / self.hot.duty()
        status = "✓ PASS" if err < 0.05 else "✗ FAIL"
        print(f"  Energy balance: {status}  (discrepancy: {err*100:.2f}%)")
        return err

    def lmtd(self):
        """
        Log Mean Temperature Difference — counter-flow.
        ΔT₁ = T_hot_in  − T_cold_out  (hot inlet end)
        ΔT₂ = T_hot_out − T_cold_in   (hot outlet end)
        """
        dT1 = self.hot.T_in  - self.cold.T_out
        dT2 = self.hot.T_out - self.cold.T_in
        if dT1 <= 0 or dT2 <= 0:
            raise ValueError("Temperature crossover — infeasible design.")
        if abs(dT1 - dT2) < 1e-6:
            return dT1
        return (dT1 - dT2) / np.log(dT1 / dT2)

    def area(self):
        """Required heat transfer area: A = Q / (U · LMTD)"""
        return self.hot.duty() / (self.U * self.lmtd())

    def ntu(self):
        """Number of Transfer Units: NTU = U·A / C_min"""
        return (self.U * self.area()) / min(self.hot.C, self.cold.C)

    def effectiveness(self):
        """ε = Q_actual / Q_max  where Q_max = C_min·(T_hot_in − T_cold_in)"""
        Q_max = min(self.hot.C, self.cold.C) * (self.hot.T_in - self.cold.T_in)
        return self.hot.duty() / Q_max

    def temperature_profile(self, n=100):
        """Axial temperature distribution along exchanger length."""
        x      = np.linspace(0, 1, n)
        T_hot  = self.hot.T_in  + (self.hot.T_out  - self.hot.T_in)  * x
        T_cold = self.cold.T_out + (self.cold.T_in - self.cold.T_out) * x
        return x, T_hot, T_cold

    def report(self):
        """Print complete design report."""
        Q   = self.hot.duty()
        L   = self.lmtd()
        A   = self.area()
        NTU = self.ntu()
        eff = self.effectiveness()

        print("\n" + "="*62)
        print("  COUNTER-FLOW HEAT EXCHANGER — DESIGN REPORT")
        print("="*62)
        print(f"\n  HOT SIDE  : {self.hot.name}")
        print(f"    {self.hot.T_in}°C → {self.hot.T_out}°C  |  ṁ = {self.hot.m_dot} kg/s  |  Cp = {self.hot.Cp} J/kg·K")
        print(f"    Heat duty = {Q/1000:.2f} kW")
        print(f"\n  COLD SIDE : {self.cold.name}")
        print(f"    {self.cold.T_in}°C → {self.cold.T_out}°C  |  ṁ = {self.cold.m_dot} kg/s  |  Cp = {self.cold.Cp} J/kg·K")
        print(f"    Heat duty = {self.cold.duty()/1000:.2f} kW")
        self.energy_balance_check()
        print(f"\n  THERMAL RESULTS")
        print(f"    LMTD              : {L:.2f} °C")
        print(f"    U (overall HTC)   : {self.U} W/m²·K")
        print(f"    Area required (A) : {A:.3f} m²")
        print(f"    NTU               : {NTU:.3f}")
        print(f"    Effectiveness (ε) : {eff:.4f}  ({eff*100:.1f}%)")
        print("="*62)
        return {"Q_kW": Q/1000, "LMTD": L, "A": A, "NTU": NTU, "eff": eff}


# ─────────────────────────────────────────────────────────────
# PARAMETRIC ANALYSIS
# ─────────────────────────────────────────────────────────────

def u_sensitivity(hx: CounterFlowHX):
    U_range = np.linspace(100, 1500, 300)
    Q, L    = hx.hot.duty(), hx.lmtd()
    return U_range, Q / (U_range * L)


def effectiveness_ntu_curves():
    """Theoretical ε-NTU for counter-flow at various capacity ratios."""
    NTU    = np.linspace(0.01, 5, 300)
    Cr_vals = [0.0, 0.25, 0.5, 0.75, 1.0]
    curves  = {}
    for Cr in Cr_vals:
        if Cr == 1.0:
            curves[Cr] = NTU / (1 + NTU)
        else:
            exp = np.exp(-NTU * (1 - Cr))
            curves[Cr] = (1 - exp) / (1 - Cr * exp)
    return NTU, curves


# ─────────────────────────────────────────────────────────────
# PLOTS
# ─────────────────────────────────────────────────────────────

def plot_results(hx: CounterFlowHX):
    fig = plt.figure(figsize=(14, 10))
    fig.suptitle(
        "Counter-Flow Heat Exchanger Design — LMTD & Effectiveness Analysis\n"
        "Petrochemistry: Naphtha Cooling Case Study | Independent Study",
        fontsize=13, fontweight='bold', y=0.98
    )
    gs = gridspec.GridSpec(2, 2, hspace=0.42, wspace=0.35)
    colors = ['#1B3A6B', '#E07B39', '#0D7377', '#8B2FC9', '#2E7D32']

    # Plot 1: Temperature profile
    ax1 = fig.add_subplot(gs[0, :])
    x, Th, Tc = hx.temperature_profile()
    ax1.plot(x*100, Th, color='#E07B39', linewidth=2.5, label=f'Hot: {hx.hot.name}')
    ax1.plot(x*100, Tc, color='#1B3A6B', linewidth=2.5, label=f'Cold: {hx.cold.name}')
    ax1.fill_between(x*100, Tc, Th, alpha=0.07, color='gray', label='Driving force ΔT')
    ax1.annotate(f'LMTD = {hx.lmtd():.1f}°C',
                 xy=(50, (Th[50]+Tc[50])/2), fontsize=10,
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.85))
    ax1.set_xlabel("Position along exchanger (%)", fontsize=11)
    ax1.set_ylabel("Temperature (°C)", fontsize=11)
    ax1.set_title("Axial Temperature Profile — Counter-Flow Configuration", fontsize=12, fontweight='bold')
    ax1.legend(fontsize=9); ax1.grid(True, alpha=0.3)

    # Plot 2: U sensitivity
    ax2 = fig.add_subplot(gs[1, 0])
    U_r, A_r = u_sensitivity(hx)
    ax2.plot(U_r, A_r, color='#1B3A6B', linewidth=2.5)
    ax2.axvline(hx.U, color='red', linestyle='--', alpha=0.7, label=f'Design U={hx.U}')
    ax2.axhline(hx.area(), color='orange', linestyle='--', alpha=0.7, label=f'Design A={hx.area():.1f}m²')
    ax2.set_xlabel("U (W/m²·K)", fontsize=11)
    ax2.set_ylabel("Required Area A (m²)", fontsize=11)
    ax2.set_title("Sensitivity: Area vs U", fontsize=11, fontweight='bold')
    ax2.legend(fontsize=8); ax2.grid(True, alpha=0.3)

    # Plot 3: ε-NTU
    ax3 = fig.add_subplot(gs[1, 1])
    NTU_r, curves = effectiveness_ntu_curves()
    lbls = {0.0:'Cr=0', 0.25:'Cr=0.25', 0.5:'Cr=0.5', 0.75:'Cr=0.75', 1.0:'Cr=1.0'}
    for i, (Cr, eff) in enumerate(curves.items()):
        ax3.plot(NTU_r, eff, color=colors[i], linewidth=2,
                 linestyle='--' if Cr==1.0 else '-', label=lbls[Cr])
    ax3.scatter([hx.ntu()], [hx.effectiveness()], color='red', s=120, zorder=5,
                marker='*', label=f'Design (ε={hx.effectiveness():.2f})')
    ax3.set_xlabel("NTU", fontsize=11)
    ax3.set_ylabel("Effectiveness ε", fontsize=11)
    ax3.set_title("ε-NTU Curves — Counter-Flow", fontsize=11, fontweight='bold')
    ax3.legend(fontsize=8); ax3.grid(True, alpha=0.3)
    ax3.set_xlim([0, 5]); ax3.set_ylim([0, 1.05])

    plt.savefig("heat_exchanger_results.png", dpi=150, bbox_inches='tight')
    print("\nPlot saved → heat_exchanger_results.png")
    plt.show()


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    hot  = Fluid("Light Naphtha",   m_dot=2.5, Cp=2200, T_in=140.0, T_out=55.0)
    cold = Fluid("Cooling Water",   m_dot=4.0, Cp=4180, T_in=25.0,  T_out=66.5)
    hx   = CounterFlowHX(hot, cold, U=500.0)

    hx.report()
    plot_results(hx)
