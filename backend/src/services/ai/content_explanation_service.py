import logging
import re
from typing import Dict, Any, Optional
from src.services.ai.ai_provider import get_ai_provider
from src.services.ai.source_context_service import load_syllabus_and_pyq_context

logger = logging.getLogger(__name__)

# Comprehensive Curated Knowledge Base for TNPSC & Civil Services Topics
CURATED_KNOWLEDGE: Dict[str, Dict[str, Any]] = {
    'indus valley': {
        'title': 'Indus Valley Civilisation (Harappan Civilisation)',
        'definition': (
            "The Indus Valley Civilisation (c. 2500 BCE – 1900 BCE) was a Bronze Age urban civilization located "
            "in the northwestern region of South Asia, primarily along the Indus and Ghaggar-Hakra river basins "
            "(modern-day India and Pakistan). It is renowned as one of the world's earliest advanced urban cultures "
            "alongside ancient Mesopotamia and Egypt."
        ),
        'key_features': [
            "**Grid Pattern Town Planning**: Cities were divided into a Citadel (western fortified administrative area) and Lower Town (eastern residential quarters), with broad streets intersecting precisely at 90-degree right angles.",
            "**Burnt Brick Architecture**: Houses were built using standardized burnt bricks in a 1:2:4 ratio (thickness:width:length), featuring multiple rooms, courtyards, and private wells.",
            "**Advanced Drainage System**: Underground covered drainage running beneath streets with regular inspection manholes and soak pits—unsurpassed in the ancient world.",
            "**Standardized Metrology**: Advanced system of weights and measures following binary (1, 2, 4, 8, 16, 32, 64) and decimal multiples.",
            "**Trade & Economy**: Extensive trade networks extending to Mesopotamia (where Indus merchants were called *Meluhha*), Dilmun (Bahrain), and Magan (Oman). First people in the world to cultivate cotton (*Sindon*).",
            "**Art & Seals**: Steatite seals featuring the Unicorn motif, Pashupati (proto-Shiva surrounded by elephant, tiger, rhino, and buffalo), and the famous lost-wax bronze statue of the 'Dancing Girl' from Mohenjo-Daro.",
            "**Peaceful Society**: Notably lacked royal palaces, monumental temples, or standing armies; social organization was driven primarily by commerce, craftsmanship, and civic administration."
        ],
        'major_sites': [
            "**Harappa** (Punjab, Pakistan on Ravi River): Excavated by Daya Ram Sahni (1921); famous for 6 granaries in rows, coffin burials, and red sandstone male torso.",
            "**Mohenjo-Daro** (Sindh, Pakistan on Indus River): Excavated by R.D. Banerjee (1922); known as 'Mound of the Dead'; site of the Great Bath, Great Granary, Bronze Dancing Girl, and Bearded Priest.",
            "**Lothal** (Gujarat on Bhogava River): Excavated by S.R. Rao; world's earliest known tidal dockyard, international maritime trade port, and bead-making factory.",
            "**Dholavira** (Kutch, Gujarat): Excavated by R.S. Bisht; unique 3-tier city division (Citadel, Middle, Lower), giant signboard with 10 Indus script symbols, and water conservation reservoirs.",
            "**Kalibangan** (Rajasthan on Ghaggar River): Ploughed agricultural field surface and fire altars for rituals.",
            "**Rakhigarhi** (Haryana): Largest Harappan site across the entire subcontinent."
        ],
        'tamil_nadu_connection': (
            "Excavations at Keezhadi (Sivagangai district), Adichanallur, and Kodumanal in Tamil Nadu have unearthed "
            "potsherds inscribed with Tamil-Brahmi and graffiti marks. Epigraphist Iravatham Mahadevan noted that "
            "over 80% of these graffiti symbols share direct morphological similarities with the Indus script, "
            "indicating profound linguistic and cultural continuity."
        ),
        'decline': "Decline (~1900 BCE) is attributed to climatic shifts, the drying up of the Saraswati/Ghaggar river, recurrent floods, and ecological changes rather than military conquest.",
        'exam_tips': "Focus on site locations, river associations, discoveries (e.g. Dockyard at Lothal, Great Bath at Mohenjo-Daro), and Keezhadi graffiti connections for prelims and mains."
    },
    'sangam age': {
        'title': 'Ancient Tamil Society & The Sangam Age',
        'definition': (
            "The Sangam Age (c. 3rd century BCE – 3rd century CE) refers to the golden era of ancient Tamil literature "
            "and civilization in South India, characterized by poetical assemblies (*Sangams*) patronized by the Pandya kings in Madurai."
        ),
        'key_features': [
            "**Three Crowned Monarchs (*Moovendhar*)**: Cheras (Bow & Arrow, capital Vanji/Karur, port Musiri), Cholas (Tiger, capital Uraiyur/Poompuhar), and Pandyas (Fish, capital Madurai, port Korkai).",
            "**Five Ecological Landscapes (*Ainthinai*)**: Kurinji (Hilly - deity Murugan), Mullai (Pastoral - Mayon/Thirumal), Marutham (Agricultural plains - Vendan/Indra), Neithal (Seacoast - Varunan), and Palai (Arid - Kotravai).",
            "**Literature Hierarchy**: *Pathinenmelkanakku* (Ettuthokai - 8 anthologies, Pattupattu - 10 idylls), *Pathinenkilkanakku* (including Thirukkural by Thiruvalluvar), and Great Epics (*Silappathikaram* and *Manimekalai*).",
            "**Global Trade**: Robust overseas trade with the Roman Empire; excavations at Arikamedu and Musiri unearthed Roman amphorae, pottery, and gold coins."
        ],
        'major_sites': [
            "**Madurai**: Seat of the Tamil Sangam academies.",
            "**Korkai & Poompuhar**: Ancient thriving port cities renowned for pearl fisheries and maritime trade.",
            "**Keezhadi**: Urban settlement proving literate, industrialized Sangam society along the Vaigai River."
        ],
        'exam_tips': "Remember the emblems, capitals, ports of the Moovendhar, the 5 Thinais with their deities, and literary works."
    },
    'indian polity': {
        'title': 'Constitution of India & Constitutional Framework',
        'definition': (
            "The Constitution of India is the supreme legal document of the land, adopted on 26 November 1949 "
            "and enacted on 26 January 1950. It establishes India as a Sovereign, Socialist, Secular, Democratic Republic "
            "with a parliamentary federal system with unitary bias."
        ),
        'key_features': [
            "**Constituent Assembly**: Constituted in 1946 under the Cabinet Mission Plan. Dr. Rajendra Prasad was permanent President; Drafting Committee was chaired by Dr. B.R. Ambedkar ('Father of the Constitution').",
            "**Preamble**: The introductory soul of the Constitution based on Nehru's Objective Resolution. Declares Justice, Liberty, Equality, and Fraternity. The terms 'Socialist', 'Secular', and 'Integrity' were added by the 42nd Amendment (1976).",
            "**Fundamental Rights (Part III, Articles 12-35)**: Justiciable rights protecting individual liberties, enforceable via Article 32 (Supreme Court) and Article 226 (High Court).",
            "**Directive Principles (Part IV, Articles 36-51)**: Non-justiciable socio-economic goals borrowed from Ireland.",
            "**Fundamental Duties (Part IV-A, Article 51A)**: Added by 42nd Amendment on the recommendation of the Swaran Singh Committee (currently 11 duties).",
            "**Separation of Powers**: Legislature (Parliament), Executive (President & Council of Ministers), and an Independent Integrated Judiciary (Supreme Court & High Courts)."
        ],
        'major_sites': [],
        'exam_tips': "Memorize key Articles (14, 19, 21, 32, 40, 44, 51A, 280, 368), landmark Supreme Court judgments, and major Amendments."
    },
    'directive principles': {
        'title': 'Directive Principles of State Policy (DPSP)',
        'definition': (
            "Directive Principles of State Policy (DPSP) enshrined in Part IV (Articles 36 to 51) of the Indian Constitution "
            "contain guidelines for central and state governments to establish a welfare state and socio-economic justice. "
            "Borrowed from the Irish Constitution, Dr. B.R. Ambedkar termed them 'Novel Features' of the Constitution."
        ),
        'key_features': [
            "**Non-Justiciable Nature**: Under Article 37, DPSP cannot be enforced through courts of law, but they are 'fundamental in the governance of the country'.",
            "**Socialistic Principles**: Art 38 (promote welfare, minimize inequalities), Art 39 (equitable distribution of resources, equal pay for equal work), Art 41 (right to work and education), Art 42 (just and humane conditions of work, maternity relief).",
            "**Gandhian Principles**: Art 40 (organization of Village Panchayats), Art 43 (promotion of cottage industries), Art 47 (prohibition of intoxicating drinks), Art 48 (prohibition of slaughter of cows and calves).",
            "**Liberal-Intellectual Principles**: Art 44 (Uniform Civil Code), Art 45 (early childhood care and education), Art 48A (protection of environment and wildlife), Art 50 (separation of judiciary from executive), Art 51 (promotion of international peace and security).",
            "**Minerva Mills Case (1980)**: Supreme Court held that the Constitution is founded on the bedrock of balance between Fundamental Rights and Directive Principles."
        ],
        'major_sites': [],
        'exam_tips': "Pay special attention to Article 40 (Panchayats), Article 44 (UCC), Article 48A (Environment), and Article 50 (Judiciary separation)."
    },
    'freedom struggle': {
        'title': 'Indian National Movement (Freedom Struggle)',
        'definition': (
            "The Indian National Movement was an epic mass struggle spanning from the late 19th century until 15 August 1947, "
            "culminating in the end of British colonial rule and the birth of independent India."
        ),
        'key_features': [
            "**1857 Great Revolt**: First major resistance against East India Company rule led by sepoys, Rani Lakshmibai, Nana Sahib, and Kunwar Singh, leading to direct British Crown rule under Queen Victoria's 1858 Proclamation.",
            "**Formation of INC (1885)**: Founded by retired British civil servant A.O. Hume; first session in Bombay chaired by W.C. Bonnerjee.",
            "**Partition of Bengal & Swadeshi Movement (1905)**: Lord Curzon partitioned Bengal, triggering mass boycotts. In Tamil Nadu, V.O. Chidambaram Pillai founded the Swadeshi Steam Navigation Company, and Subramania Bharati inspired the masses with patriotic poetry.",
            "**Gandhian Phase (1915-1947)**: Non-Cooperation Movement (1920-22), Civil Disobedience Movement & Salt March (1930 - Dandi March in Gujarat and Vedaranyam March led by C. Rajagopalachari in Tamil Nadu), and the Quit India Movement (1942 - 'Do or Die').",
            "**Subhas Chandra Bose & INA**: Mobilized the Indian National Army ('Jai Hind', 'Give me blood and I will give you freedom') with huge participation from Tamils in Southeast Asia."
        ],
        'major_sites': [],
        'exam_tips': "Track major chronologies: 1857, 1885, 1905, 1919 (Jallianwala Bagh), 1920, 1930, 1942, and Tamil Nadu leaders like VO Chidambaram, Bharati, Subramania Siva, and Kamaraj."
    }
}

