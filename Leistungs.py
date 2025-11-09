import random          # Modul für Zufallszahlen → wir brauchen das, um zufällige gerichtete Graphen zu erzeugen
import time            # Modul für Zeitmessung → damit messen wir, wie lange ein Algorithmus braucht
import tracemalloc     # Modul zur Überwachung von Speicherverbrauch in Python
import sys             # Modul für systemnahe Funktionen (hier: Rekursionslimit ändern)

sys.setrecursionlimit(20000)  # erhöht die maximale Rekursionstiefe, damit die DFS auch bei großen Graphen nicht abstürzt
                             # Standard in Python ist ca. 1000 – für 20.000 Knoten ist das zu wenig
                             # wir brauchen das vor allem für Tarjan, weil er rekursiv arbeitet


# ---------- Graph erzeugen ----------
def make_random_digraph(n, m):
    """Erzeugt einen zufälligen gerichteten Graphen mit n Knoten und m Kanten."""
    g = [[] for _ in range(n)]      # legt eine Adjazenzliste an: für jeden Knoten eine leere Liste der Nachbarn
    for _ in range(m):              # wir fügen jetzt m Kanten hinzu
        u = random.randrange(n)     # zufälliger Startknoten (0 … n-1)
        v = random.randrange(n)     # zufälliger Zielknoten (0 … n-1)
        g[u].append(v)              # füge gerichtete Kante u -> v ein
    return g                        # gib den erzeugten Graphen zurück


# ---------- Tarjan ----------
def tarjan_scc(graph):
    """Implementierung des Tarjan-Algorithmus zur Bestimmung starker Zusammenhangskomponenten."""
    n = len(graph)                  # Anzahl der Knoten
    index = 0                       # globaler Zähler für die Besuchsreihenfolge
    stack = []                      # Stack, auf dem aktuell offene Knoten liegen
    on_stack = [False] * n          # Merker: liegt der Knoten gerade auf dem Stack?
    indices = [-1] * n              # für jeden Knoten: Besuchsindex (anfangs -1 = nicht besucht)
    lowlink = [0] * n               # für jeden Knoten: niedrigster erreichbarer Index
    sccs = []                       # hier sammeln wir die gefundenen SCCs

    def strongconnect(v):
        nonlocal index              # wir greifen auf die Variable 'index' aus der äußeren Funktion zu
        indices[v] = index          # setze Besuchsindex für v
        lowlink[v] = index          # initial ist lowlink = index
        index += 1                  # nächster Knoten bekommt einen höheren Index
        stack.append(v)             # v kommt auf den Stack
        on_stack[v] = True          # markieren, dass v auf dem Stack liegt

        for w in graph[v]:          # durchlaufe alle Nachbarn von v
            if indices[w] == -1:    # wenn Nachbar w noch nicht besucht wurde
                strongconnect(w)    # dann DFS auf w
                lowlink[v] = min(lowlink[v], lowlink[w])  # lowlink von v evtl. nach unten anpassen
            elif on_stack[w]:       # wenn w schon besucht und noch auf dem Stack ist → Rückkante
                lowlink[v] = min(lowlink[v], indices[w])  # auch dann lowlink von v nach unten setzen

        # wenn v Wurzel einer SCC ist (lowlink == index), dann alle bis v vom Stack holen
        if lowlink[v] == indices[v]:
            comp = []               # neue Komponente
            while True:
                w = stack.pop()     # obersten Knoten vom Stack holen
                on_stack[w] = False
                comp.append(w)      # zu dieser SCC hinzufügen
                if w == v:          # bis wir wieder bei v sind
                    break
            sccs.append(comp)       # fertige SCC speichern

    for v in range(n):              # alle Knoten durchgehen
        if indices[v] == -1:        # wenn noch nicht besucht
            strongconnect(v)        # starte Tarjan-DFS von diesem Knoten

    return sccs                     # Liste aller gefundenen SCCs zurückgeben


