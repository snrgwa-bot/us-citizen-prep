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

FEATURES = [
    ("Exam simulator", "The real format, start to finish",
     "Up to 20 questions asked one at a time. Pass with 12, and the exam ends at 9 wrong, as it does at the interview. In 65/20 mode it becomes 10 questions and a pass at 6.",
     "app-exam.jpg", "The exam simulator showing question 1 of 20 with four answer choices", "#4F6BFF", "#7B5CFF"),
    ("Audio Interview", "Answer out loud, like the real thing",
     "The officer asks out loud and you answer out loud. The app listens, checks what you said against every accepted answer, and stops when you stop talking.",
     "app-audio.jpg", "The Audio Interview screen with a question from the officer and a microphone button", "#FF6A88", "#FF4D6D"),
    ("Flashcards", "All 128 questions, with a voice",
     "Swipe what you know and keep what you are still learning. Tap Listen to hear the question and its answer read aloud.",
     "app-cards.jpg", "A flashcard asking a history question with Still learning and Got it buttons", "#22C9B8", "#18A7D8"),
    ("Your language", "Study in the language you think in",
     "Questions and answers in English, Spanish, French, German, Russian, Ukrainian, Chinese and Arabic. One tap translates a practice question; one more brings back the English you will hear at the interview.",
     "app-translate.jpg", "A practice question translated into Chinese with a button to switch back to English", "#FFB020", "#FF8A1F"),
    ("Progress", "See exactly what is left",
     "A week of study at a glance, your streak, and how much of Government, History, Symbols and Rights you have learned, so you know when you are ready.",
     "app-progress.jpg", "The Progress screen with a weekly chart, streak and mastery by topic", "#3D5CFF", "#6B4DFF"),
]
features = "\n".join(
    f'''      <article class="feat{" feat--flip" if i % 2 else ""}">
        <div class="feat__text reveal">
          <p class="chip" style="--a:{c1};--b:{c2}">{tag}</p>
          <h3>{title}</h3>
          <p>{text}</p>
        </div>
        <div class="feat__phone reveal" style="--a:{c1};--b:{c2}">
          <div class="phone"><img src="img/{img}" width="660" height="1434" alt="{alt}" loading="lazy"></div>
        </div>
      </article>''' for i, (tag, title, text, img, alt, c1, c2) in enumerate(FEATURES))

FAQ = [
    ("Are the questions up to date?", "Yes. The app uses the current USCIS civics test, all 128 questions, the version in use today. Answers that change (the President, the Speaker, your governor and senators) are refreshed from a public file once a day when you are online, so an election never leaves you with an old name."),
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
faq = "\n".join(f'        <details class="qa reveal"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)

html = open("page.html").read()
for key, val in {"{{FEATURES}}": features, "{{FAQ}}": faq,
                 "{{PRIVACY}}": body, "{{STORE}}": STORE}.items():
    html = html.replace(key, val)
open("index.html", "w").write(html)
print("index.html", len(html))