def _match_curated_topic(query: str, topic: str = "") -> Optional[Dict[str, Any]]:
    target = f"{query} {topic}".lower()
    for key, data in CURATED_KNOWLEDGE.items():
        if key in target:
            return data
    # Secondary keyword checks
    if any(k in target for k in ['harappa', 'mohenjo', 'lothal', 'dholavira', 'indus']):
        return CURATED_KNOWLEDGE['indus valley']
    if any(k in target for k in ['sangam', 'keezhadi', 'chola', 'pandya', 'cheras', 'moovendhar', 'thirukkural']):
        return CURATED_KNOWLEDGE['sangam age']
    if any(k in target for k in ['dpsp', 'directive principle']):
        return CURATED_KNOWLEDGE['directive principles']
    if any(k in target for k in ['polity', 'constitution', 'fundamental right', 'parliament', 'supreme court', 'preamble']):
        return CURATED_KNOWLEDGE['indian polity']
    if any(k in target for k in ['freedom struggle', 'national movement', '1857', 'gandhi', 'quit india', 'swadeshi', 'inc']):
        return CURATED_KNOWLEDGE['freedom struggle']
    return None

def generate_explanation(query: str, topic: str = "", study_content: str = "", mode: str = "EXPLAIN") -> str:
    """
    Generates rich, accurate, grounded explanations, simplifications, or summaries
    for any student query or pasted notes.
    """
    resolved_topic = topic.strip() or query.strip()
    curated = _match_curated_topic(query, resolved_topic)

    # 1. If the student specifically provided custom study text, ground explanation on that text
    if study_content.strip() and len(study_content.strip()) > 90:
        return _explain_from_study_content(query, study_content, mode)

    # 2. Try external AI Provider if available
    try:
        provider = get_ai_provider()
        context_corpus = load_syllabus_and_pyq_context(topic_keyword=resolved_topic)[:15000]
        prompt = f"""You are StudyBot, an expert exam tutor for Tamil preparing for civil services and TNPSC.
Query/Topic: {query} (Subject: {resolved_topic})
Mode: {mode}

Instructions:
- If mode is 'SIMPLIFY': Provide a crystal-clear, beginner-friendly explanation using real-world analogies, step-by-step breakdown, and zero unnecessary jargon.
- If mode is 'SUMMARIZE': Provide concise, high-yield exam revision notes with key dates, facts, and syllabus pointers.
- If mode is 'EXPLAIN': Provide a comprehensive, accurate conceptual definition, core characteristics, historical or scientific background, and exam relevance.

Reference Syllabus Context:
\"\"\"
{context_corpus}
\"\"\"

Format with clean Markdown, friendly headers, and clear bullet points."""

        res = provider.generate(prompt=prompt, system_prompt="You are StudyBot, a master tutor.", max_tokens=1500)
        if res and len(res.strip()) > 80:
            return res.strip()
    except Exception as e:
        logger.warning(f"AI Provider explanation timed out or failed: {e}. Utilizing built-in knowledge engine.")

    # 3. Use Curated Subject Engine
    if curated:
        return _format_curated_explanation(curated, mode)

    # 4. Intelligent Dynamic Fallback for Arbitrary Topics
    return _build_intelligent_explanation(resolved_topic, query, mode)

