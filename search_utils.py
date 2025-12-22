import os
import re
import requests
from typing import List, Tuple

def search_repo(query: str, root: str = ".", max_results: int = 20) -> List[Tuple[str, int, str]]:
    """Search repository files for lines containing the query (case-insensitive).
    Returns list of tuples: (relative_path, line_number, line_text).
    """
    results = []
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    for dirpath, _, filenames in os.walk(root):
        # skip virtualenv and .git directories
        if any(part in (".git", "venv", "node_modules") for part in dirpath.split(os.sep)):
            continue
        for fn in filenames:
            if fn.endswith(('.py', '.md', '.txt', '.rst')):
                path = os.path.join(dirpath, fn)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        for i, line in enumerate(f, start=1):
                            if pattern.search(line):
                                rel = os.path.relpath(path, start=root)
                                results.append((rel, i, line.strip()))
                                if len(results) >= max_results:
                                    return results
                except Exception:
                    continue
    return results

def wiki_search_summary(query: str) -> Tuple[str, str]:
    """Return (title, summary) from Wikipedia for the query. If none found, return ("", "")."""
    search_url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': query,
        'format': 'json',
        'srlimit': 1,
    }
    try:
        r = requests.get(search_url, params=params, timeout=6)
        r.raise_for_status()
        data = r.json()
        hits = data.get('query', {}).get('search', [])
        if not hits:
            return "", ""
        title = hits[0]['title']
        # fetch summary
        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.requote_uri(title)}"
        s = requests.get(summary_url, timeout=6)
        s.raise_for_status()
        summ = s.json().get('extract', '')
        return title, summ
    except Exception:
        return "", ""
