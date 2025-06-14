import os
import anthropic
from typing import List, Dict

client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

def classifica_bandi_claude(bandi: List[Dict], azienda: Dict) -> str:
    prompt = f"""
Sei un analista di finanza agevolata. Valuta l’idoneità dei bandi forniti rispetto al profilo aziendale seguendo questi criteri di scoring:

🧾 Dati azienda:
Regione: {azienda['regione']}
Codice ATECO: {azienda['codice_ateco']}
Dimensione: {azienda['dimensione']}
Macro-area assegnata: {azienda['macro_area']}
EBITDA Margin: {azienda['indici'].get('EBITDA_margin', 'N/A')}
Utile netto: {azienda['indici'].get('utile_netto', 'N/A')}
Debt/Equity: {azienda['indici'].get('Debt_Equity', 'N/A')}

📄 Bandi disponibili (max 15):
{bandi}

🎯 Criteri di valutazione (peso %):
B. Solidità Finanziaria – 35%
C. Forma dell’agevolazione – 20%
D. Dimensione Aziendale – 15%
E. Capacità di co-finanziamento – 15%
F. Coerenza territoriale e settore ATECO – 15%

🧮 Assegna a ogni bando:
- Un punteggio da 0 a 100
- Una classificazione qualitativa:
  • 80–100 → Alta probabilità ✅
  • 50–79 → Media probabilità ⚠️
  • 0–49 → Bassa probabilità ❌
- Una breve motivazione (massimo 2 righe)

📌 IMPORTANTE:
- Scarta tutti i bandi con punteggio inferiore a 80
- Restituisci solo i **top 3 bandi** con punteggio ≥80
- Rispondi in formato elenco numerato.
"""

    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0.3,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.content[0].text if response.content else "Errore nella risposta di Claude."
