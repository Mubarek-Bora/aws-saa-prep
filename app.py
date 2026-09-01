import json
import math
from pathlib import Path

import streamlit as st

from curriculum import WEEKS, DOMAIN_COLORS

PROGRESS_FILE = Path(__file__).parent / "progress.json"

DOMAIN_ICONS = {
    "Foundations": "🧭",
    "Security": "🔒",
    "Resilience": "🛡️",
    "Cost": "💰",
    "Exam prep": "🎯",
}

st.set_page_config(page_title="AWS SAA-C03 Prep", page_icon="📚", layout="wide")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp, .stApp * {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}
.stApp {
    background:
        radial-gradient(1200px 600px at 8% -10%, rgba(255,153,0,0.08), transparent 55%),
        radial-gradient(1000px 500px at 100% 0%, rgba(37,99,235,0.06), transparent 55%);
}

.week-card {
    border-radius: 16px;
    padding: 18px 20px;
    margin-bottom: 14px;
    background: rgba(127,127,127,0.06);
    border: 1px solid rgba(127,127,127,0.12);
    border-left: 5px solid var(--card-color, #FF9900);
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.week-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(0,0,0,0.12);
}
.week-card .wc-title { font-size: 1.05rem; font-weight: 700; margin-bottom: 2px; }
.week-card .wc-sub { opacity: 0.7; font-size: 0.85rem; margin-bottom: 10px; }

.domain-badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 999px;
    color: white;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.02em;
    text-transform: uppercase;
    box-shadow: 0 1px 3px rgba(0,0,0,0.15);
}

.hero-banner {
    border-radius: 18px;
    padding: 26px 30px;
    margin-bottom: 20px;
    background: linear-gradient(135deg, var(--hero-color, #FF9900) 0%, rgba(0,0,0,0.18) 100%);
    box-shadow: 0 8px 28px rgba(0,0,0,0.16);
}
.hero-banner .hb-week { font-size: 0.85rem; font-weight: 700; color: white; opacity: 0.9; text-transform: uppercase; letter-spacing: 0.06em; }
.hero-banner .hb-title { font-size: 1.9rem; font-weight: 800; color: white; margin: 6px 0 10px 0; }
.hero-banner .hb-intro { color: white; opacity: 0.96; font-size: 0.97rem; line-height: 1.5; }

.topic-card {
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 12px;
    background: rgba(127,127,127,0.06);
    border: 1px solid rgba(127,127,127,0.1);
    border-left: 4px solid var(--card-color, #FF9900);
    transition: box-shadow 0.15s ease;
}
.topic-card:hover { box-shadow: 0 6px 16px rgba(0,0,0,0.08); }
.topic-card .tc-name { font-weight: 700; margin-bottom: 6px; }

.score-pill {
    display: inline-block;
    padding: 1px 10px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
    color: white;
}

[data-testid="stMetric"] {
    background: rgba(127,127,127,0.06);
    border: 1px solid rgba(127,127,127,0.12);
    border-radius: 14px;
    padding: 14px 18px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
[data-testid="stMetricValue"] { font-weight: 800; }

.stButton button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: transform 0.12s ease, box-shadow 0.12s ease !important;
}
.stButton button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 14px rgba(0,0,0,0.14);
}

.progress-ring-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    padding: 10px 0 4px 0;
}
.progress-ring-svg { display: block; }
.progress-ring-label {
    margin-top: 6px;
    font-size: 0.8rem;
    font-weight: 600;
    opacity: 0.7;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text())
    return {}


def save_progress(progress: dict) -> None:
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2))


def week_progress(progress: dict, week_num: int) -> dict:
    return progress.setdefault(str(week_num), {"hands_on": [], "best_score": None})


def score_color(pct: int) -> str:
    if pct >= 80:
        return "#059669"
    if pct >= 50:
        return "#d97706"
    return "#dc2626"


def domain_badge(domain: str, color: str) -> str:
    icon = DOMAIN_ICONS.get(domain, "📦")
    return f'<span class="domain-badge" style="background:{color}">{icon} {domain}</span>'