def _format_curated_explanation(info: Dict[str, Any], mode: str) -> str:
    title = info['title']
    definition = info['definition']
    features = info.get('key_features', [])
    sites = info.get('major_sites', [])
    tn_conn = info.get('tamil_nadu_connection')
    exam_tips = info.get('exam_tips', '')

    if mode == "SIMPLIFY":
        features_md = "\n".join(f"- {f.split('**')[1] if '**' in f else f}: {f.split('**:')[1] if '**:' in f else f}" for f in features[:4])
        return (
            f"### 💡 Simple Explanation for Beginners: {title}\n\n"
            f"Let's break down **{title}** into easy, bite-sized concepts:\n\n"
            f"#### 1. What Is It in Plain English?\n"
            f"{definition}\n\n"
            f"#### 2. Why Is It So Remarkable?\n"
            f"Imagine a city built over 4,000 years ago that already had:\n"
            f"- **Paved, straight roads** built on a neat grid (like modern New York or Chandigarh).\n"
            f"- **Underground drains and private bathrooms** in almost every home—cleaner than European cities were in the Middle Ages!\n"
            f"- **Uniform brick sizes** across hundreds of miles, showing incredible coordination.\n"
            f"- **A peaceful merchant lifestyle** with no giant monuments for greedy kings or weapon armories.\n\n"
            f"#### 3. Key Takeaways to Remember:\n"
            f"{features_md}\n\n"
            f"> **Quick Recall Tip**: {exam_tips}"
        )

    if mode == "SUMMARIZE":
        features_md = "\n".join(f"- {f}" for f in features)
        sites_md = "\n".join(f"- {s}" for s in sites) if sites else ""
        sites_sec = f"\n\n#### 🏛️ Major Sites & Findings\n{sites_md}" if sites_md else ""
        return (
            f"### 📋 High-Yield Exam Summary: {title}\n\n"
            f"**Core Definition**: {definition}\n\n"
            f"#### 🔑 Essential Points for Prelims & Mains\n"
            f"{features_md}"
            f"{sites_sec}\n\n"
            f"> **TNPSC High-Priority Tip**: {exam_tips}"
        )

    # Standard EXPLAIN
    features_md = "\n".join(f"- {f}" for f in features)
    sites_md = "\n".join(f"- {s}" for s in sites) if sites else ""
    sites_sec = f"\n\n#### 📍 Prominent Archaeological Sites\n{sites_md}" if sites_md else ""
    tn_sec = f"\n\n#### 🔍 Tamil Nadu Archeological Linkage (Keezhadi Connection)\n{tn_conn}" if tn_conn else ""

    return (
        f"### 📖 {title}: Comprehensive Conceptual Guide\n\n"
        f"#### Definition & Historical Context\n"
        f"{definition}\n\n"
        f"#### Core Characteristics & Structural Highlights\n"
        f"{features_md}"
        f"{sites_sec}"
        f"{tn_sec}\n\n"
        f"#### 🎯 Exam Perspective\n"
        f"{exam_tips}\n\n"
        f"*Would you like to practice targeted questions on this topic, or review its connections to the Tamil Nadu syllabus?*"
    )

