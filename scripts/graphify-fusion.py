"""Fusion des concepts identiques entre documents (graphe FluxyRH-docs).

Un meme concept cite dans plusieurs documents devient un noeud par document.
Ce script relie ces copies par une arete `same_as` (cle exacte : code de phase,
exigence, ecran, classe, table, decision), puis recalcule communautes, rapport
et graph.json. A relancer apres chaque `/graphify ... --update`.

Usage (depuis la racine FluxyRH) : python FluxyRH-docs/scripts/graphify-fusion.py
"""
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / 'graphify-out'
ROOT = (OUT / '.graphify_root').read_text(encoding='utf-8').strip()

PHASE = re.compile(r'^(W\d{2}(?:\.\d+){0,2}|E\d{2}(?:\.\d+)?|B\d{2}(?:\.\d+)?|C\d{2}(?:\.\d+)?|MEP(?:\.\d+)?)(?=[\s:—\-(]|$)')
REQ = re.compile(r'^(F-[A-Z]{3}-\d{2}|NF-\d{2}|T-\d{2})\b')
PRINCIPLE = re.compile(r'^(P\d{1,2}|U\d{1,2})\s')
SCREEN = re.compile(r'^(?:ecran\s+)?S-(\d{2,3})\b', re.I)
DECISION = re.compile(r'^decision\s+(\d{4})\b', re.I)
CLASS = re.compile(r'^([A-Z][a-z0-9]+(?:[A-Z][A-Za-z0-9]*)+)(?:::|\b)')
TABLE_PREFIX = re.compile(r'^tables?\s+([a-z][a-z0-9_]+)', re.I)
SNAKE = re.compile(r'^([a-z][a-z0-9]*(?:_[a-z0-9]+)+)\b')
PLURAL = re.compile(r'^([a-z]{4,}s)\b')
PREFIXES = ('middleware ', 'cast eloquent ', 'cast ', 'composant mobile ', 'composant ', 'enum ', 'route ')


def ascii_fold(s):
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()


def key_of(node):
    if node.get('_origin') == 'ast':
        return None
    label = ascii_fold(node.get('label', '')).strip()
    low = label.lower()
    for p in PREFIXES:
        if low.startswith(p):
            label = label[len(p):]
            low = label.lower()
            break
    if m := PHASE.match(label):
        return 'phase:' + m.group(1)
    if m := REQ.match(label):
        return 'req:' + m.group(1)
    if m := PRINCIPLE.match(label):
        return 'principle:' + m.group(1)
    if m := SCREEN.match(label):
        return 'screen:S-' + m.group(1)
    if m := DECISION.match(label):
        return 'decision:' + m.group(1)
    if m := CLASS.match(label):
        return 'class:' + m.group(1)
    if m := TABLE_PREFIX.match(label):
        return 'table:' + m.group(1).lower()
    if m := SNAKE.match(label):
        return 'table:' + m.group(1)
    if m := PLURAL.match(label):
        return 'table:' + m.group(1)
    return None


def main():
    from graphify.build import build_from_json
    from graphify.cluster import cluster, score_all
    from graphify.analyze import god_nodes, surprising_connections, suggest_questions
    from graphify.report import generate
    from graphify.export import to_json
    from graphify.detect import detect

    g = json.loads((OUT / 'graph.json').read_text(encoding='utf-8'))
    nodes = [{k: v for k, v in n.items() if k not in ('community', 'community_name', 'norm_label')} for n in g['nodes']]
    edges = [e for e in g['links'] if e.get('relation') != 'same_as']
    hyper = g.get('hyperedges') or g.get('graph', {}).get('hyperedges', [])

    degree = defaultdict(int)
    pairs = set()
    for e in edges:
        degree[e['source']] += 1
        degree[e['target']] += 1
        pairs.add(frozenset((e['source'], e['target'])))

    groups = defaultdict(list)
    for n in nodes:
        if k := key_of(n):
            groups[k].append(n)

    added = 0
    multi = {k: v for k, v in groups.items() if len({n['source_file'] for n in v}) > 1}
    for k, members in multi.items():
        canon = max(members, key=lambda n: degree[n['id']])
        for n in members:
            if n['id'] == canon['id'] or frozenset((n['id'], canon['id'])) in pairs:
                continue
            edges.append({'source': n['id'], 'target': canon['id'], 'relation': 'same_as',
                          'confidence': 'INFERRED', 'confidence_score': 0.95,
                          'source_file': n['source_file'], 'source_location': None,
                          'weight': 1.0, '_origin': 'semantic', 'context': k})
            added += 1
    print(f'{len(multi)} concepts presents dans plusieurs documents, {added} aretes same_as ajoutees')

    extraction = {'nodes': nodes, 'edges': edges, 'hyperedges': hyper, 'input_tokens': 0, 'output_tokens': 0}
    G = build_from_json(extraction, root=ROOT, directed=False)
    communities = cluster(G)
    cohesion = score_all(G, communities)

    labels_file = sys.argv[sys.argv.index('--labels') + 1] if '--labels' in sys.argv else None
    lab = {n['id']: n['label'] for n in nodes}
    if labels_file:
        given = {int(k): v for k, v in json.loads(Path(labels_file).read_text(encoding='utf-8')).items()}
    else:
        given = {}
    labels = {cid: given.get(cid) or ('Groupe : ' + lab.get(sorted(m, key=lambda i: -G.degree(i))[0], '')[:40])
              for cid, m in communities.items()}

    detection = detect(Path(ROOT))
    gods = god_nodes(G)
    surprises = surprising_connections(G, communities)
    questions = suggest_questions(G, communities, labels)
    cost = json.loads((OUT / 'cost.json').read_text(encoding='utf-8'))
    tokens = {'input': cost['total_input_tokens'], 'output': cost['total_output_tokens']}
    if not to_json(G, communities, str(OUT / 'graph.json'), community_labels=labels):
        raise SystemExit('graph.json non ecrit (garde anti-retrecissement)')
    report = generate(G, communities, cohesion, labels, gods, surprises, detection, tokens, ROOT, suggested_questions=questions)
    (OUT / 'GRAPH_REPORT.md').write_text(report, encoding='utf-8')
    (OUT / '.graphify_labels.json').write_text(json.dumps({str(k): v for k, v in labels.items()}, ensure_ascii=False), encoding='utf-8')
    print(f'Graphe : {G.number_of_nodes()} noeuds, {G.number_of_edges()} aretes, {len(communities)} communautes')
    for cid, m in sorted(communities.items(), key=lambda kv: -len(kv[1])):
        if len(m) >= 8:
            top = sorted(m, key=lambda i: -G.degree(i))[:5]
            print(cid, len(m), ' | '.join(lab.get(i, i)[:35] for i in top))


if __name__ == '__main__':
    main()
