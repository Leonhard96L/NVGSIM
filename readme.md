## Ablauf

1. QTGs auswählen
2. START MQTG / QTG
3. Tests werden nach der Reihe ausgeführt. Tests werden von QTG_Generator gesteuert und output/input wird gehandled
    - Plots werden von den tests generiert und ins richtige verzeichnis gespeichert. Werden später erneut geladen
4. Testberichte werden angefertigt
	Teilberichte mit Header
	Hauptbericht mit Header, Teilberichte ohne header anfügen
	A) Teilberichte 2x speichern, 1x mit header
		Create header file und join PDF??
	B) Test mit header erstellen, später weg werfen??
	C) Code für test_case kopieren, jedes mal alles neu rendern	<THIS.>
5. Fertig :)

## TODO:
- Speichern der berichte ins richtige dir und mit richtigen namen.	DONE
- Header hinzufügen	DONE
- Struktur anpassen (mit Leo)	DONE
- Tabelle neu generieren (änderungen von Leo)
	- einheiten hinzufügen
	- MQTG: Init_condition_Reference, Init_condition_MQTG
    - Reference Ü, MQTG
    - QTG: Init_condition_Reference, Init_condition_MQTG, Init_condition_Reccurent
    - Reference *, MQTG, Recurrent
- IO mit Leo