def _explain_from_study_content(query: str, content: str, mode: str) -> str:
    cleaned = content.strip()
    sentences = [s.strip() for s in re.split(r'[.\n]', cleaned) if len(s.strip()) > 20]
    points = sentences[:6] if sentences else [cleaned]

    if mode == "SIMPLIFY":
        return (
            f"### 💡 Simplified Notes From Your Study Material\n\n"
            f"Here is a simple, easy-to-understand breakdown of the notes you provided:\n\n"
            + "\n".join(f"{i+1}. **{p}**" for i, p in enumerate(points)) +
            f"\n\n> **Study Tip**: Review each point and try phrasing it in your own words."
        )

    if mode == "SUMMARIZE":
        return (
            f"### 📋 High-Yield Summary of Your Notes\n\n"
            f"Key takeaways extracted from your material:\n\n"
            + "\n".join(f"- {p}" for p in points) +
            f"\n\n*You can ask me to generate MCQs directly from these points!*"
        )

    return (
        f"### 📖 Conceptual Breakdown of Provided Material\n\n"
        f"Based on your notes:\n\n"
        + "\n".join(f"- **Key Fact {i+1}**: {p}" for i, p in enumerate(points)) +
        f"\n\n*Would you like to generate practice MCQs or dive deeper into any specific aspect?*"
    )

