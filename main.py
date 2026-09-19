import gradio as gr
import spaces


@spaces.GPU(duration=1)
def zerogpu_startup():
    return None

# ============================================================
# RECOMMENDATION DATA
# ============================================================

content = [
    {
        "title": "The Matrix",
        "type": "movie",
        "categories": ["movies", "ai", "sci-fi"],
        "rating": 8.7
    },
    {
        "title": "Python for Data Science",
        "type": "course",
        "categories": ["python", "data-science"],
        "rating": 9.2
    },
    {
        "title": "Inception",
        "type": "movie",
        "categories": ["movies", "sci-fi"],
        "rating": 8.8
    },
    {
        "title": "Learn Python Basics",
        "type": "course",
        "categories": ["python", "programming"],
        "rating": 8.9
    },
    {
        "title": "AI and Machine Learning",
        "type": "course",
        "categories": ["ai", "python", "data-science"],
        "rating": 9.0
    },
    {
        "title": "Gaming PC Guide",
        "type": "article",
        "categories": ["gaming", "tech"],
        "rating": 8.5
    },
    {
        "title": "FIFA 2024",
        "type": "game",
        "categories": ["gaming", "sports"],
        "rating": 8.6
    },
    {
        "title": "Top 10 Sports Documentaries",
        "type": "documentary",
        "categories": ["sports", "movies"],
        "rating": 8.4
    },
    {
        "title": "Music Production Basics",
        "type": "course",
        "categories": ["music", "creative"],
        "rating": 8.7
    },
    {
        "title": "Web Development with JavaScript",
        "type": "course",
        "categories": ["programming", "web-development"],
        "rating": 9.1
    }
]


# ============================================================
# RECOMMENDATION FUNCTION
# ============================================================

def get_recommendations(selected_interests, custom_interest):

    if not selected_interests:
        selected_interests = []

    if custom_interest:
        custom_interest = custom_interest.strip().lower()

        if custom_interest:
            selected_interests.append(custom_interest)

    if not selected_interests:
        return """
        <div class="message-box warning">

            <div class="message-icon">⚠️</div>

            <div>
                <h3>Select an interest</h3>

                <p>
                    Please select at least one interest
                    to get recommendations.
                </p>
            </div>

        </div>
        """

    results = []

    for item in content:

        categories = [
            category.lower()
            for category in item["categories"]
        ]

        matches = sum(
            1
            for interest in selected_interests
            if interest.lower() in categories
        )

        score = matches * item["rating"]

        if score > 0:

            results.append(
                (
                    item["title"],
                    item["type"],
                    item["categories"],
                    item["rating"],
                    round(score, 1)
                )
            )

    if not results:
        return """
        <div class="message-box">

            <div class="message-icon">🔎</div>

            <div>

                <h3>No recommendations found</h3>

                <p>
                    Try selecting different interests
                    or adding another interest.
                </p>

            </div>

        </div>
        """

    results.sort(
        key=lambda x: x[4],
        reverse=True
    )

    cards = ""

    for index, (
        title,
        type_,
        categories,
        rating,
        score
    ) in enumerate(results, 1):

        category_html = ""

        for category in categories:

            category_html += f"""
            <span class="tag">
                {category}
            </span>
            """

        cards += f"""
        <div class="recommendation-card">

            <div class="rank">
                #{index}
            </div>

            <div class="recommendation-content">

                <div class="title-row">

                    <h3>
                        {title}
                    </h3>

                    <span class="type-badge">
                        {type_}
                    </span>

                </div>

                <div class="tags">

                    {category_html}

                </div>

                <div class="card-bottom">

                    <div class="rating">

                        ⭐

                        <strong>
                            {rating}
                        </strong>

                        <span>
                            rating
                        </span>

                    </div>

                    <div class="match">

                        <span>
                            Match
                        </span>

                        <strong>
                            {score}
                        </strong>

                    </div>

                </div>

            </div>

        </div>
        """

    return f"""
    <div class="results-header">

        <div>

            <p class="small-label">
                PERSONALIZED FOR YOU
            </p>

            <h2>
                ✨ Your Recommendations
            </h2>

        </div>

        <div class="result-count">
            {len(results)} found
        </div>

    </div>

    <div class="recommendations">

        {cards}

    </div>
    """


