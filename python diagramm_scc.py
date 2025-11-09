import matplotlib.pyplot as plt

# 🔹 Daten aus deinen echten Messungen
graph_types = ["klein", "klein", "klein", "mittel", "mittel", "mittel", "groß", "groß", "groß"]

tarjan_memory = [1.46, 1.91, 2.33, 6.94, 14.34, 29.57, 436.00, 884.23, 1781.13]
kosaraju_memory = [2.63, 3.39, 4.52, 18.09, 35.58, 49.94, 1001.30, 2006.99, 4039.40]

tarjan_time = [0.090, 0.061, 0.114, 0.237, 0.487, 1.610, 217.407, 998.837, 3930.401]
kosaraju_time = [0.116, 0.115, 0.153, 0.456, 1.025, 1.983, 224.841, 794.369, 3174.868]

x = range(len(graph_types))
bar_width = 0.35

# ---------- Hilfsfunktion zum Anzeigen der Werte über den Balken ----------
def add_values(bars):
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2,
            height,
            f"{height:.1f}",
            ha='center',
            va='bottom',
            fontsize=8
        )

# ---------- 1. Diagramm: Speicherverbrauch ----------
plt.figure(figsize=(9, 5))
bars1 = plt.bar([i - bar_width/2 for i in x], tarjan_memory, width=bar_width, color="#4f9ccf", label="Tarjan")
bars2 = plt.bar([i + bar_width/2 for i in x], kosaraju_memory, width=bar_width, color="#1f77b4", label="Kosaraju")
add_values(bars1)
add_values(bars2)
plt.xticks(x, graph_types, rotation=30)
plt.xlabel("Graphgröße")
plt.ylabel("Speicherverbrauch (KB)")
plt.title("Vergleich des Speicherverbrauchs – Tarjan vs. Kosaraju")
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("speicher_diagramm.png", dpi=300)
plt.show()

# ---------- 2. Diagramm: Laufzeit ----------
plt.figure(figsize=(9, 5))
bars3 = plt.bar([i - bar_width/2 for i in x], tarjan_time, width=bar_width, color="#4f9ccf", label="Tarjan")
bars4 = plt.bar([i + bar_width/2 for i in x], kosaraju_time, width=bar_width, color="#1f77b4", label="Kosaraju")
add_values(bars3)
add_values(bars4)
plt.xticks(x, graph_types, rotation=30)
plt.xlabel("Graphgröße")
plt.ylabel("Laufzeit (ms)")
plt.title("Vergleich der Laufzeit – Tarjan vs. Kosaraju")
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("laufzeit_diagramm.png", dpi=300)
plt.show()

print("✅ Diagramme wurden erfolgreich gespeichert:")
print("   - speicher_diagramm.png")
print("   - laufzeit_diagramm.png")

