"""Builds index.html for the US Naturalization Prep 2027 site. Run: python3 build.py
The privacy text comes from privacy.html so the two never drift apart."""
import re

priv = open("privacy.html").read()
body = priv[priv.index("<h1>"):]
body = body[body.index("</h1>") + 5:]
body = body[:body.rindex("</body>")]
body = re.sub(r"</(main|div)>\s*$", "", body.strip())
body = re.sub(r'\sclass="[^"]*"', "", body)
body = body.replace("<h2>", "<h3>").replace("</h2>", "</h3>")

STORE = "https://apps.apple.com/app/id6766182846"

SLIPS = [
    ("What is the supreme law of the land?", ["(U.S.) Constitution"], 34, 0),
    ("Why does the flag have 13 stripes?", ["(Because there were) 13 original colonies", "(Because the stripes) represent the original colonies"], 44, -1.5),
    ("When was the Declaration of Independence adopted?", ["July 4, 1776"], 30, 0),
    ("What is the rule of law?", ["Everyone must follow the law.", "Leaders must obey the law.", "Government must obey the law.", "No one is above the law."], 42, 1.5),
    ("What territory did the United States buy from France in 1803?", ["Louisiana Territory", "Louisiana"], 36, 0),
    ("What does the President’s Cabinet do?", ["Advises the President (of the United States)"], 28, -1),
]
slips = "\n".join(
    f'''        <article class="slip rise" style="--h:{h}svh;--tilt:{t}deg">
          <p class="slip__q">{q}</p>
          <p class="slip__rule" aria-hidden="true">· · · · · · · · · · · ·</p>
          <ul>{"".join(f"<li>{a}</li>" for a in ans)}</ul>
        </article>''' for q, ans, h, t in SLIPS)

SHEETS = [
    ("Exam simulator", "slate", "app-exam.jpg",
     "The real format: up to 20 questions asked one at a time, pass with 12, and the exam ends at 9 wrong, as it does at the interview. In 65/20 mode it becomes 10 questions and a pass at 6.",
     "The exam simulator showing question 1 of 20 with four answer choices"),
    ("Audio Interview", "blue", "app-audio.jpg",
     "The officer asks out loud and you answer out loud. The app listens, checks what you said against every accepted answer, and stops when you stop talking.",
     "The Audio Interview screen with a question from the officer and a microphone button"),
    ("Flashcards with a voice", "teal", "app-cards.jpg",
     "All 128 official questions. Swipe what you know, keep what you are still learning, and tap Listen to hear the question and its answer read aloud.",
     "A flashcard asking a history question with Still learning and Got it buttons"),
    ("Study in your language", "amber", "app-translate.jpg",
     "Questions and answers in English, Spanish, French, German, Russian, Ukrainian, Chinese and Arabic. One tap on a practice question shows it in your language; one more brings back the English you will hear at the interview.",
     "A practice question translated into Chinese with a button to switch back to English"),
    ("See what is left", "coral", "app-progress.jpg",
     "A week of study at a glance, your streak, and how much of Government, History, Symbols and Rights you have learned, so you know when you are ready.",
     "The Progress screen with a weekly chart, streak and mastery by topic"),
]
sheets = "\n".join(
    f'''      <article class="sheet sheet--{tone}" style="--i:{i}">
        <h3 class="sheet__name">{name}</h3>
        <p class="sheet__text">{text}</p>
        <div class="sheet__pic"><img src="img/{img}" width="660" height="1434" alt="{alt}" loading="lazy"></div>
      </article>''' for i, (name, tone, img, text, alt) in enumerate(SHEETS))

