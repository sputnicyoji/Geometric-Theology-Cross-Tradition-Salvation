# -*- coding: utf-8 -*-
"""
GTS Translation Verification Tool
Comprehensive verification of GTS document translations

Usage:
    python gts_verify.py              # Check all documents
    python gts_verify.py GTS-12       # Check specific document
    python gts_verify.py --sections   # Include section-level analysis

Author: Claude Opus 4.5 (G9)
Date: 2025-12-06
"""

import os
import re
import sys
from pathlib import Path

# Base paths
ZH_BASE = Path("E:/Yoji/Project_GTS/GTS/content/zh")
EN_BASE = Path("E:/Yoji/Project_GTS/GTS/content/en")

# Document mapping (Chinese path -> English path)
DOC_MAPPING = {
    # 00-Overview
    "00-Overview/GTS-00-Overview.md": ("00-总览/GTS-00-系统总览.md", "00-Overview/GTS-00-Overview.md"),
    "00-Overview/GTS-Index.md": ("00-总览/GTS-索引.md", "00-Overview/GTS-Index.md"),
    "00-Overview/GTS-Reading-Paths.md": ("00-总览/GTS-阅读路径.md", "00-Overview/GTS-Reading-Paths.md"),

    # 01-Foundations
    "01-Foundations/GTS-01-Channel-Ontology.md": ("01-基础理论/GTS-01-通道本体论.md", "01-Foundations/GTS-01-Channel-Ontology.md"),
    "01-Foundations/GTS-02-Spiral-Cone-Framework.md": ("01-基础理论/GTS-02-螺旋锥框架.md", "01-Foundations/GTS-02-Spiral-Cone-Framework.md"),
    "01-Foundations/GTS-02D-Pain-Dynamics.md": ("01-基础理论/GTS-02D-痛苦动力学.md", "01-Foundations/GTS-02D-Pain-Dynamics.md"),
    "01-Foundations/GTS-03-Prism-Model.md": ("01-基础理论/GTS-03-棱镜模型.md", "01-Foundations/GTS-03-Prism-Model.md"),

    # 02-Quantum-Mapping
    "02-Quantum-Mapping/GTS-04-Wheeler-Participatory-Universe.md": ("02-量子映射/GTS-04-惠勒参与性宇宙.md", "02-Quantum-Mapping/GTS-04-Wheeler-Participatory-Universe.md"),
    "02-Quantum-Mapping/GTS-05-Bohm-Implicate-Order.md": ("02-量子映射/GTS-05-玻姆隐卷序.md", "02-Quantum-Mapping/GTS-05-Bohm-Implicate-Order.md"),
    "02-Quantum-Mapping/GTS-06-Quantum-Decoherence-Emptiness.md": ("02-量子映射/GTS-06-量子退相干与空性.md", "02-Quantum-Mapping/GTS-06-Quantum-Decoherence-Emptiness.md"),
    "02-Quantum-Mapping/GTS-11-Buddhist-Emptiness-Quantum-Vacuum.md": ("02-量子映射/GTS-11-佛教空性与量子真空.md", "02-Quantum-Mapping/GTS-11-Buddhist-Emptiness-Quantum-Vacuum.md"),

    # 03-Cross-Tradition
    "03-Cross-Tradition/GTS-07-Samsara-Salvation-Geometry.md": ("03-跨传统整合/GTS-07-轮回救赎几何.md", "03-Cross-Tradition/GTS-07-Samsara-Salvation-Geometry.md"),
    "03-Cross-Tradition/GTS-08-Nirvana-Heaven-Dao-Quantum-Information-Conservation.md": ("03-跨传统整合/GTS-08-涅槃天国道与量子信息守恒.md", "03-Cross-Tradition/GTS-08-Nirvana-Heaven-Dao-Quantum-Information-Conservation.md"),
    "03-Cross-Tradition/GTS-09-Cross-Universal-Geometry.md": ("03-跨传统整合/GTS-09-跨传统普遍几何.md", "03-Cross-Tradition/GTS-09-Cross-Universal-Geometry.md"),
    "03-Cross-Tradition/GTS-10-Trinity-Quantum-Field-Theory.md": ("03-跨传统整合/GTS-10-三一论与量子场论.md", "03-Cross-Tradition/GTS-10-Trinity-Quantum-Field-Theory.md"),
    "03-Cross-Tradition/GTS-19-Sufi-Spiral-Geometry.md": ("03-跨传统整合/GTS-19-苏菲螺旋几何.md", "03-Cross-Tradition/GTS-19-Sufi-Spiral-Geometry.md"),
    "03-Cross-Tradition/GTS-20-Gnostic-Geometry.md": ("03-跨传统整合/GTS-20-诺斯替几何神学.md", "03-Cross-Tradition/GTS-20-Gnostic-Geometry.md"),

    # 04-Applications
    "04-Applications/GTS-12-Mandala-Topology.md": ("04-应用/GTS-12-曼荼罗拓扑学.md", "04-Applications/GTS-12-Mandala-Topology.md"),
    "04-Applications/GTS-13-Kabbalah-Double-Helix.md": ("04-应用/GTS-13-卡巴拉双螺旋.md", "04-Applications/GTS-13-Kabbalah-Double-Helix.md"),
    "04-Applications/GTS-14-Individuation-Spiral.md": ("04-应用/GTS-14-自性化螺旋.md", "04-Applications/GTS-14-Individuation-Spiral.md"),

    # 05-Meta-Theory
    "05-Meta-Theory/GTS-15-Epistemological-Framework-Raft-and-Shore.md": ("05-元理论/GTS-15-认识论框架-筏与岸.md", "05-Meta-Theory/GTS-15-Epistemological-Framework-Raft-and-Shore.md"),
    "05-Meta-Theory/GTS-16-AI-Assisted-Metaphysics.md": ("05-元理论/GTS-16-AI辅助形而上学.md", "05-Meta-Theory/GTS-16-AI-Assisted-Metaphysics.md"),
    "05-Meta-Theory/GTS-17-The-Age-of-Lost-Axis.md": ("05-元理论/GTS-17-失轴的时代.md", "05-Meta-Theory/GTS-17-The-Age-of-Lost-Axis.md"),
    "05-Meta-Theory/GTS-18-The-Geometry-of-Attention.md": ("05-元理论/GTS-18-注意力几何学.md", "05-Meta-Theory/GTS-18-The-Geometry-of-Attention.md"),
    "05-Meta-Theory/GTS-21-Tao-Flow-Resonance.md": ("05-元理论/GTS-21-道流共振.md", "05-Meta-Theory/GTS-21-Tao-Flow-Resonance.md"),
    "05-Meta-Theory/GTS-META-02-Axis-Handshake.md": ("05-元理论/GTS-META-02-轴心握手.md", "05-Meta-Theory/GTS-META-02-Axis-Handshake.md"),
    "05-Meta-Theory/GTS-Core-Insights.md": ("05-元理论/GTS-核心洞见.md", "05-Meta-Theory/GTS-Core-Insights.md"),
}