def progress_ring_html(pct: int, color: str, size: int = 132, stroke: int = 12) -> str:
    r = (size - stroke) / 2
    c = 2 * math.pi * r
    offset = c * (1 - pct / 100)
    center = size / 2
    return f"""
    <div class="progress-ring-wrap">
        <div style="position:relative; width:{size}px; height:{size}px;">
            <svg class="progress-ring-svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}"
                 style="transform:rotate(-90deg);">
                <circle cx="{center}" cy="{center}" r="{r}" fill="none"
                        stroke="rgba(127,127,127,0.18)" stroke-width="{stroke}"/>
                <circle cx="{center}" cy="{center}" r="{r}" fill="none"
                        stroke="{color}" stroke-width="{stroke}" stroke-linecap="round"
                        stroke-dasharray="{c:.2f}" stroke-dashoffset="{offset:.2f}"/>
            </svg>
            <div style="position:absolute; inset:0; display:flex; align-items:center; justify-content:center;
                        font-size:1.4rem; font-weight:800;">{pct}%</div>
        </div>
        <div class="progress-ring-label">Overall progress</div>
    </div>
    """


if "progress" not in st.session_state:
    st.session_state.progress = load_progress()

progress = st.session_state.progress

# ---------- sidebar ----------
st.sidebar.title("📚 AWS SAA-C03 Prep")
st.sidebar.caption("16-week plan · 3-5 hrs/week")

total_hands_on_tasks = sum(len(w["hands_on"]) for w in WEEKS)
done_hands_on_tasks = sum(len(progress.get(str(w["num"]), {}).get("hands_on", [])) for w in WEEKS)
overall_pct = done_hands_on_tasks / total_hands_on_tasks if total_hands_on_tasks else 0
st.sidebar.progress(overall_pct, text=f"Hands-on progress: {done_hands_on_tasks}/{total_hands_on_tasks}")

nav_options = ["🏠 Overview"] + [f"Week {w['num']}: {w['title']}" for w in WEEKS]
for w in WEEKS:
    wp = progress.get(str(w["num"]), {})
    done = len(wp.get("hands_on", [])) == len(w["hands_on"]) and len(w["hands_on"]) > 0
    if done:
        idx = nav_options.index(f"Week {w['num']}: {w['title']}")
        nav_options[idx] += " ✅"

if "nav_choice" not in st.session_state:
    st.session_state.nav_choice = nav_options[0]
elif st.session_state.nav_choice not in nav_options:
    # label may have gained/lost a checkmark since last run — match by prefix
    prefix = st.session_state.nav_choice.split(" ✅")[0]
    matches = [o for o in nav_options if o.startswith(prefix)]
    st.session_state.nav_choice = matches[0] if matches else nav_options[0]

selected_label = st.sidebar.radio("Navigate", nav_options, key="nav_choice", label_visibility="collapsed")


def go_to(label: str):
    st.session_state.nav_choice = label


# ---------- overview page ----------
if selected_label == "🏠 Overview":
    st.title("📚 AWS SAA-C03 Prep")
    st.caption("Your 16-week roadmap to the Solutions Architect Associate exam.")

    weeks_done = sum(
        1 for w in WEEKS
        if len(progress.get(str(w["num"]), {}).get("hands_on", [])) == len(w["hands_on"]) and w["hands_on"]
    )
    scores = [progress.get(str(w["num"]), {}).get("best_score") for w in WEEKS]
    scores = [s for s in scores if s is not None]
    avg_score = round(sum(scores) / len(scores)) if scores else None

    ring_col, m1, m2, m3, m4 = st.columns([1, 1, 1, 1, 1])
    with ring_col:
        st.markdown(progress_ring_html(round(overall_pct * 100), "#FF9900"), unsafe_allow_html=True)
    m1.metric("Weeks fully done", f"{weeks_done}/16")
    m2.metric("Hands-on tasks", f"{done_hands_on_tasks}/{total_hands_on_tasks}")
    m3.metric("Quizzes taken", f"{len(scores)}/16")
    m4.metric("Average best score", f"{avg_score}%" if avg_score is not None else "—")

    st.divider()

    cols = st.columns(4)
    for i, w in enumerate(WEEKS):
        color = DOMAIN_COLORS.get(w["domain"], "#6b7280")
        wp = progress.get(str(w["num"]), {})
        hdone = len(wp.get("hands_on", []))
        htotal = len(w["hands_on"])
        best = wp.get("best_score")
        score_html = (
            f'<span class="score-pill" style="background:{score_color(best)}">{best}%</span>'
            if best is not None else '<span style="opacity:0.5;font-size:0.8rem;">no quiz yet</span>'
        )
        with cols[i % 4]:
            st.markdown(
                f'<div class="week-card" style="--card-color:{color}">'
                f'{domain_badge(w["domain"], color)}'
                f'<div class="wc-title">Week {w["num"]}: {w["title"]}</div>'
                f'<div class="wc-sub">Hands-on: {hdone}/{htotal} &nbsp;·&nbsp; {score_html}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.button(
                "Open →",
                key=f"open_{w['num']}",
                on_click=go_to,
                args=(f"Week {w['num']}: {w['title']}",),
                use_container_width=True,
            )

    st.stop()

