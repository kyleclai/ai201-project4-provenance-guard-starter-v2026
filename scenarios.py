"""
What my test runs. (Unit 8, Milestone 3)  run_eval.py executes SCENARIOS, three
trials each; check_criteria.py does the parts a string can't (appeals, logs).

Criteria are in criteria.md:
  1  none of my own writing is labeled high-confidence AI   (0 of 10)
  2  clearly-AI vs clearly-human mean combined score gap    (>= 0.30)
  3  all three labels reachable; >= 3 of 5 borderline -> unsure
  4  every valid appeal -> under_review + logged (10 of 10)  -> check_criteria.py
  5  bad input never 500s, each rejection logged            -> bodies below +
                                                                check_criteria.py

Where the text came from (be honest about it):
  MY_WRITING      ten pieces Kyle wrote himself, pasted in for this test. Names,
                  and the city in piece 9, are replaced with [Name]/[City]
                  because this file is committed to a public repo.
  AI_TEXTS        five pieces written by Claude for this test, in the plain
                  generic style language models produce. Not found, not tuned.
  BORDERLINE      five neutral pieces written by Claude to sit between the two.
                  "Borderline" is my judgment, made before any run.
  The "clearly human" set for criterion 2 reuses five of MY_WRITING (4, 5, 6,
  7, 10: the casual, note-like ones), so criteria 1 and 2 are not independent.
"""

MY_WRITING = [
"""Hi [Name]! I'm [My Name], an AI Intern here at [Company].

I'm doing a quick listening tour across the company to see how different teams use AI in their day-to-day work and gather insights for our new initiatives.

[Name] suggested I connect with you! I'd love to hear about your experiences with AI - what's working, what challenges you see, or even if you aren't using it much.

If you're open to a quick chat, let me know and I'll send over a Teams invite. Looking forward to connecting!

Sweet - that's awesome to hear! I'm excited to chat - I'll get something on your calendar for next week 😊""",

"""Hi [Name],

I'm glad you enjoyed our conversation—we did as well. I appreciate you following up with new ideas!

That sounds like an interesting pain point. It would be helpful to dig a bit deeper with a few questions.

If possible, trying to quantify that last point—i.e,  in terms of labor hours saved or cost reduction. Having a clear, measurable impact makes it much easier to build a case for leadership (also will help for our presentation 🙂).

At a minimum, being able to clearly articulate what will be easier, better, or faster once the project is complete is key.

More broadly, I'm especially interested in questions that go beyond surface-level details—ones that explore a professional's thought process, decision-making, and how they approach solving problems in their field.

Thanks again, and looking forward to hearing more.""",

"""Hi [Name],

I really enjoyed connecting and learning about your background and your team's reporting workflow. Especially using AI to build and learn a new skill at the same time, is a model I'd like to share as I meet more teams with similar workflows, and I'd love to keep learning from you as I go.

Attached is the one-pager I mentioned. It covers where to find us, what we can help with, and how to request things.

Thanks again, and feel free to reach out anytime!""",

"""if demo fails - roll with the punches. have contingency plans (consider the the amount of time, the audience im presenting, the goal of the meeting)

always be thinking abt the goal of the meeting (for all meetings): "trying to teach something, getting money, pitching product, etc..."

[manager] said if i was pitching a product i wouoldn't have sold it based on the way the presentation went (which i agree). he says need to communciate every presentation thing with [coworker] so that there's 4 different avenues to present when going into a presentation/demo (consider all backups). think abt if you were presenting for a room of 1000 ppl who came to watch your update (even its only 1 person who shows up) - doesn't mean you should overthink but just be equipped.

in practicality, sending my presentation/demo to a teammate in the future so that its there, also having it in the cloud, or having it in on usb. while this doesn't work for all presentations its just a mindset to have for going into the types of things (presentations are high risk and high reward so need to be prepared)""",

"""he also said the presentation wasn't bad and was asking for how i felt: i told him from a technnal stradnpoint there was no excuse it shouldve worked but it didn't and i  was still kinda sused bc even thought i knew how to immediately fix the problem - 50% of my brain doesn't understand why it failed and became brittle... but from a presentation standpoint, i think a pivoted but it wasn't my best work... and then [manager] said, dont say that just take it as a learning opportunity to get better....""",

"""My brain / thoughts are built for O(1) word/thought associations

Example:
Q: what is your reading superpower.
A: can always find an obvious/subliminal message in reading that applies to larger personal life context. Additionally can pair poems (rhyming schemes come readily), always thinking abt how personal experiences relate to new ones

Mental reminder: Don't get in yourself way, solve for low friction, & the simple solution is often the best

post on personal page book reviews, accomplishments at work, projects, surprises, etc

Always forgetting ideas right after thinking - lack of extended thought communication between tactile tasks (writing) and mental thoughts/states""",

"""The people I'm learning the most from are usually not teaching.

They're just doing work.

Need more opportunities to observe: decision making, prioritization, tradeoffs.

Still curious about Power BI, data engineering, automation, reporting pipelines. Need more exposure to daily work.

Interesting realization: Architecture seems less about technology. More about constraints, tradeoffs, reducing complexity.

What did I remove today? Not what did I add. What friction, uncertainty, confusion, or waste did I eliminate?""",

"""at work / in industry, are ppl actually asking you to build classifiers in Python or similar, or are they asking you to use large enterprise models like Copilot or Claude and customize them for a specific classification task? I feel like it most likely will be the second but knowing which to use could help decision making at different levels.

1. It helps to know which is cheaper. But it seems like those decisions seem to be made by leadership or the business, rather than the eng?
2. Do companies mostly want AI engineers who understand the business and bring frontier knowledge back to inform decisions, or do they still need people who build and train models from the ground up? When does the low-level work still matter?
3. How do AI engineers, ML/DL engineers, and forward-deployed engineers differ in your view? Who does each one build for?

If a role involves enabling the business to use AI tools, running training, building AI solutions for internal teams, and handling intake of AI requests. Which of these roles does that most closely match?""",

"""Hi, I'm [Name] - a [City]-based CS student who loves big data and building ML pipelines. My 2026 goal: apply that work to solve meaningful problems at scale. I learn fast, adapt faster, and I'm at my best solving real problems with good people. I believe interest is the best teacher, and community is the best accelerator. Always down to connect - say hi 👋""",

"""When building AI agents/projects - it feels very easy to get caught up in shiny add-on/connector/potentially out-of-scope that may have value later on. Esp in industry, when your managers/leadership might not actually know what's possible and want you to come back and relay a solution to a project as we're supposed to be AI SMEs.

What's your mental model / golden tidbit of advice for staying aligned with the business need while still putting on the philsophical developer hat - being able to whip a tinker to a product w creativity.""",
]

