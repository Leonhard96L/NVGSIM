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


## Using github:
1. Git bash open in dir NVGSIM
2. git status 
3. git pull
4. git add . -> alles in diesem Verzeichnis
5. git commit -m "Schreibe Information ueber diesen commit"
6. git push

## TODO:
 - Überlegung - zzt: ref_dir und test_dir an tester übergeben
   - Können wir nicht einfach ref -> test dir kopieren und dann in test_dir arbeiten?
   - Dazu ein neues feld zum Eingeben der ref_dir (sont automatisch das neuste MQTG)
 - evtl noch checks für valid file handles und dirs
 - generell error catching und handling (in gui)

### DONE
- Speichern der berichte ins richtige dir und mit richtigen namen.	DONE
- Header hinzufügen	DONE
- Struktur anpassen (mit Leo)	DONE
- Tabelle neu generieren (änderungen von Leo)    DONE
    - einheiten hinzufügen
    - MQTG: Init_condition_Reference, Init_condition_MQTG
    - Reference Ü, MQTG
    - QTG: Init_condition_Reference, Init_condition_MQTG, Init_condition_Reccurent
    - Reference *, MQTG, Recurrent
- IO mit Leo    DONE

- Hauptbericht generieren    DONE