# ============================================================
# CUSTOM CSS
# ============================================================

css = """

/* =========================
   GLOBAL
   ========================= */

body {
    background: #0b0f14 !important;
}

.gradio-container {
    max-width: 1180px !important;
    margin: auto !important;
    padding: 25px 20px 40px !important;
}


/* =========================
   HERO
   ========================= */

.hero {
    text-align: center;
    padding: 45px 25px 38px;
    margin-bottom: 25px;
}

.hero-icon {
    width: 64px;
    height: 64px;

    margin: 0 auto 18px;

    border-radius: 18px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: #171d26;

    border: 1px solid #2a3340;

    font-size: 30px;
}

.hero h1 {
    font-size: 42px !important;

    font-weight: 700 !important;

    letter-spacing: -1.5px;

    margin: 0 0 12px !important;
}

.hero p {
    max-width: 650px;

    margin: auto;

    font-size: 16px;

    line-height: 1.7;

    color: #9ca6b5;
}


/* =========================
   INPUT CARD
   ========================= */

.input-card {
    background: #11161d !important;

    border: 1px solid #232c37 !important;

    border-radius: 18px !important;

    padding: 25px !important;

    margin-bottom: 22px;
}

.section-title {
    margin-bottom: 20px;
}

.section-title h2 {
    margin: 0 0 5px;

    font-size: 21px;
}

.section-title p {
    margin: 0;

    color: #8993a2;

    font-size: 14px;
}


/* =========================
   CUSTOM INPUT
   ========================= */

.custom-box {
    background: #0d1218 !important;

    border: 1px solid #27313d !important;

    border-radius: 12px !important;
}


/* =========================
   BUTTON
   ========================= */

#recommend-button {

    width: 100%;

    min-height: 52px;

    margin-top: 20px;

    border-radius: 11px !important;

    font-size: 16px !important;

    font-weight: 600 !important;
}


/* =========================
   RESULTS CARD
   ========================= */

.results-card {

    background: #11161d !important;

    border: 1px solid #232c37 !important;

    border-radius: 18px !important;

    padding: 25px !important;
}

.results-header {

    display: flex;

    justify-content: space-between;

    align-items: center;

    margin-bottom: 20px;
}

.results-header h2 {

    margin: 0;

    font-size: 24px;
}

.small-label {

    color: #7f8b9b;

    font-size: 11px;

    letter-spacing: 1.5px;

    font-weight: 600;

    margin: 0 0 5px;
}

.result-count {

    background: #1a222d;

    border: 1px solid #2b3542;

    padding: 7px 12px;

    border-radius: 20px;

    font-size: 13px;

    color: #aeb7c4;
}


/* =========================
   RECOMMENDATION CARD
   ========================= */

.recommendation-card {

    display: flex;

    background: #0d1218;

    border: 1px solid #232d38;

    border-radius: 14px;

    margin-bottom: 12px;

    overflow: hidden;

    transition: 0.2s ease;
}

.recommendation-card:hover {

    border-color: #3b4654;

    transform: translateY(-2px);
}

.rank {

    min-width: 58px;

    display: flex;

    align-items: center;

    justify-content: center;

    background: #151c25;

    color: #8995a5;

    font-size: 14px;

    font-weight: 600;
}

.recommendation-content {

    width: 100%;

    padding: 18px 20px;
}

.title-row {

    display: flex;

    align-items: center;

    justify-content: space-between;

    gap: 15px;
}

.title-row h3 {

    margin: 0;

    font-size: 17px;

    font-weight: 600;
}

.type-badge {

    background: #19212b;

    border: 1px solid #2b3542;

    padding: 4px 9px;

    border-radius: 6px;

    color: #9da8b7;

    font-size: 11px;

    text-transform: uppercase;
}


/* =========================
   TAGS
   ========================= */

.tags {

    display: flex;

    flex-wrap: wrap;

    gap: 6px;

    margin-top: 12px;
}

.tag {

    padding: 4px 8px;

    background: #161e27;

    border: 1px solid #27313c;

    border-radius: 5px;

    color: #8e99a8;

    font-size: 11px;
}


/* =========================
   CARD BOTTOM
   ========================= */

.card-bottom {

    display: flex;

    align-items: center;

    gap: 25px;

    margin-top: 15px;
}

.rating,
.match {

    display: flex;

    align-items: center;

    gap: 5px;

    font-size: 13px;
}

.rating span,
.match span {

    color: #707b8a;

    font-size: 11px;
}

.match {

    margin-left: auto;
}

.match strong {

    color: #d7dde6;
}


/* =========================
   MESSAGE
   ========================= */

.message-box {

    display: flex;

    align-items: center;

    gap: 15px;

    padding: 22px;

    background: #0d1218;

    border: 1px solid #28313d;

    border-radius: 12px;
}

.message-box.warning {

    border-color: #4a4027;
}

.message-icon {

    font-size: 25px;
}

.message-box h3 {

    margin: 0 0 4px;
}

.message-box p {

    margin: 0;

    color: #8993a2;
}


/* =========================
   FOOTER
   ========================= */

.footer {

    text-align: center;

    margin-top: 25px;

    color: #596474;

    font-size: 12px;
}


/* =========================
   MOBILE
   ========================= */

@media (max-width: 700px) {

    .gradio-container {

        padding: 15px !important;
    }

    .hero {

        padding: 30px 15px;
    }

    .hero h1 {

        font-size: 30px !important;
    }

    .results-header {

        align-items: flex-start;

        gap: 10px;
    }

    .title-row {

        align-items: flex-start;

        flex-direction: column;

        gap: 8px;
    }

    .match {

        margin-left: 0;
    }

}
"""