MOMENTS = [
    ("You check in", "Bring your appointment notice and green card. The officer calls your name and walks you to the office.", 96, "assets/citizenship-ceremony-8142304276.jpg", "People seated under a white tent at an outdoor citizenship ceremony", "60% 50%"),
    ("You swear to tell the truth", "Standing, right hand raised. Everything after this is part of your English speaking test.", 132, "assets/citizenship-ceremony-8142299052.jpg", "A row of people with their right hands raised taking an oath", "50% 40%"),
    ("You read one sentence", "You get three chances to read one sentence aloud correctly. The app's Reading test listens to you read.", 80, "img/app-home.jpg", "The app's home screen with interview readiness at 77 percent", "50% 0%"),
    ("You write one sentence", "The officer says a sentence and you write it. Three chances for one correct sentence. Practice it in the Writing test.", 140, "img/app-translate.jpg", "A practice question shown in the app", "50% 0%"),
    ("Up to 20 civics questions", "Asked out loud from the list of 128. You pass with 12 correct, and the officer stops as soon as you reach it.", 104, "img/app-exam.jpg", "The exam simulator on question 1 of 20", "50% 0%"),
    ("Questions about your state", "Your governor, one of your senators, your capital. These change after elections, so the app updates them for you.", 124, "img/app-cards.jpg", "A flashcard in the app", "50% 0%"),
    ("You take the oath", "Pass, and you are scheduled for the ceremony. That day you become a citizen of the United States.", 88, "assets/meeting-room-faneuil-hall-naturalization-ceremony-oath.jpg", "A naturalization ceremony inside Faneuil Hall in Boston", "50% 75%"),
]
moments = "\n".join(
    f'''        <li class="moment">
          <p class="moment__cap">{cap}</p>
          <p class="moment__text">{text}</p>
          <div class="moment__gap" style="height:{gap}px"></div>
          <img src="{src}" alt="{alt}" width="560" height="700" loading="lazy" style="object-position:{pos}">
        </li>''' for cap, text, gap, src, alt, pos in MOMENTS)

FAQ = [
    ("Are the questions up to date?", "Yes. The app uses the full 2025 USCIS civics test, all 128 questions. Answers that change (the President, the Speaker, your governor and senators) are refreshed from a public file once a day when you are online, so an election never leaves you with an old name."),
    ("Is this the 100-question test or the 128-question test?", "The 128-question test. People who filed Form N-400 on or after October 20, 2025 take it: up to 20 questions, 12 correct to pass. If you filed earlier you take the 2008 test with 100 questions, which this app does not cover."),
    ("What is 65/20 mode?", "If you are 65 or older and have been a permanent resident for 20 years or more, you study 20 marked questions and are asked 10; 6 correct is a pass. Turn it on in Settings (the gear, top right) and every test follows those rules."),
    ("How do I change my state?", "Open Settings with the gear at the top right and choose Current State. Your governor, senators and capital change at once."),
    ("How do I study in my language?", "Choose a language in Settings. Flashcards show both languages, and a translate button on each practice question switches it and its answers. The exam simulator stays in English unless 65/20 mode is on, because that is the rule at the real interview."),
    ("Does it work offline?", "Yes. Questions, answers, translations, voices and your progress are on your phone. Only the daily check for new officials needs a connection."),
    ("What is free?", "Flashcards for all 128 questions and one 10-question practice test every day. A short video ad opens one more test. Your first day includes every Pro tool."),
    ("What does Pro add?", "The exam simulator, unlimited practice, your state's answers, the English reading and writing test, the Audio Interview with voices, and no ads. Weekly, monthly, yearly or once for life."),
    ("How do I cancel a subscription?", "In the app: Settings, then Manage Subscription. Or on your iPhone: Settings, your name, Subscriptions."),
    ("I found a wrong answer. What now?", "Tell us. Email essentialdevteam@gmail.com with the question number, or use Settings, Report a Bug. We check every report against the USCIS list and correct the file the same day when it is wrong."),
    ("Is this an official USCIS app?", "No. It is an independent study aid made by Essential Dev Team. It is not affiliated with or endorsed by USCIS or any government agency. The civics questions themselves are published by USCIS."),
]
faq = "\n".join(f'        <p><strong>{q}</strong> {a}</p>' for q, a in FAQ)

html = open("template.html").read()
for key, val in {"{{SLIPS}}": slips, "{{SHEETS}}": sheets, "{{MOMENTS}}": moments, "{{FAQ}}": faq,
                 "{{PRIVACY}}": body, "{{STORE}}": STORE}.items():
    html = html.replace(key, val)
open("index.html", "w").write(html)
print("index.html", len(html))