AI_TEXTS = [
"Remote work has become an increasingly important aspect of the modern workplace. It offers numerous benefits, including greater flexibility, reduced commuting time, and improved work-life balance. However, it also presents several challenges, such as communication barriers and feelings of isolation. Organizations that invest in clear communication practices and collaborative tools can overcome these obstacles. By embracing a thoughtful approach, companies can create a productive and inclusive environment for all employees.",
"Getting enough sleep is essential for maintaining good physical and mental health. Adults generally need between seven and nine hours of sleep each night to function at their best. Poor sleep can negatively affect concentration, mood, and immune function. There are several effective strategies for improving sleep quality. These include maintaining a consistent schedule, limiting screen time before bed, and creating a comfortable sleeping environment. By prioritizing rest, individuals can enhance their overall well-being.",
"Climate change is one of the most pressing challenges facing the world today. Rising global temperatures are causing more frequent extreme weather events and threatening ecosystems around the globe. Addressing this issue requires coordinated action from governments, businesses, and individuals. Transitioning to renewable energy sources and improving energy efficiency are important steps forward. Furthermore, it is crucial to invest in sustainable infrastructure. Together, we can build a more resilient and sustainable future for generations to come.",
"Effective time management is a valuable skill that can significantly improve productivity and reduce stress. By setting clear goals and prioritizing tasks, individuals can focus on what matters most. It is also important to minimize distractions and take regular breaks to maintain energy levels. Tools such as calendars and task lists can provide helpful structure. Ultimately, developing strong time management habits leads to greater efficiency and a more balanced life.",
"Cybersecurity has become a critical concern for organizations of all sizes in the digital age. Cyber threats such as phishing, malware, and data breaches can cause significant financial and reputational damage. To protect sensitive information, businesses should implement strong passwords, multi-factor authentication, and regular software updates. Employee training is also essential for recognizing potential threats. By adopting a proactive security strategy, organizations can safeguard their assets and maintain the trust of their customers.",
]

BORDERLINE = [
"The team met on Tuesday to go over the quarterly numbers. Sales were up slightly compared with last quarter, although the increase was smaller than expected. Several members raised concerns about supply delays, and it was agreed that the operations group would look into them before the next meeting.",
"We stayed at the hotel for three nights. The room was clean and the staff were friendly, but the walls were thin and the breakfast ended earlier than advertised. The location was convenient for the train station. Overall it was a reasonable place to stay for the price.",
"The library will be closed on Monday for maintenance work. Regular hours resume on Tuesday morning. Books due on Monday may be returned through the outside drop box, and no late fees will be charged for items returned by Wednesday. Questions can be sent to the front desk.",
"After reading the chapter, I think the main point is that small habits add up over time. The author gives several examples, and some of them were more convincing than others. I liked the section on routines, but the part about motivation felt a little repetitive.",
"The new phone has a bright screen and a good camera, and the battery lasts most of a full day. It is a bit heavy, and the fingerprint reader is not always accurate. For the money, it is decent, though I would wait for a sale if you are not in a hurry.",
]

SCENARIOS = [
    {"name": "my own writing (10 pieces)", "criterion": 1, "texts": MY_WRITING},
    {"name": "clearly AI (5)", "criterion": 2, "texts": AI_TEXTS},
    {"name": "clearly human (5 of my own)", "criterion": 2,
     "texts": [MY_WRITING[i] for i in (3, 4, 5, 6, 9)]},
    {"name": "borderline (5)", "criterion": 3, "texts": BORDERLINE},
    {
        "name": "bad input",
        "criterion": 5,
        "bodies": [
            {"creator_id": "eval_bad_missing_text"},
            {"text": "", "creator_id": "eval_bad_empty"},
            {"text": "   \n\t  ", "creator_id": "eval_bad_whitespace"},
            {"text": 12345, "creator_id": "eval_bad_nonstring"},
            {"text": "Some perfectly fine text for scoring.", },
            {"text": "word " * 50000, "creator_id": "eval_bad_huge"},
        ],
    },
    # Criterion 4 (appeals) and the non-JSON-body case of criterion 5 are in
    # check_criteria.py: they need a submission first, or a non-JSON body.
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
