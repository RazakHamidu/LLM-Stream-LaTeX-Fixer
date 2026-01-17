# 🌊 LLM Stream & LaTeX Fixer

Un "Proof of Concept" (PoC) che dimostra come gestire flussi di risposta LLM (Google Gemini) in tempo reale, risolvendo i comuni problemi di rendering di Markdown e LaTeX incompleti.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?style=flat&logo=flask)
![Gemini API](https://img.shields.io/badge/Google%20Gemini-API-orange?style=flat&logo=google)
![JavaScript](https://img.shields.io/badge/JavaScript-Vanilla-yellow?style=flat&logo=javascript)

---

## 🛑 Il Problema

Quando si costruiscono interfacce chat moderne con gli LLM, lo **streaming** è essenziale per ridurre la latenza percepita (Time to First Token). Tuttavia, inviare frammenti di testo grezzo al frontend causa rotture visive nei parser:

1.  **LaTeX Incompleto:** Se lo stream si ferma momentaneamente su `$$ \frac{1}{2`, il motore di rendering (es. KaTeX) non trova la chiusura `$$` e spesso mostra il codice sorgente o lancia un errore.
2.  **Markdown Rotto:** Tabelle e blocchi di codice non vengono renderizzati finché non sono sintatticamente chiusi.
3.  **Gestione Errori Backend:** Le API di Gemini lanciano un `ValueError` se si tenta di accedere al testo di un chunk bloccato dai filtri di sicurezza, rischiando di interrompere lo stream lato server.

---

## ✅ La Soluzione

Questo progetto implementa una pipeline robusta per mitigare questi problemi sia lato server che lato client.

### 1. Frontend: Heuristic Repair (Riparazione Euristica)
Prima di passare il buffer di testo alle librerie di rendering (`Marked` e `KaTeX`), una funzione JavaScript analizza la stringa. Se rileva sintassi LaTeX aperte (es. numero dispari di `$$`), aggiunge temporaneamente una chiusura fittizia.

```javascript
// Esempio logico del fix applicato in tempo reale
function fixIncompleteLatex(text) {
    const doubleDollars = (text.match(/\$\$/g) || []).length;
    // Se i delimitatori sono dispari, chiudiamo forzatamente il blocco
    if (doubleDollars % 2 !== 0) {
        return text + " $$"; 
    }
    return text;
}

```

### 2. Backend: Streaming Sicuro

Il server Flask utilizza un generatore (`yield`) per inoltrare i chunk immediatamente. Include un blocco `try-except` specifico per gestire i `Safety Settings` di Google, garantendo che lo stream continui anche se parzialmente censurato, senza crashare il server.

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask, `google-generativeai`.
* **Frontend:** HTML5, CSS3, Vanilla JS.
* **Librerie Frontend:**
* `Marked.js`: Parsing Markdown -> HTML.
* `KaTeX`: Rendering veloce di formule matematiche.



---

## 🚀 Installazione e Avvio

Segui questi passaggi per avviare il progetto in locale.

### 1. Prerequisiti

* Python installato (3.8 o superiore).
* Una API Key di Google Gemini ([Ottienila qui](https://aistudio.google.com/app/apikey)).

### 2. Clona il repository

```bash
git clone [https://github.com/tuo-username/gemini-stream-fix.git](https://github.com/tuo-username/gemini-stream-fix.git)
cd gemini-stream-fix

```

### 3. Configura l'ambiente virtuale (Opzionale ma consigliato)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

```

### 4. Installa le dipendenze

```bash
pip install -r requirements.txt

```

### 5. Configurazione Variabili d'Ambiente

Crea un file `.env` nella root del progetto e inserisci la tua chiave:

```env
GOOGLE_API_KEY=la_tua_chiave_api_qui_12345
FLASK_DEBUG=1

```

### 6. Avvia l'applicazione

```bash
python app.py

```

Apri il browser all'indirizzo: `http://127.0.0.1:5000`

---

## 🧪 Test Consigliati

Per verificare l'efficacia del fix, prova questi prompt nell'interfaccia:

* **Matematica Avanzata:** *"Scrivimi l'equazione di campo di Einstein e spiegami i tensori."* (Osserva come la formula non "saltella" mentre viene scritta).
* **Formattazione Mista:** *"Crea una lista puntata che contenga formule inline e block math."*

---

## 📂 Struttura del Progetto

```text
/
├── app.py              # Entry point Flask e logica streaming Gemini
├── requirements.txt    # Elenco librerie Python
├── .env                # File configurazione (da non committare)
└── templates/
    └── index.html      # Frontend: UI + Logica JS di fix rendering

```

---



```

```