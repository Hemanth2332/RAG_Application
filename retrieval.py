def make_prompt(query, passage):
    return f"""
QUESTION: {query}
PASSAGE: {passage}
ANSWER (friendly, simple, <250 words):
"""

def get_relevant_contents(query: str, db, k=3):
    results = db.query(query_texts=[query], n_results=k, include=["documents"])
    return results["documents"][0]
