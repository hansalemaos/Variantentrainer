from random import randrange, shuffle
import zipfile
import regex
import pandas as pd
import spacy
from satzmetzger.satzmetzger import Satzmetzger
from add_color_print_reg import *
from time import sleep as timesleep
from operator import indexOf
import de_dep_news_trf
satzanalyse_werkzeug = de_dep_news_trf.load()
from einfuehrung import einfuehrung
from maximize_console import maximize_console

wikitexte='wikitext.dat'
filepath = r"v.zip"
satzmetzgerle = Satzmetzger()
woerterzumtrainieren=[]
def read_zipfile(filepath, woerterholen):
    regexfuergewaehltewoerter=''
    woerterholenmitprefix = ['v/' + x.strip() + '.txt' for x in woerterholen]
    woerterfueraufgabe = []
    try:
        with zipfile.ZipFile(
                filepath, mode="r", allowZip64=True
        ) as file:  
            alledateien = file.namelist()

            for www in woerterholenmitprefix:
                try:
                    dateiindex = indexOf(alledateien, www)
                    text_file = file.open(name=alledateien[dateiindex], mode="r")
                    daten = text_file.read()
                    daten = daten.decode("utf-8")
                    daten = str(daten).splitlines()
                    daten = [x.strip() for x in daten]
                    for ddd in daten:
                        woerterfueraufgabe.append(ddd)
                    text_file.close()

                except Exception as Fehler:
                    nichtgefunden = regex.sub('^v/', '', www)
                    nichtgefunden = regex.sub('\.txt$', '', nichtgefunden)
                    print(drucker.f.red.brightwhite.italic(f'  Wort "{nichtgefunden}" nicht in Varianten gefunden, ich werde nur die Grundform benutzen'))
                    woerterfueraufgabe.append(nichtgefunden)


    except Exception as Fehler:
        print(Fehler)
        pass
    print(drucker.f.brightwhite.cyan.normal('  Ich habe folgende Varianten gefunden: '))
    for indi,wwww in enumerate(woerterfueraufgabe):
        if indi%2 == 0:
            print(drucker.f.black.brightcyan.italic(f'{str(indi).zfill(4)})    ') + drucker.f.brightcyan.black.italic(f'{wwww}'))
        if indi%2 != 0:
            print(drucker.f.brightcyan.black.italic(f'{str(indi).zfill(4)})    ') + drucker.f.black.brightcyan.italic(
                f'{wwww}'))
    return woerterfueraufgabe.copy()




def alle_antworten_drucken(alleantwortendict):
    zaehler = 0
    for key, item in alleantwortendict.items():
        if zaehler % 2 == 0:
            print(drucker.f.cyan.black.italic(f"  {key}) {item}"))
        elif zaehler % 2 != 0:
            print(drucker.f.black.cyan.italic(f"  {key}) {item}"))
        zaehler = zaehler + 1
    user_pronominal = input(
        drucker.f.brightyellow.black.italic("  Bitte richtige Antwort eingeben")
    ).strip()
    if user_pronominal.isnumeric():
        try:
            user_pronominal = int(user_pronominal)
            return alleantwortendict[user_pronominal]
        except:
            return ""
    return user_pronominal.strip().lower()


def get_falsche_antworten(richtigeantwort, wievieleantworten=3):
    fertigeliste = []
    while len(fertigeliste) < wievieleantworten:

        fertigeliste.append(choice(woerterzumtrainieren))
        fertigeliste = list(dict.fromkeys(fertigeliste))
        fertigeliste = [x for x in fertigeliste if x != richtigeantwort]
        if len(fertigeliste) == len(woerterzumtrainieren) - 1:
            break
    return fertigeliste.copy()