def count_lines(filepath):
    """Count lines in a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except:
        return 0


def get_sections(filepath):
    """Extract section headers (## level) with line numbers."""
    sections = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if line.startswith('## '):
                    sections.append((i + 1, line.strip()))
            # Add end marker
            sections.append((len(lines) + 1, "END"))
    except:
        pass
    return sections


def get_status(ratio):
    """Determine translation status based on ratio."""
    if ratio >= 95:
        return "EXCELLENT", ""
    elif ratio >= 85:
        return "GOOD", ""
    elif ratio >= 70:
        return "ACCEPTABLE", " *"
    elif ratio >= 50:
        return "FAIR", " !"
    else:
        return "CRITICAL", " !!!"


def analyze_document(zh_path, en_path, show_sections=False):
    """Analyze a single document pair."""
    zh_lines = count_lines(zh_path)
    en_lines = count_lines(en_path)

    if zh_lines == 0:
        return None

    ratio = en_lines * 100 // zh_lines
    status, flag = get_status(ratio)

    zh_sections = get_sections(zh_path)
    en_sections = get_sections(en_path)

    result = {
        'zh_lines': zh_lines,
        'en_lines': en_lines,
        'ratio': ratio,
        'status': status,
        'flag': flag,
        'zh_section_count': len(zh_sections) - 1,
        'en_section_count': len(en_sections) - 1,
        'sections': []
    }

    if show_sections:
        max_sections = max(len(zh_sections) - 1, len(en_sections) - 1)
        for i in range(max_sections):
            zh_name = zh_sections[i][1] if i < len(zh_sections) - 1 else "-"
            zh_line_count = zh_sections[i+1][0] - zh_sections[i][0] if i < len(zh_sections) - 1 else 0

            en_name = en_sections[i][1] if i < len(en_sections) - 1 else "-"
            en_line_count = en_sections[i+1][0] - en_sections[i][0] if i < len(en_sections) - 1 else 0

            if zh_line_count > 0 and en_line_count > 0:
                sec_ratio = en_line_count * 100 // zh_line_count
                sec_status, sec_flag = get_status(sec_ratio)
            else:
                sec_ratio = 0
                sec_status = "N/A"
                sec_flag = ""

            result['sections'].append({
                'index': i + 1,
                'zh_name': zh_name[:40],
                'en_name': en_name[:40],
                'zh_lines': zh_line_count,
                'en_lines': en_line_count,
                'ratio': sec_ratio,
                'status': sec_status,
                'flag': sec_flag
            })

    return result


def main():
    # Parse arguments
    target_doc = None
    show_sections = False

    for arg in sys.argv[1:]:
        if arg == '--sections':
            show_sections = True
        elif arg.startswith('GTS-'):
            target_doc = arg

    print("=" * 80)
    print("GTS TRANSLATION VERIFICATION TOOL")
    print("=" * 80)

    results = []

    for en_rel_path, (zh_rel, en_rel) in DOC_MAPPING.items():
        zh_path = ZH_BASE / zh_rel
        en_path = EN_BASE / en_rel

        # Extract document name
        doc_name = en_rel_path.split('/')[-1].replace('.md', '')

        # Filter if specific document requested
        if target_doc and target_doc not in doc_name:
            continue

        result = analyze_document(zh_path, en_path, show_sections)
        if result:
            result['name'] = doc_name
            results.append(result)

    # Sort by ratio
    results.sort(key=lambda x: x['ratio'])

    # Print summary table
    print("\n" + "-" * 80)
    print("DOCUMENT SUMMARY (sorted by ratio)")
    print("-" * 80)
    print(f"{'Document':<45} {'ZH':>6} {'EN':>6} {'Ratio':>7} {'Sec':>5} {'Status':<12}")
    print("-" * 80)

    total_zh = 0
    total_en = 0

    for r in results:
        total_zh += r['zh_lines']
        total_en += r['en_lines']

        sec_match = "OK" if r['zh_section_count'] == r['en_section_count'] else f"{r['zh_section_count']}/{r['en_section_count']}"

        print(f"{r['name']:<45} {r['zh_lines']:>6} {r['en_lines']:>6} {r['ratio']:>6}% {sec_match:>5} {r['status']:<12}{r['flag']}")

        # Show sections if requested
        if show_sections and r['sections']:
            print(f"  {'#':<3} {'ZH Section':<40} {'Lines':>6} | {'EN Section':<40} {'Lines':>6}")
            for sec in r['sections']:
                print(f"  {sec['index']:<3} {sec['zh_name']:<40} {sec['zh_lines']:>6} | {sec['en_name']:<40} {sec['en_lines']:>6}{sec['flag']}")
            print()

    print("-" * 80)
    if total_zh > 0:
        print(f"{'TOTAL':<45} {total_zh:>6} {total_en:>6} {total_en*100//total_zh:>6}%")

    # Statistics
    excellent = len([r for r in results if r['status'] == 'EXCELLENT'])
    good = len([r for r in results if r['status'] == 'GOOD'])
    acceptable = len([r for r in results if r['status'] == 'ACCEPTABLE'])
    fair = len([r for r in results if r['status'] == 'FAIR'])
    critical = len([r for r in results if r['status'] == 'CRITICAL'])

    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    print(f"  EXCELLENT (95%+):    {excellent} documents")
    print(f"  GOOD (85-94%):       {good} documents")
    print(f"  ACCEPTABLE (70-84%): {acceptable} documents")
    print(f"  FAIR (50-69%):       {fair} documents")
    print(f"  CRITICAL (<50%):     {critical} documents")
    print(f"\n  Total documents: {len(results)}")
    if total_zh > 0:
        print(f"  Overall ratio: {total_en*100//total_zh}%")

    # Warnings
    if critical > 0:
        print("\n" + "!" * 80)
        print("CRITICAL ISSUES FOUND:")
        for r in results:
            if r['status'] == 'CRITICAL':
                print(f"  - {r['name']}: {r['ratio']}%")
        print("!" * 80)

    if fair > 0:
        print("\nWARNINGS:")
        for r in results:
            if r['status'] == 'FAIR':
                print(f"  - {r['name']}: {r['ratio']}%")

    print("\n" + "=" * 80)
    print("VERIFICATION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