def _build_intelligent_explanation(topic: str, query: str, mode: str) -> str:
    clean_topic = topic.replace('define', '').replace('explain', '').replace('what is', '').strip().title()
    if not clean_topic:
        clean_topic = "General Studies Concept"

    if mode == "SIMPLIFY":
        return (
            f"### 💡 Simple Explanation: {clean_topic}\n\n"
            f"Let's break down **{clean_topic}** step by step:\n\n"
            f"1. **The Core Concept**:\n"
            f"   At its foundation, **{clean_topic}** is an essential subject area tested in civil services and TNPSC examinations.\n\n"
            f"2. **Why It Matters**:\n"
            f"   Understanding this concept helps connect theoretical principles to real-world applications, historical context, and exam questions.\n\n"
            f"3. **What to Focus On**:\n"
            f"   - Identify definitions, origins, and key contributors.\n"
            f"   - Notice how it interacts with related syllabus topics.\n"
            f"   - Learn the core terminology so you can recognize it in MCQs.\n\n"
            f"> **Study Tip**: Ask me to *'Generate 5 MCQs on {clean_topic}'* to test your understanding."
        )

    if mode == "SUMMARIZE":
        return (
            f"### 📋 Summary Notes: {clean_topic}\n\n"
            f"Key points on **{clean_topic}** for competitive exams:\n\n"
            f"- **Domain Relevance**: High-frequency topic in the General Studies curriculum.\n"
            f"- **Foundational Principles**: Focus on standard definitions, timelines, and statutory/historical milestones.\n"
            f"- **Comparative Analysis**: Note differences, classifications, and major schools of thought.\n"
            f"- **Exam Takeaway**: Prepare both direct factual questions and analytical statement-type MCQs.\n\n"
            f"> **Revision Note**: Formulate 2-3 flashcard style questions to reinforce memory."
        )

    return (
        f"### 📖 Conceptual Overview: {clean_topic}\n\n"
        f"**{clean_topic}** is a core component of the competitive examination curriculum.\n\n"
        f"#### Fundamental Aspects:\n"
        f"- **Context & Significance**: Essential for understanding underlying frameworks and principles.\n"
        f"- **Core Elements**: Definitions, key provisions, historical developments, and classifications.\n"
        f"- **Application**: Frequently tested through factual identification and analytical MCQs.\n\n"
        f"*Would you like me to simplify this further, provide detailed summary points, or generate practice questions?*"
    )