def read_zipfile_wiki(wikitexte):
    allesaetzemitpronominaladverbienalle=[]
    try:
        with zipfile.ZipFile(
            wikitexte, mode="r", allowZip64=True
        ) as file:
            dateiliste = file.namelist()
            shuffle(dateiliste)
            for indineu, einzelnedatei in enumerate(dateiliste):
                try:
                    text_file = file.open(name=einzelnedatei, mode="r")
                    daten = text_file.read()
                    daten = daten.decode("utf-8")
                    allesaetzemitpronominaladverbien = pronomfinden.findall(daten)
                    allesaetzemitpronominaladverbien = [
                        (x[1], x[0])
                        for x in allesaetzemitpronominaladverbien]
                    print(drucker.f.blue.black.italic(f'Sätze werden durchsucht, bitte warten {indineu}'))
                    if any(allesaetzemitpronominaladverbien):
                        for gutersatz in allesaetzemitpronominaladverbien:
                            allesaetzemitpronominaladverbienalle.append(gutersatz)
                    text_file.close()
                except Exception as Fehler:
                    continue
            return allesaetzemitpronominaladverbienalle.copy()
    except Exception as Fehler:
        pass



def delete_duplicates_from_nested_list(nestedlist):
    """01.11"""
    tempstringlist = {}
    for ergi in nestedlist:
        tempstringlist[str(ergi)] = ergi
    endliste = [tempstringlist[key] for key in tempstringlist.keys()]
    return endliste.copy()

