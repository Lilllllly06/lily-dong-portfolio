import datetime
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request
from peewee import *
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)
mydb = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306,
)


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


mydb.connect(reuse_if_open=True)
mydb.create_tables([TimelinePost])
mydb.close()


NAV_ITEMS = [
    {"label": "Home", "endpoint": "index"},
    {"label": "About", "endpoint": "index", "fragment": "about"},
    {"label": "Experience", "endpoint": "index", "fragment": "experience"},
    {"label": "Projects", "endpoint": "index", "fragment": "projects"},
    {"label": "Places", "endpoint": "index", "fragment": "places"},
    {"label": "Hobbies", "endpoint": "hobbies"},
]

SKILLS = [
    "Python",
    "TypeScript",
    "React",
    "Flask",
    "FastAPI",
    "PyTorch",
    "LLM APIs",
    "Ruby on Rails",
    "PostgreSQL",
    "Docker",
]

EXPERIENCES = [
    {
        "role": "Software Engineering Intern",
        "company": "Shopify",
        "period": "May 2026 - Aug 2026",
        "tools": "Python, TypeScript, React Native, Ruby on Rails, RAG, LLM, OAuth, BLE",
        "summary": (
            "Contributed to agentic developer tooling infrastructure, including RAG-based "
            "context retrieval and prompt orchestration that improved the relevance "
            "of context sent to LLM workflows."
        ),
    },
    {
        "role": "Software Engineering Intern",
        "company": "Shopify",
        "period": "Sep 2025 - Dec 2025",
        "tools": "React, TypeScript, Ruby on Rails, GraphQL",
        "summary": (
            "Built full-stack retail admin features, including staff assignment "
            "workflows with GraphQL pagination and cross-system data contracts."
        ),
    },
    {
        "role": "Web Developer Co-op",
        "company": "AGF Investments",
        "period": "Jan 2025 - Apr 2025",
        "tools": "Java, Spring Boot, Maven, Apache POI, Git",
        "summary": (
            "Developed a Spring Boot ScoreCard application that automated XLSX "
            "report generation for internal teams and reduced manual spreadsheet work."
        ),
    },
]

EDUCATION = [
    {
        "school": "University of Waterloo",
        "program": "BASc in Computer Engineering",
        "period": "Expected graduation: May 2028",
        "location": "Waterloo, ON",
        "notes": (
            "Second-year computer engineering student interested in full-stack systems, "
            "model tooling, and products that make technical work feel more usable."
        ),
    }
]

PROJECTS = [
    {
        "name": "Multimodal Agent Evaluation Sandbox",
        "stack": "Python, PyTorch, Gemini API, FastAPI, React, PostgreSQL, Docker",
        "summary": (
            "A benchmark environment for evaluating software agents across text, image, "
            "code, and tabular reasoning tasks."
        ),
    },
    {
        "name": "Merchant Inventory Assistant",
        "stack": "Python, TypeScript, LLM APIs, scikit-learn, React, Node/Express",
        "summary": (
            "An LLM-powered inventory assistant that routes merchant questions into "
            "structured workflow tools and database queries."
        ),
    },
    {
        "name": "3D Data Sandbox",
        "stack": "Electron, Node.js, Three.js, PapaParse",
        "summary": (
            "A desktop app for offline 3D visualization of CSV and JSON datasets, "
            "with clustering, outlier detection, and interactive highlighting."
        ),
    },
]

HOBBIES = [
    {
        "name": "Workout Reset",
        "image": "img/hobby-workout.png",
        "summary": (
            "I like workouts that feel sustainable: strength training, a good playlist, "
            "and enough movement to clear my head without pretending I am training for the Olympics."
        ),
    },
    {
        "name": "Crochet Projects",
        "image": "img/hobby-crochet.png",
        "summary": (
            "Crochet is my favorite kind of slow problem-solving. I like choosing colors, "
            "building stitch by stitch, and ending up with something soft and useful."
        ),
    },
    {
        "name": "Weekend Baking",
        "image": "img/hobby-baking.png",
        "summary": (
            "Baking is where I get to be precise and cozy at the same time. Cookies, cakes, "
            "and small treats are my favorite excuse to share something warm."
        ),
    },
]

PLACES = [
    {
        "name": "Orlando, Florida",
        "detail": "Theme parks, sunshine, and one very memorable Disney trip.",
    },
    {
        "name": "Romania",
        "detail": "A physics tournament trip with historical streets and competition memories.",
    },
    {
        "name": "Beijing, China",
        "detail": "Traditional food, local flavors, and landmarks with a lot of history.",
    },
    {
        "name": "Shanghai, China",
        "detail": "Bund views, city lights, and a magical Shanghai Disney day.",
    },
    {
        "name": "Hong Kong, China",
        "detail": "Disneyland, dense city views, and excellent food around every corner.",
    },
    {
        "name": "Suzhou, China",
        "detail": "Classical gardens, canals, and quiet old streets.",
    },
]


@app.context_processor
def inject_navigation():
    return {"nav_items": NAV_ITEMS}


@app.before_request
def before_request():
    mydb.connect(reuse_if_open=True)


@app.after_request
def after_request(response):
    if not mydb.is_closed():
        mydb.close()
    return response


@app.route("/")
def index():
    return render_template(
        "index.html",
        title="Portfolio",
        url=os.getenv("URL"),
        skills=SKILLS,
        experiences=EXPERIENCES,
        education=EDUCATION,
        projects=PROJECTS,
        hobbies=HOBBIES,
        places=PLACES,
    )


@app.route("/hobbies")
def hobbies():
    return render_template(
        "hobbies.html",
        title="Hobbies",
        url=os.getenv("URL"),
        hobbies=HOBBIES,
    )


@app.route("/api/timeline_post", methods=["POST"])
def post_timeline_post():
    data = request.get_json(silent=True) or request.form
    required_fields = ("name", "email", "content")
    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields:
        return {"error": f"Missing required fields: {', '.join(missing_fields)}"}, 400

    timeline_post = TimelinePost.create(
        name=data.get("name"),
        email=data.get("email"),
        content=data.get("content"),
    )

    return model_to_dict(timeline_post), 201


@app.route("/api/timeline_post", methods=["GET"])
def get_timeline_posts():
    timeline_posts = [
        model_to_dict(post)
        for post in TimelinePost.select().order_by(TimelinePost.created_at.desc())
    ]

    return {"timeline_posts": timeline_posts}


@app.route("/api/timeline_post/<int:post_id>", methods=["DELETE"])
def delete_timeline_post(post_id):
    deleted_count = TimelinePost.delete_by_id(post_id)

    if deleted_count == 0:
        return {"error": "Timeline post not found"}, 404

    return {"deleted": post_id}
