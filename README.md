# PenguinDeployer

Titolo del progetto
Sviluppo di un’interfaccia interattiva per la personalizzazione delle impostazioni di sistema e
la gestione del software in Linux
Obiettivo
Realizzare uno strumento con interfaccia testuale o grafica che consenta agli utenti (anche non
esperti) di modificare le principali impostazioni di sistema e gestire i pacchetti software,
facilitando la configurazione post-installazione o l’uso didattico.
Contenuti principali
1. Introduzione teorica
• Comandi e file principali per la configurazione di sistema Linux.
• Gestione del software: apt, snap, flatpak.
• Shell scripting per automazione.
2. Scenario
• Creazione di una utility di configurazione post-installazione che consenta all'utente di:
o Installare software consigliato.
o Abilitare/disabilitare servizi.
o Configurare il nome host, la rete o la shell.
o Personalizzare l’ambiente utente (prompt, editor, temi desktop).
3. Funzionalità dell’interfaccia
Moduli suggeriti:
✅ Configurazione di sistema:
• Impostazione di hostname.
• Configurazione DNS o rete.
• Scelta shell predefinita (bash, zsh, fish).
• Impostazione di alias utili (ll, update, ecc.).
✅ Gestione pacchetti software:
• Installazione pacchetti consigliati (editor, browser, strumenti di rete).
• Rimozione pacchetti inutili.
• Aggiornamento del sistema.
✅ Servizi di sistema:
• Attivazione/disattivazione servizi (systemctl).
• Avvio automatico (es. SSH, Apache, Docker).
✅ Backup configurazioni:
• Salvataggio delle impostazioni utente in file .tar.gz o .conf.
4. Automazione
• Uso di script per:
o Salvare e ripristinare configurazioni.
o Installare pacchetti in batch.
o Applicare modifiche senza riavvio.
5. Testing e validazione
• Verifica delle modifiche a sistema (hostname, shell, pacchetti installati).
• Test di revert (ripristino delle configurazioni originali).
6. Documentazione
• Relazione tecnica (min. 15–20 pagine).
o Architettura dell’interfaccia.
o Codice sorgente commentato.
o Screenshot dei menu/interfacce.
• Manuale utente per chi usa lo strumento.
• Slide per presentazione orale (5–10 slide).
Output richiesti
• Relazione
• Presentazione.
