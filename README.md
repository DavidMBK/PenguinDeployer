# Progetto: Sviluppo di un’interfaccia interattiva per la personalizzazione delle impostazioni di sistema e la gestione del software in Linux

## 🎯 Obiettivo

Realizzare uno strumento con interfaccia testuale o grafica che consenta agli utenti (anche non esperti) di modificare le principali impostazioni di sistema e gestire i pacchetti software, facilitando la configurazione post-installazione o l’uso didattico.

---

## 📚 Contenuti principali

### 1. Introduzione teorica

- Comandi e file principali per la configurazione del sistema Linux.
- Gestione del software tramite:
  - `apt`
  - `snap`
  - `flatpak`
- Shell scripting per l’automazione delle attività.

---

### 2. Scenario

Creazione di una utility per la **configurazione post-installazione**, che consenta all’utente di:

- Installare software consigliato.
- Abilitare o disabilitare servizi di sistema.
- Configurare:
  - Nome host
  - Rete
  - Shell predefinita
- Personalizzare l’ambiente utente:
  - Prompt
  - Editor predefinito
  - Temi desktop (se disponibile)

---

### 3. Funzionalità dell’interfaccia

#### ✅ Modulo: Configurazione di sistema

- Impostazione hostname.
- Configurazione della rete (DNS, IP statico/dinamico).
- Selezione della shell predefinita: `bash`, `zsh`, `fish`.
- Definizione di alias comuni: `ll`, `update`, ecc.

#### ✅ Modulo: Gestione pacchetti software

- Installazione di pacchetti consigliati: editor, browser, strumenti di rete.
- Rimozione di pacchetti inutili.
- Aggiornamento completo del sistema.

#### ✅ Modulo: Servizi di sistema

- Abilitazione/disabilitazione servizi tramite `systemctl`.
- Gestione dell'avvio automatico di servizi come:
  - `ssh`
  - `apache2`
  - `docker`

#### ✅ Modulo: Backup configurazioni

- Salvataggio delle impostazioni utente in file `.tar.gz` o `.conf`.
- Esportazione/importazione delle configurazioni.

---

### 4. Automazione

Utilizzo di **script shell** per:

- Salvare e ripristinare configurazioni personalizzate.
- Installare pacchetti in modalità batch.
- Applicare modifiche senza necessità di riavvio del sistema.

---

### 5. Testing e validazione

- Verifica delle modifiche apportate:
  - Hostname aggiornato
  - Shell attiva
  - Pacchetti installati/disinstallati
- Test di **ripristino delle configurazioni originali**.

---

### 6. Documentazione

#### 📝 Relazione tecnica (15–20 pagine)

- Architettura dell’interfaccia.
- Codice sorgente documentato.
- Screenshot delle interfacce e dei menu.

#### 📘 Manuale utente

- Guida all’uso per utenti inesperti o studenti.

#### 📊 Slide presentazione orale

- 5–10 slide con:
  - Obiettivi
  - Architettura
  - Dimostrazione delle funzionalità
  - Conclusioni

---

## ✅ Output richiesti

- 📄 Relazione tecnica
- 📘 Manuale utente
- 📊 Presentazione (slide)

---

## 🔧 Tecnologie e strumenti suggeriti

- **Linguaggi:** Bash, Python (Tkinter o curses), Zenity, YAD
- **Ambienti di test:** Debian/Ubuntu-based (VirtualBox, WSL, macchina reale)
- **Gestori pacchetti:** `apt`, `snap`, `flatpak`
- **Controllo servizi:** `systemctl`, `service`

---

## 📌 Note finali

Il progetto è pensato per essere **modulare e facilmente estendibile**, offrendo un'esperienza utente intuitiva e utile sia in ambito didattico che professionale.
