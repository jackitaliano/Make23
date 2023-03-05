import functions.chat as chat
import functions.search as search
import json

keys:str

with open('keys.json', 'r') as file:
    keys = json.load(file)
    
open = keys['openai']
bing = keys['bing']

text1 = "Now, there’s a few things to note about this passage. First, it’s incredibly sexist. It assumes not just merely in reflexive use of phrases. It assumes that — William James assumes he’s talking to males, male humans who sometimes take the perspective of male bears. And so, it assumes a male audience. You wouldn’t normally — You wouldn’t actually ever write this way. A second point is it’s beautifully written and you’re not — ;also, not allowed to write that way anymore either. It’s poetic and lyrical and if — William James characteristically writes that way. I think he writes so much better than his brother, Henry James, an obscure novelist. [laughter] Finally though, the point that he makes is a terrific one, which is yes, all of these things seem natural to us but the reason why they seem natural is not because they are in some sense necessary or logical truths. Rather, they emerge from contingent aspects of our biological nature."
text2 = "Emotions set goals and establish priorities. And without them you wouldn’t do anything, you couldn’t do anything. Your desire to come to class to study, to go out with friends, to read a book, to raise a family, to be — to do anything are priorities set by your emotions. Life would be impossible without those emotions. And so, there’s certain themes we’re going to explore here. The first is this, that emotions are basically mechanisms that set goals and priorities and we’re going to talk a lot about — in this class and the next class about universals. We’re also going to talk about culture. It turns out that cultures, different cultures, including differences between America and Japan and the American South and the American North, have somewhat different emotional triggers and emotional baselines to respond to. But at the same time, as Darwin well knew, emotions have universal roots that are shared across all humans and across many animals."
context = ""

notes = chat.summarize(open, context, text2)
url = search.search(open, bing, notes)

print(notes)

print(f'\nAdditional Resources:\n{url["title"]}: {url["url"]}')
