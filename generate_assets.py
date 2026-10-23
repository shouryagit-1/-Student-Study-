import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont

def create_psit_logo(out_path="psit_logo.png"):
    fig, ax = plt.subplots(figsize=(3.2, 1.2), dpi=300)
    ax.axis("off")
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    
    # PSIT main text
    ax.text(0.5, 0.65, "PSIT", color="#002b66", fontsize=38, fontweight="black",
            ha="center", va="center", family="sans-serif", transform=ax.transAxes)
    
    # Underline
    ax.plot([0.18, 0.82], [0.40, 0.40], color="#002b66", lw=2, transform=ax.transAxes)
    
    # Kanpur text
    ax.text(0.5, 0.22, "Kanpur", color="#002b66", fontsize=18, style="italic",
            fontweight="normal", ha="center", va="center", family="serif", transform=ax.transAxes)
    
    plt.tight_layout(pad=0)
    plt.savefig(out_path, dpi=300, bbox_inches="tight", transparent=False, facecolor="white")
    plt.close()
    print(f"Created {out_path}")

def create_architecture_diagram(out_path="architecture_diagram.png"):
    fig, ax = plt.subplots(figsize=(10, 4.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.2)
    ax.axis("off")
    fig.patch.set_facecolor("white")
    
    # Box definitions: (x, y, w, h, text)
    # Row 1 (y = 2.4, h = 1.2)
    # 4 boxes
    # x: 0.2, 2.7, 5.2, 7.7
    w = 2.1
    h = 1.15
    y1 = 2.6
    
    boxes_r1 = [
        (0.2, y1, "User Input\n(URL / Email /\nSMS text)"),
        (2.7, y1, "Preprocessing\n& Validation"),
        (5.2, y1, "Feature Extraction\n(URL, Domain,\nContent features)"),
        (7.7, y1, "AI/ML Classifier\n(Random Forest /\nXGBoost / NLP)")
    ]
    
    y2 = 0.6
    boxes_r2 = [
        (7.7, y2, "Risk Scoring\n(Safe / Suspicious /\nPhishing / Scam)"),
        (5.2, y2, "Alert & Report\nGeneration"),
        (2.7, y2, "Web App / Browser\nExtension (UI)"),
        (0.2, y2, "Logs &\nDatabase")
    ]
    
    box_props = dict(boxstyle="round,pad=0.5,rounding_size=0.15", facecolor="#f4f8ff", edgecolor="#1a56a0", linewidth=1.5)
    
    for x, y, text in boxes_r1:
        bbox = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.12",
                                      facecolor="#f4f8fc", edgecolor="#0b3c6d", linewidth=1.4)
        ax.add_patch(bbox)
        ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=8.5, fontweight="bold", color="#111827", multialignment="center")

    # Arrows for Row 1
    # 0.2+2.1=2.3 -> 2.7
    arrow_props = dict(arrowstyle="-|>", color="#0b3c6d", lw=1.6, mutation_scale=14)
    ax.annotate("", xy=(2.7, y1 + h/2), xytext=(2.3, y1 + h/2), arrowprops=arrow_props)
    ax.annotate("", xy=(5.2, y1 + h/2), xytext=(4.8, y1 + h/2), arrowprops=arrow_props)
    ax.annotate("", xy=(7.7, y1 + h/2), xytext=(7.3, y1 + h/2), arrowprops=arrow_props)
    
    # Arrow down from box 4 to box 5
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
    create_psit_logo()
    create_architecture_diagram()
