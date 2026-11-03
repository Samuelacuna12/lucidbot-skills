#!/usr/bin/env python3
"""Consulta local y de solo lectura de la biblioteca pública de Lucid Academy."""
import argparse
import json
import math
import re
import sys
import unicodedata
from pathlib import Path

STOPWORDS = set('a al con de del el en es la las lo los o para por que se su sus un una y'.split())


def normalize(value):
    return ''.join(c for c in unicodedata.normalize('NFKD', str(value).lower())
                   if not unicodedata.combining(c))


def words(value):
    raw = re.findall(r'[a-z0-9_]+', normalize(value))
    return {w[:-1] if len(w) > 4 and w.endswith(('as', 'os')) else w
            for w in raw if w not in STOPWORDS}


def default_path():
    skill = Path(__file__).resolve().parent.parent
    candidates = [skill / 'references' / 'course-knowledge.json',
                  skill.parent.parent / 'knowledge' / 'lucid-bot-normal.json']
    return next((p for p in candidates if p.is_file()), candidates[0])


def load(path):
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, dict) or not isinstance(data.get('lessons'), list):
        raise ValueError('Se esperaba un objeto con lessons[].')
    if data.get('edition') != 'public_general':
        raise ValueError('La biblioteca debe ser la edición public_general.')
    seen = set()
    for lesson in data['lessons']:
        if not isinstance(lesson, dict) or not isinstance(lesson.get('number'), int):
            raise ValueError('Cada clase necesita number entero.')
        if lesson['number'] in seen:
            raise ValueError('Número de clase duplicado.')
        seen.add(lesson['number'])
        knowledge = lesson.get('knowledge')
        if not isinstance(knowledge, dict) or not isinstance(knowledge.get('procedures'), list):
            raise ValueError('Cada clase necesita knowledge.procedures[].')
        for procedure in knowledge['procedures']:
            if not isinstance(procedure, dict) or not procedure.get('topic'):
                raise ValueError('Cada procedimiento necesita topic.')
    return data


def emit(value):
    print(json.dumps(value, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--knowledge', type=Path, help='Ruta a otra copia pública del JSON.')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--session', type=int, choices=range(1, 21), metavar='1..20')
    mode.add_argument('--query', help='Palabras o frase del procedimiento buscado.')
    mode.add_argument('--document', help='ID de un documento íntegro; sin extracción parcial.')
    mode.add_argument('--validate', action='store_true', help='Comprobar estructura e informar cobertura.')
    parser.add_argument('--limit', type=int, choices=range(1, 21), default=6, metavar='1..20')
    args = parser.parse_args()
    path = args.knowledge or default_path()
    try:
        data = load(path)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        parser.error(f'No se pudo leer la biblioteca pública: {exc}. Usa --knowledge con una copia válida.')
    lessons = sorted(data['lessons'], key=lambda lesson: lesson['number'])
    documents = {d['id']: d for d in data.get('documents', []) if isinstance(d, dict) and 'id' in d}
    if args.validate:
        emit({'valid': True, 'edition': data['edition'], 'lessons': len(lessons),
              'procedures': sum(len(x['knowledge']['procedures']) for x in lessons),
              'documents': len(documents),
              'scope': 'Biblioteca de aprendizaje; no ejecuta acciones ni prueba integraciones.'})
        return
    if args.document:
        if args.document not in documents:
            parser.error('Documento desconocido. Ejecuta sin argumentos para ver los IDs disponibles.')
        emit(documents[args.document])
        return
    if args.session:
        lesson = next((x for x in lessons if x['number'] == args.session), None)
        if lesson is None:
            parser.error('La clase no está disponible en esta copia.')
        emit({'lesson': lesson, 'notes': documents.get(lesson.get('notesDocumentId')),
              'caution': 'Ficha completa de formación; no prueba una ejecución en tu cuenta.'})
        return
    if args.query is not None:
        terms = words(args.query)
        if not terms:
            parser.error('La consulta necesita al menos una palabra significativa.')
        phrase = normalize(args.query).strip()
        corpus = []
        for lesson in lessons:
            for index, procedure in enumerate(lesson['knowledge']['procedures']):
                title = normalize(procedure.get('topic', ''))
                body = normalize(json.dumps(procedure, ensure_ascii=False))
                corpus.append((lesson, index, procedure, title, body, words(title), words(body)))
        weights = {term: math.log(1 + len(corpus) / (1 + sum(term in item[6] for item in corpus)))
                   for term in terms}
        scored = []
        for lesson, index, procedure, title, body, title_words, body_words in corpus:
            overlap = terms & body_words
            if not overlap:
                continue
            score = sum(weights[t] * (5 if t in title_words else 1) for t in overlap)
            if overlap == terms:
                score += 12
            if len(terms) > 1 and re.search(r'(?<![a-z0-9_])' + re.escape(phrase) + r'(?![a-z0-9_])', body):
                score += 30
            scored.append((score, {'session': lesson['number'], 'title': lesson.get('title'),
                                   'procedureId': f"lesson-{lesson['number']:02}-procedure-{index + 1:02}",
                                   'procedure': procedure,
                                   'notesDocumentId': lesson.get('notesDocumentId')}))
        scored.sort(key=lambda item: item[0], reverse=True)
        emit({'query': args.query, 'matches': [entry[1] for entry in scored[:args.limit]],
              'caution': 'No sustituye el contrato actual. Respetar límites y scopeApplicability de cada procedimiento.'})
        return
    emit({'title': data.get('title'), 'lessons': [
        {'session': item['number'], 'title': item.get('title'), 'scope': item['knowledge'].get('scope'),
         'procedures': len(item['knowledge']['procedures']), 'notesDocumentId': item.get('notesDocumentId')}
        for item in lessons], 'documents': list(documents),
        'usage': ['--query "tema"', '--session 9', '--document lesson-09-notes', '--validate']})


if __name__ == '__main__':
    main()