# ============================================================
# GRADIO APP
# ============================================================

with gr.Blocks(
    title="AI Recommendation System",

    theme=gr.themes.Base(
        primary_hue="blue",
        neutral_hue="slate"
    ),

    css=css

) as demo:


    # =========================
    # HERO
    # =========================

    gr.HTML(
        """
        <div class="hero">

            <div class="hero-icon">
                🎯
            </div>

            <h1>
                AI Recommendation System
            </h1>

            <p>
                Tell us what you're interested in and discover
                movies, courses, games, articles and more.
            </p>

        </div>
        """
    )


    # =========================
    # INPUT SECTION
    # =========================

    with gr.Group(
        elem_classes="input-card"
    ):

        gr.HTML(
            """
            <div class="section-title">

                <h2>
                    📌 Choose your interests
                </h2>

                <p>
                    Select the topics you enjoy the most.
                </p>

            </div>
            """
        )


        with gr.Row():

            with gr.Column(
                scale=2
            ):

                interests = gr.CheckboxGroup(

                    choices=[
                        "python",
                        "movies",
                        "ai",
                        "data-science",
                        "programming",
                        "gaming",
                        "sports",
                        "music",
                        "tech",
                        "creative",
                        "web-development"
                    ],

                    label="Interests",

                    info="Select one or more"

                )


            with gr.Column(
                scale=1
            ):

                custom = gr.Textbox(

                    label="Custom Interest",

                    placeholder="e.g. cooking, photography...",

                    info="Optional",

                    elem_classes="custom-box"

                )


        btn = gr.Button(

            "🔍 Find My Recommendations",

            variant="primary",

            elem_id="recommend-button"

        )


    # =========================
    # RESULTS
    # =========================

    with gr.Group(
        elem_classes="results-card"
    ):

        output = gr.HTML(

            """
            <div class="message-box">

                <div class="message-icon">
                    💡
                </div>

                <div>

                    <h3>
                        Your recommendations will appear here
                    </h3>

                    <p>
                        Choose your interests above and click
                        "Find My Recommendations".
                    </p>

                </div>

            </div>
            """

        )


    # =========================
    # BUTTON EVENT
    # =========================

    btn.click(

        fn=get_recommendations,

        inputs=[
            interests,
            custom
        ],

        outputs=output

    )


    # =========================
    # FOOTER
    # =========================

    gr.HTML(

        """
        <div class="footer">
            Built with Python & Gradio
        </div>
        """

    )


# ============================================================
# LAUNCH
# ============================================================

if __name__ == "__main__":

    demo.launch()
    