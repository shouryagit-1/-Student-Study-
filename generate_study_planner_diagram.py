import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_study_planner_architecture(out_path="study_planner_architecture.png"):
    fig, ax = plt.subplots(figsize=(10, 4.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.2)
    ax.axis("off")
    fig.patch.set_facecolor("white")
    
    w = 2.1
    h = 1.15
    y1 = 2.6
    
    boxes_r1 = [
        (0.2, y1, "Student Input\n(Subjects, Topics,\nExam Dates)"),
        (2.7, y1, "Input Validation\n& SQLite Storage"),
        (5.2, y1, "Urgency & Workload\nCalculation Engine"),
        (7.7, y1, "Smart Timetable\nAllocator Algorithm")
    ]
    
    y2 = 0.6
    boxes_r2 = [
        (7.7, y2, "Daily Session\nGeneration & Pacing"),
        (5.2, y2, "Pomodoro &\nBreak Manager"),
        (2.7, y2, "Interactive Topic\nTracker (AJAX / DB)"),
        (0.2, y2, "Web Dashboard &\nVisual Progress (UI)")
    ]
    
    for x, y, text in boxes_r1:
        bbox = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.12",
                                      facecolor="#f4f8fc", edgecolor="#0b3c6d", linewidth=1.4)
        ax.add_patch(bbox)
        ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=8.5, fontweight="bold", color="#111827", multialignment="center")

    arrow_props = dict(arrowstyle="-|>", color="#0b3c6d", lw=1.6, mutation_scale=14)
    ax.annotate("", xy=(2.7, y1 + h/2), xytext=(2.3, y1 + h/2), arrowprops=arrow_props)
    ax.annotate("", xy=(5.2, y1 + h/2), xytext=(4.8, y1 + h/2), arrowprops=arrow_props)
    ax.annotate("", xy=(7.7, y1 + h/2), xytext=(7.3, y1 + h/2), arrowprops=arrow_props)
    
    # Down arrow from box 4 to box 5
    ax.annotate("", xy=(8.75, y2 + h), xytext=(8.75, y1), arrowprops=arrow_props)
    
    for x, y, text in boxes_r2:
        bbox = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.12",
                                      facecolor="#f4f8fc", edgecolor="#0b3c6d", linewidth=1.4)
        ax.add_patch(bbox)
        ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=8.5, fontweight="bold", color="#111827", multialignment="center")

    # Arrows for Row 2 (leftward)
    ax.annotate("", xy=(7.3, y2 + h/2), xytext=(7.7, y2 + h/2), arrowprops=arrow_props)
    ax.annotate("", xy=(4.8, y2 + h/2), xytext=(5.2, y2 + h/2), arrowprops=arrow_props)
    ax.annotate("", xy=(2.3, y2 + h/2), xytext=(2.7, y2 + h/2), arrowprops=arrow_props)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Created {out_path}")

if __name__ == "__main__":
    create_study_planner_architecture()