# ---------- Kosaraju ----------
def kosaraju_scc(graph):
    """Implementierung des Kosaraju-Algorithmus (2 DFS + transponierter Graph)."""
    n = len(graph)                  # Anzahl der Knoten
    visited = [False] * n           # Besuchsarray für die erste DFS
    order = []                      # hier speichern wir die Abschlussreihenfolge (Finishing order)

    def dfs1(v):
        visited[v] = True
        for w in graph[v]:          # normale DFS im Originalgraphen
            if not visited[w]:
                dfs1(w)
        order.append(v)             # wenn alle Kinder fertig sind → v ans Ende hängen

    for v in range(n):              # evtl. mehrere Komponenten → alle Knoten starten
        if not visited[v]:
            dfs1(v)

    # Transponierter Graph: alle Kanten umdrehen
    rev = [[] for _ in range(n)]    # neue Adjazenzliste
    for v in range(n):
        for w in graph[v]:
            rev[w].append(v)        # Kante v->w wird zu w->v

    visited = [False] * n           # für die zweite DFS wieder auf nicht besucht setzen
    sccs = []                       # hier sammeln wir SCCs

    def dfs2(v, comp):
        visited[v] = True
        comp.append(v)
        for w in rev[v]:            # DFS jetzt im transponierten Graphen
            if not visited[w]:
                dfs2(w, comp)

    # zweite Phase: in umgekehrter Abschlussreihenfolge durchgehen
    for v in reversed(order):
        if not visited[v]:
            comp = []
            dfs2(v, comp)
            sccs.append(comp)

    return sccs


# ---------- Messfunktion ----------
def messe(func, graph):
    """misst Laufzeit (ms), Speicherverbrauch (KB) und Anzahl SCCs für eine gegebene Algorithmus-Funktion."""
    tracemalloc.start()                         # Speicherüberwachung starten
    start = time.perf_counter()                 # genaue Startzeit nehmen
    sccs = func(graph)                          # Algorithmus ausführen (Tarjan oder Kosaraju)
    t_s = time.perf_counter() - start           # vergangene Zeit in Sekunden
    _, peak = tracemalloc.get_traced_memory()   # aktuellen und maximalen (peak) Speicher holen
    tracemalloc.stop()                          # Speicherüberwachung beenden
    t_ms = t_s * 1000                           # Sekunden → Millisekunden umrechnen
    return t_ms, peak / 1024, len(sccs)         # Zeit in ms, Speicher in KB, Anzahl SCCs zurückgeben


# ---------- Hauptteil ----------
if __name__ == "__main__":          # sorgt dafür, dass der Code nur läuft, wenn die Datei direkt gestartet wird
    random.seed(42)                 # Zufalls-Seed setzen → dadurch werden die Graphen reproduzierbar

    # drei Größenklassen, wie du in deiner Arbeit beschrieben hast
    kleine_groessen = [10, 15, 20]          # kleine Graphen: sehr wenige Knoten
    mittlere_groessen = [100, 200, 300]     # mittlere Graphen
    grosse_groessen = [5000, 10000, 20000]  # große Graphen → hier wird’s spannend

    # Kopfzeile ausgeben, damit die Daten wie eine Tabelle aussehen
    print("kategorie,nodes,edges,tarjan_time_ms,tarjan_mem_kb,kosaraju_time_ms,kosaraju_mem_kb,tarjan_scc,kosaraju_scc")

    # --- kleine ---
    for n in kleine_groessen:       # gehe alle kleinen Knotenzahlen durch
        m = 4 * n                   # Kanten = 4 * Knoten → leichte, aber nicht zu dünne Graphen
                                    # 4 wurde gewählt, weil kleine Graphen sonst sehr leer wären
        g = make_random_digraph(n, m)               # Graph erzeugen
        t_time, t_mem, t_scc = messe(tarjan_scc, g) # Tarjan messen
        k_time, k_mem, k_scc = messe(kosaraju_scc, g)  # Kosaraju messen
        # alles in einer Zeile ausgeben
        print(f"klein,{n},{m},{t_time:.3f},{t_mem:.2f},{k_time:.3f},{k_mem:.2f},{t_scc},{k_scc}")

    # --- mittlere ---
    for n in mittlere_groessen:
        m = 5 * n                   # hier 5*n → etwas dichter, um Unterschiede besser zu sehen
        g = make_random_digraph(n, m)
        t_time, t_mem, t_scc = messe(tarjan_scc, g)
        k_time, k_mem, k_scc = messe(kosaraju_scc, g)
        print(f"mittel,{n},{m},{t_time:.3f},{t_mem:.2f},{k_time:.3f},{k_mem:.2f},{t_scc},{k_scc}")

    # --- große ---
    for n in grosse_groessen:
        m = 5 * n                   # auch hier 5*n, aber Achtung: das sind viele Kanten → echte Belastung für den Algo
        g = make_random_digraph(n, m)
        t_time, t_mem, t_scc = messe(tarjan_scc, g)
        k_time, k_mem, k_scc = messe(kosaraju_scc, g)
        print(f"gross,{n},{m},{t_time:.3f},{t_mem:.2f},{k_time:.3f},{k_mem:.2f},{t_scc},{k_scc}")
