import json
import re

def analyze_and_cluster():
    with open(r'D:\projects\HK\crawler\betalist_startups.json', 'r', encoding='utf-8') as f:
        startups = json.load(f)
        
    # Categories definition with keyword heuristics
    categories = {
        "AI Agents & Automation Infrastructure": {
            "keywords": ["agent", "agents", "mcp", "automate", "automation", "kalshi", "coding agent", "receptionist", "deskbot", "tally", "muster", "sickle", "call4me"],
            "seed_multiple": 10, # Typical SaaS ARR multiple
            "base_valuation_k": 3500, # $3.5M Seed baseline
            "projected_5y_growth": "18x - 30x",
            "market_driver": "Rapid migration from static prompt wrappers to autonomous OS/MCP execution runtimes."
        },
        "AI Developer Tools & Code Reviews": {
            "keywords": ["code", "developer", "api", "review", "pull request", "heydeer", "transcription", "convert.express", "convert pdf"],
            "seed_multiple": 8,
            "base_valuation_k": 2800,
            "projected_5y_growth": "12x - 20x",
            "market_driver": "Developer productivity enhancement and automated CI/CD code gatekeeping."
        },
        "Autonomous SEO & Growth Engines": {
            "keywords": ["seo", "openseo", "tadaseo", "rankinai", "citations", "google rankings", "visibility", "marketing"],
            "seed_multiple": 6,
            "base_valuation_k": 2200,
            "projected_5y_growth": "8x - 15x",
            "market_driver": "Disruption of traditional SEMrush/Ahrefs monopolies via open-source and generative search indexing."
        },
        "Media Generation & Creative AI": {
            "keywords": ["3d", "video", "icons", "cinematic", "seedance", "quady3d", "kiriframe", "ai shorts", "cullit", "roomstaging", "photos"],
            "seed_multiple": 7,
            "base_valuation_k": 2500,
            "projected_5y_growth": "10x - 22x",
            "market_driver": "High-throughput 3D mesh and synthetic cinematic short-form video generation."
        },
        "B2B Vertical Workspaces & Management": {
            "keywords": ["hoa", "store", "headoffis", "basicops", "rentalthread", "care", "membership", "retello", "storage", "charging", "ev"],
            "seed_multiple": 5,
            "base_valuation_k": 2000,
            "projected_5y_growth": "6x - 12x",
            "market_driver": "Digitization of neglected offline brick-and-mortar operations (HOA, EV chargers, rentals)."
        },
        "Fintech, Budgeting & Split Billing": {
            "keywords": ["calendar", "budget", "cash flow", "split", "subsplit", "dividends", "nimblewit", "stocks", "cyrontek"],
            "seed_multiple": 8,
            "base_valuation_k": 3000,
            "projected_5y_growth": "9x - 18x",
            "market_driver": "Micro-fintech tackling irregular freelance gig-income and automated multi-tenant bill splitting."
        }
    }
    
    clustered = {cat: [] for cat in categories}
    unclassified = []
    
    for s in startups:
        text = (s['name'] + " " + s['slug'] + " " + s['pitch']).lower()
        matched = False
        for cat, meta in categories.items():
            if any(k in text for k in meta['keywords']):
                clustered[cat].append(s)
                matched = True
                break
        if not matched:
            unclassified.append(s)
            
    # Compile valuation report
    report = []
    for cat, items in clustered.items():
        meta = categories[cat]
        count = len(items)
        if count == 0: continue
        
        # Current Estimated Aggregate Pre-Seed / Seed Valuation (assuming early beta/traction $1.5M - $4M each)
        est_current_total_m = round((count * meta['base_valuation_k']) / 1000, 2)
        # 5-Year Projected Category Market Cap / Exit Value (with power law: 1-2 winners)
        min_mult = int(meta['projected_5y_growth'].split('x')[0].strip())
        max_mult = int(meta['projected_5y_growth'].split('-')[1].replace('x','').strip())
        proj_low_m = round(est_current_total_m * (min_mult * 0.35), 1) # Accounting for 65% failure rate
        proj_high_m = round(est_current_total_m * (max_mult * 0.50), 1)
        
        report.append({
            "category": cat,
            "startup_count": count,
            "startups": [f"{it['name']} ({it['betalist_url']})" for it in items],
            "current_est_aggregate_networth_usd": f"${est_current_total_m}M",
            "avg_seed_valuation_per_startup": f"${meta['base_valuation_k']/1000}M",
            "five_year_projected_category_cap": f"${proj_low_m}M - ${proj_high_m}M",
            "power_law_growth_multiple": meta['projected_5y_growth'],
            "market_driver": meta['market_driver']
        })
        
    out_file = r'D:\projects\HK\crawler\betalist_category_valuation_matrix.json'
    with open(out_file, 'w', encoding='utf-8') as fp:
        json.dump(report, fp, indent=2, ensure_ascii=False)
        
    print(f"[+] Successfully clustered {len(startups)} startups into {len(report)} categories!")
    print(f"[+] Output written to {out_file}\n")
    
    # Print clean terminal report
    for r in report:
        print("=" * 85)
        print(f"CATEGORY: {r['category']} ({r['startup_count']} Startups)")
        print(f"Current Aggregate Seed Value: {r['current_est_aggregate_networth_usd']} | 5-Year Projected Category Cap: {r['five_year_projected_category_cap']}")
        print(f"Growth Multiple: {r['power_law_growth_multiple']} | Driver: {r['market_driver']}")
        print("Startups in this cluster:")
        for s in r['startups'][:6]:
            print(f"  • {s}")
        if len(r['startups']) > 6:
            print(f"  ...and {len(r['startups']) - 6} more.")

if __name__ == '__main__':
    analyze_and_cluster()
