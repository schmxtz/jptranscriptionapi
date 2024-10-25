import spacy
import time

nlp = spacy.load('de_core_news_sm')
st = time.monotonic_ns()
doc = nlp("In einem kleinen Dorf namens St. Moritz am Fuße der Berge lebte einst ein alter Mann namens Friedrich. Er war bekannt für seine Geschichten, die er den Kindern am Abend erzählte. Die Kinder versammelten sich um ihn, während er am Feuer saß und mit seiner rauen Stimme von Abenteuern in fernen Ländern berichtete. Eines Tages beschloss er, eine Reise zu unternehmen, um die Orte zu besuchen, von denen er so oft erzählt hatte. Er packte seinen Rucksack mit Proviant und machte sich auf den Weg. Auf seiner Reise begegnete er vielen interessanten Menschen: einem weisen alten Fischer am See, einer mutigen Bäuerin, die ihre Felder bestellte, und einem jungen Künstler, der die Schönheit der Natur auf Leinwand bannte. Jeder von ihnen hatte eine eigene Geschichte zu erzählen, und Friedrich hörte aufmerksam zu. Nach Wochen des Reisens kehrte er schließlich in sein Dorf zurück, bereichert durch die Erfahrungen und Freundschaften, die er geschlossen hatte. Die Kinder lauschten gebannt seinen neuen Geschichten und lernten, dass das Leben voller Wunder und Überraschungen steckt.")
end = time.monotonic_ns()
print(f'time: {(end-st)/1000000}', )
token = '" "'.join([token.text for token in doc])
print(token)
