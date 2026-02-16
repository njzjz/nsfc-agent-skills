#!/usr/bin/env python3
"""Generate a research roadmap figure for NSFC proposals.

Usage:
    python generate_roadmap.py --title "技术路线图" \
        --nodes "数据采集,模型训练,性能评估,应用验证" \
        --output roadmap.png --dpi 300

    python generate_roadmap.py --config roadmap.json --output roadmap.png
"""

import argparse
import json
import sys

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.patches import FancyBboxPatch
except ImportError:
    print("Error: matplotlib is required. Install with: pip install matplotlib")
    sys.exit(1)


# Try to set Chinese font
def setup_chinese_font():
    """Try to configure matplotlib for Chinese text."""
    import matplotlib.font_manager as fm
    
    # Common Chinese fonts on different platforms
    chinese_fonts = [
        'SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei',
        'Noto Sans CJK SC', 'Source Han Sans SC', 'PingFang SC',
        'STHeiti', 'AR PL UMing CN'
    ]
    
    available = [f.name for f in fm.fontManager.ttflist]
    for font in chinese_fonts:
        if font in available:
            plt.rcParams['font.sans-serif'] = [font] + plt.rcParams['font.sans-serif']
            plt.rcParams['axes.unicode_minus'] = False
            return font
    
    print("Warning: No Chinese font found. Chinese text may not display correctly.")
    return None


def draw_flowchart(nodes, title="技术路线图", output="roadmap.png", dpi=300,
                   colors=None, figsize=(12, 6)):
    """Draw a simple left-to-right flowchart.
    
    Args:
        nodes: List of node labels
        title: Figure title
        output: Output file path
        dpi: Resolution
        colors: List of colors for nodes (optional)
        figsize: Figure size in inches
    """
    setup_chinese_font()
    
    if colors is None:
        # Academic blue color scheme
        base_colors = ['#4472C4', '#5B9BD5', '#70AD47', '#FFC000', '#ED7D31', '#A5A5A5']
        colors = [base_colors[i % len(base_colors)] for i in range(len(nodes))]
    
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    ax.set_xlim(-0.5, len(nodes) - 0.5)
    ax.set_ylim(-1, 1)
    ax.axis('off')
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    
    box_width = 0.6
    box_height = 0.5
    
    for i, (node, color) in enumerate(zip(nodes, colors)):
        # Draw box
        bbox = FancyBboxPatch(
            (i - box_width/2, -box_height/2),
            box_width, box_height,
            boxstyle="round,pad=0.05",
            facecolor=color, edgecolor='white',
            linewidth=2, alpha=0.9
        )
        ax.add_patch(bbox)
        
        # Add text
        ax.text(i, 0, node, ha='center', va='center',
                fontsize=10, color='white', fontweight='bold',
                wrap=True)
        
        # Draw arrow to next node
        if i < len(nodes) - 1:
            ax.annotate('', xy=(i + 1 - box_width/2 - 0.05, 0),
                       xytext=(i + box_width/2 + 0.05, 0),
                       arrowprops=dict(arrowstyle='->', color='#333333',
                                      lw=2, connectionstyle='arc3,rad=0'))
    
    plt.tight_layout()
    plt.savefig(output, dpi=dpi, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"Saved to {output} ({dpi} DPI)")
    plt.close()


def draw_hierarchical(config, output="roadmap.png", dpi=300):
    """Draw a hierarchical research roadmap from a config dict.
    
    Config format:
    {
        "title": "技术路线图",
        "levels": [
            {"label": "科学问题", "items": ["问题1", "问题2"]},
            {"label": "研究内容", "items": ["内容1", "内容2", "内容3"]},
            {"label": "预期成果", "items": ["成果1", "成果2"]}
        ]
    }
    """
    setup_chinese_font()
    
    levels = config.get('levels', [])
    title = config.get('title', '技术路线图')
    
    n_levels = len(levels)
    max_items = max(len(l['items']) for l in levels)
    
    fig, ax = plt.subplots(figsize=(max_items * 3, n_levels * 2.5))
    ax.set_xlim(-0.5, max_items - 0.5)
    ax.set_ylim(-0.5, n_levels - 0.5)
    ax.axis('off')
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.invert_yaxis()
    
    level_colors = ['#4472C4', '#70AD47', '#FFC000', '#ED7D31', '#5B9BD5']
    
    for li, level in enumerate(levels):
        items = level['items']
        n = len(items)
        # Center items
        start_x = (max_items - n) / 2
        
        for ii, item in enumerate(items):
            x = start_x + ii
            y = li
            color = level_colors[li % len(level_colors)]
            
            bbox = FancyBboxPatch(
                (x - 0.4, y - 0.25), 0.8, 0.5,
                boxstyle="round,pad=0.05",
                facecolor=color, edgecolor='white',
                linewidth=2, alpha=0.85
            )
            ax.add_patch(bbox)
            ax.text(x, y, item, ha='center', va='center',
                    fontsize=9, color='white', fontweight='bold')
            
            # Draw arrows to next level
            if li < n_levels - 1:
                next_items = levels[li + 1]['items']
                next_n = len(next_items)
                next_start = (max_items - next_n) / 2
                for ni in range(next_n):
                    nx = next_start + ni
                    ny = li + 1
                    ax.annotate('', xy=(nx, ny - 0.25),
                               xytext=(x, y + 0.25),
                               arrowprops=dict(arrowstyle='->', color='#999999',
                                              lw=0.8, alpha=0.5))
        
        # Level label
        ax.text(-0.4, li, level.get('label', ''), ha='right', va='center',
                fontsize=11, fontweight='bold', color='#333333')
    
    plt.tight_layout()
    plt.savefig(output, dpi=dpi, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"Saved to {output} ({dpi} DPI)")
    plt.close()


def main():
    parser = argparse.ArgumentParser(description='Generate research roadmap figures')
    parser.add_argument('--title', default='技术路线图', help='Figure title')
    parser.add_argument('--nodes', help='Comma-separated node labels (for flowchart)')
    parser.add_argument('--config', help='JSON config file (for hierarchical)')
    parser.add_argument('--output', default='roadmap.png', help='Output file path')
    parser.add_argument('--dpi', type=int, default=300, help='Resolution (DPI)')
    parser.add_argument('--figsize', default='12,6', help='Figure size (width,height)')
    
    args = parser.parse_args()
    figsize = tuple(float(x) for x in args.figsize.split(','))
    
    if args.config:
        with open(args.config) as f:
            config = json.load(f)
        draw_hierarchical(config, args.output, args.dpi)
    elif args.nodes:
        nodes = [n.strip() for n in args.nodes.split(',')]
        draw_flowchart(nodes, args.title, args.output, args.dpi, figsize=figsize)
    else:
        # Demo
        print("No input specified. Generating demo...")
        nodes = ['科学问题', '数据采集', '模型构建', '性能评估', '应用验证']
        draw_flowchart(nodes, args.title, args.output, args.dpi, figsize=figsize)


if __name__ == '__main__':
    main()