# ---------- week page ----------
week_num = int(selected_label.split(":")[0].replace("Week", "").strip())
selected_week = next(w for w in WEEKS if w["num"] == week_num)

domain = selected_week["domain"]
color = DOMAIN_COLORS.get(domain, "#6b7280")

st.sidebar.markdown(domain_badge(domain, color) + " domain", unsafe_allow_html=True)

st.markdown(
    f'<div class="hero-banner" style="--hero-color:{color}">'
    f'<div class="hb-week">Week {selected_week["num"]} of 16</div>'
    f'<div class="hb-title">{selected_week["title"]}</div>'
    f'<div class="hb-intro">{selected_week["intro"]}</div>'
    f'</div>',
    unsafe_allow_html=True,
)

tab_learn, tab_hands_on, tab_quiz = st.tabs(["📖 Learn", "🛠 Hands-On", "📝 Quiz"])

with tab_learn:
    for name, explanation in selected_week["topics"]:
        st.markdown(
            f'<div class="topic-card" style="--card-color:{color}">'
            f'<div class="tc-name">📌 {name}</div>'
            f'<div>{explanation}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

with tab_hands_on:
    wp = week_progress(progress, selected_week["num"])
    done_set = set(wp["hands_on"])
    week_pct = len(done_set) / len(selected_week["hands_on"]) if selected_week["hands_on"] else 0
    st.progress(week_pct, text=f"{len(done_set)}/{len(selected_week['hands_on'])} tasks done")
    st.caption("Check off each task as you complete it in the AWS console yourself.")

    changed = False
    for i, task in enumerate(selected_week["hands_on"]):
        checked = st.checkbox(task, value=i in done_set, key=f"hands_on_{selected_week['num']}_{i}")
        if checked and i not in done_set:
            wp["hands_on"].append(i)
            changed = True
        elif not checked and i in done_set:
            wp["hands_on"].remove(i)
            changed = True
    if changed:
        save_progress(progress)
    if len(wp["hands_on"]) == len(selected_week["hands_on"]) and selected_week["hands_on"]:
        st.success("All hands-on tasks for this week are done. 🎉")

with tab_quiz:
    quiz = selected_week["quiz"]
    quiz_key = f"quiz_submitted_{selected_week['num']}"
    if quiz_key not in st.session_state:
        st.session_state[quiz_key] = False

    answers = []
    for i, q in enumerate(quiz):
        with st.container(border=True):
            st.markdown(f"**Q{i + 1}. {q['q']}**")
            choice = st.radio(
                "Choose one",
                q["options"],
                index=None,
                key=f"quiz_{selected_week['num']}_{i}",
                label_visibility="collapsed",
            )
            answers.append(choice)

    if st.button("Submit Quiz", key=f"submit_{selected_week['num']}", type="primary"):
        st.session_state[quiz_key] = True

    if st.session_state[quiz_key]:
        score = 0
        for i, q in enumerate(quiz):
            correct_option = q["options"][q["answer"]]
            is_correct = answers[i] == correct_option
            if is_correct:
                score += 1
            icon = "✅" if is_correct else "❌"
            st.markdown(f"{icon} **Q{i + 1}:** correct answer is *{correct_option}*")
            st.caption(q["explanation"])

        pct = round(100 * score / len(quiz))
        wp = week_progress(progress, selected_week["num"])
        if wp["best_score"] is None or pct > wp["best_score"]:
            wp["best_score"] = pct
            save_progress(progress)

        sc = score_color(pct)
        st.markdown(
            f'<div class="hero-banner" style="--hero-color:{sc}; text-align:center;">'
            f'<div class="hb-title" style="margin:0;">Score: {score}/{len(quiz)} ({pct}%)</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

st.sidebar.divider()
st.sidebar.subheader("Best quiz scores")
for w in WEEKS:
    best = progress.get(str(w["num"]), {}).get("best_score")
    if best is not None:
        st.sidebar.markdown(
            f'Week {w["num"]}: <span class="score-pill" style="background:{score_color(best)}">{best}%</span>',
            unsafe_allow_html=True,
        )
    else:
        st.sidebar.write(f"Week {w['num']}: —")