if __name__ == "__main__":
    maximize_console()
    einfuehrung('Variantentrainer')
    allemoeglichenpunkte = 0
    punktevomuser = 0

    try:
        woerterzumtrainieren = input( drucker.f.magenta.black.negative('\n  Welche Wörter möchtest du üben?\n') +
            drucker.f.black.magenta.negative(
                "\nGib mir eine Liste wie z.B.\nverschreiben,beschreiben,aufschreiben,schreiben\nverschreiben, beschreiben, aufschreiben, schreiben\nverschreiben beschreiben aufschreiben schreiben\nverschreiben|beschreiben|aufschreiben|schreiben\nverschreiben/beschreiben/aufschreiben/schreiben\nverschreiben;beschreiben;aufschreiben;schreiben\n"
            )
        )
        woerterzumtrainieren = regex.findall(r'\b[\w+-]+\b', str(woerterzumtrainieren))
        woerterzumtrainieren = [x for x in woerterzumtrainieren if len(x) > 1]
        print(drucker.f.brightwhite.cyan.normal('  Du hast folgende Wörter gewählt: '))
        for indi, wwww in enumerate(woerterzumtrainieren):
            if indi % 2 == 0:
                print(
                    drucker.f.black.brightcyan.italic(f'  {str(indi).zfill(4)})    ') + drucker.f.brightcyan.black.italic(
                        f'{wwww}'))
            if indi % 2 != 0:
                print(
                    drucker.f.brightcyan.black.italic(f'  {str(indi).zfill(4)})    ') + drucker.f.black.brightcyan.italic(
                        f'{wwww}'))

    except:
        print("Fehler bei der Eingabe! Programm wird gleich beendet")
        timesleep(10)

    try:
        derivatetrainierensuchen = True
        derivatetrainieren = input(drucker.f.magenta.black.negative('\nMöchtest du auch Varianten trainieren?\n') +
            drucker.f.black.magenta.negative(
                "\nEin paar Beispiele für 'aufschreiben':\naufgeschrieben, aufgeschriebene, aufgeschriebenes\n\n\nn - nein\nj - ja\n"
            )
        )
        if derivatetrainieren.strip().lower() == 'n':
            derivatetrainierensuchen = False

    except:
        derivatetrainierensuchen = True

    if derivatetrainierensuchen is True:
        woerterzumtrainieren = read_zipfile(filepath, woerterzumtrainieren)

    regexfuergewaehltewoerter = r"""[.!?]\s+([^!?.]+[.?!]\s+[^!?.]*\b(""" + '|'.join(
        [f'(?:{x})' for x in woerterzumtrainieren]) + r""")\b[^!?.]*?[^!?.]*[?!.])"""
    pronomfinden = regex.compile(regexfuergewaehltewoerter)


    try:
        aufgabenmaximalgenerieren = input(
            drucker.f.magenta.black.italic(
                "  Wie viele Aufgaben sollen ungefähr generiert werden?"
            )
        )
        aufgabenmaximalgenerieren = int(aufgabenmaximalgenerieren)
    except:
        print("  Fehler bei der Eingabe! Ich probiere, ungefähr 50 Aufgaben zu generieren!")
        aufgabenmaximalgenerieren = 50
    linebreakx = 70
    wrapper = TextWrapper(width=linebreakx)
    allemoeglichenpunkte = 0
    punktevomuser = 0
    print(
        drucker.f.brightwhite.red.italic(
            "     Achtung: Aufgaben werden generiert! Das dauert zwischen 2 und 5 Minuten!  "
        )
    )

    allesaetzemitpronominaladverbien = read_zipfile_wiki(wikitexte)
    df = pd.DataFrame(allesaetzemitpronominaladverbien)
    df.columns = ["wort_trainieren", "satz"]
    df = df.loc[~df.satz.str.contains(r"\d+:\d")]
    df2 = pd.DataFrame(df.groupby('wort_trainieren')).copy()
    df2.columns = ['wort', 'infos']
    df2['saetzegefunden'] = df2.infos.apply(len)
    saetzezumerstellen = []

    df2 = df2.loc[df2.saetzegefunden > 0].copy()
    vonjedemnehmen = int(aufgabenmaximalgenerieren / len(df2) * 2)





    antwortenundsatz = []
    for indi, row in df2.iterrows():
        antwortenundsatzsubliste = []
        for indi2, row2 in row.infos.iterrows():
            antwortenundsatzsubliste.append((row.wort, row2.satz))
            antwortenundsatzsubliste = delete_duplicates_from_nested_list(nestedlist=antwortenundsatzsubliste)
            if len(antwortenundsatzsubliste) >= vonjedemnehmen:
                break
        for antwortoption in antwortenundsatzsubliste:
            antwortenundsatz.append(antwortoption)
    shuffle(antwortenundsatz)
    df3 = pd.DataFrame.from_records(antwortenundsatz)
    df3.columns = ['wort', 'satz']
    df3["spacy"] = df3.satz.apply(satzanalyse_werkzeug)
    df3.reset_index(inplace=True, drop=True)
    for satznummer in range(df3.shape[0]):
        alsjson = df3.spacy[satznummer].to_json()
        allemoeglichenpunkte = allemoeglichenpunkte + 1

        for wort in alsjson['tokens']:

            startwort = wort['start']
            endewort = wort['end']
            originalwort = alsjson['text'][startwort:endewort]
            if df3.wort[satznummer] == originalwort:
                fragestellen = alsjson['text'].replace(originalwort, '_____')
                print('\n'.join(wrapper.wrap(drucker.f.brightwhite.black.normal(f'\n{fragestellen}\n'))))
                teileinstipps = regex.split(r'\|', wort['morph'])
                teileinstipps = '\n'.join([f'     {x}' for x in teileinstipps])
                antwortvomuser = input(drucker.f.black.brightwhite.normal(f"\n  Tipps:\n     Wortart: \n     {wort['pos']}  \n     Weitere details: \n{teileinstipps}\n"))
                if antwortvomuser.strip() == originalwort:
                    print(
                        drucker.f.brightwhite.brightgreen.italic(
                            "     Super! Deine Antwort: "
                        )
                        + drucker.f.brightgreen.black.negative(
                            f"   '{antwortvomuser.strip()}' war richtig     "
                        )
                    )
                    punktevomuser = punktevomuser +1
                elif antwortvomuser.strip() != originalwort:
                    print(
                        drucker.f.brightwhite.red.italic(
                            "    Deine Antwort: "
                        )
                        + drucker.f.red.black.negative(
                            f"   '{antwortvomuser.strip()}' war leider falsch! Die richtige Antwort ist: {originalwort}"
                        )
                    )
                print(
                    drucker.f.magenta.black.italic(
                        f"  Deine Punktzahl: {punktevomuser}\nMaximale Punktzahl: {allemoeglichenpunkte}\n"
                    )
                )
                print(3 * "\n")
