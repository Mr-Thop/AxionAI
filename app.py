from flask import Flask , request , jsonify
from flask_cors import CORS
import logging
from Models import Model
from Parser import Parser
from DB import DB
from Embedder import Embed
from Scheduler import Schedule
from Evaluator import InterviewEvaluator
from dotenv import load_dotenv
import json
import os


load_dotenv()
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

model_4b = os.getenv("4b")
model_27b = os.getenv("27b")
db = DB()

embedder = Embed()
embedder.create_db(db.string,db.collection)
logging.info("Embedder Loaded Successfully")

evaluator = InterviewEvaluator(model_4b)
logging.info("Evaluator Loaded Successfully")

PROMPT = os.getenv("Prompt")
JD_Prompt = os.getenv("JD_Prompt")
Summary = os.getenv("Summary_Prompt")
parser = Parser()


@app.route("/",methods = ["GET","POST"])
def default_route():
    return jsonify({
        "output" : "Backend Running Successfully"
    })

@app.route("/parse",methods = ["POST"])
def parse():
    db.connect_PS()
    logging.info("Database Connected Successfully")

    
    structure_model = Model(PROMPT,model_27b)
    logging.info("Model Loaded Successfully")
    
    logging.info("Parsing Resumes")
    

    files = os.listdir("./resume")
    contents = []
    documents = []
    for file_path in files:
        if file_path.endswith(".pdf"):
            path = r"./resume/" + file_path 
            print(path)
            result = parser.parse(path)
            content = result["content"][0]
            contents.append(content)
    
    if contents:
        logging.info("Resumes Parsed Successfully")
        for i in range(len(contents)):
            structured = structure_model.send(contents[i])
            doc = embedder.create_document(i, json.dumps(structured))
            documents.append(doc)
        
        embedder.add_docs(documents)
        logging.info("Resumes Embeddings Added Successfully")
    else:
        logging.error('No Resumes Found/Parsed')
    
    db.close_PS()
    return jsonify({
        "output" : "Resumes Parsed and Embedded Successfully"
    })

@app.route("/match", methods = ["POST"])
def match():
    db.connect_PS()
    data = request.get_json()
    JD = data.get("job_description")
    k = data.get("candidates")
    out = Model(JD_Prompt, model_4b).send(JD)
    summarizer = Model(Summary,model_4b)

    result = embedder.match(json.dumps(out),k)
    output = []
    for i in result:
        content = {}
        content["Name"] = i.metadata["name"]
        content["Email"] = i.metadata["email"]
        content["content"] = summarizer.send(json.dumps(i.page_content))
        output.append(content)
    db.close_PS()
    return jsonify(output)

@app.route("/interview", methods = ["GET"])
def interview():
    # 0 for non_tech and 1 for tech questions
    data = request.get_json()
    q_id = data.get("id")
    questions = evaluator.ask(q_id)
    return jsonify(questions)

@app.route("/interview",methods=["POST"])
def edit():
    data = request.get_json()
    # 0 for non_tech and 1 for tech questions
    q_id = data.get("id")
    questions = data.get("questions")
    evaluator.edit(questions,q_id)
    return jsonify({"output" : "Questions Edited Successfully"})

@app.route("/evaluate",methods = ["POST"])
def score():
    db.connect_MS()
    data = request.get_json()
    candid = data.get("user_output")
    email = data.get("email")
    password = data.get("password")
    result = evaluator.score_candid(candid)
    score = result["score"]
    query = f"Update score = {score} from users where Email = {email} and password = {password}"
    db.cursor_MS.execute(query)
    db.connection_MS.commit()
    db.close_MS()
    return jsonify(result)


def create_user():
    db.connect_MS()
    df = scheduler.df
    for name,email,date,time in zip(df["Name"],df["Email"],scheduler.date,df["Slot"]):
        password = name[:5] + email[:5]
        db.insert([name,email,date,time,password,0.0])
    
    db.connection_MS.commit()
    db.close_MS()


@app.route("/schedule", methods = ["POST"])
def email():
    data = request.get_json()
    date = data.get("date")
    time = data.get("time")
    slot_length = data.get("length")

    scheduler = Schedule()
    scheduler.defaults(date,time,slot_length)
    scheduler.schedule_slots("./test.csv")
    create_user()
    scheduler.send_emails()
    return jsonify({"output" : "Emails Sent Successfully"})

@app.route("/login-user",methods=["GET"])
def login_u():
    db.connect_MS()
    data = request.get_json()
    email = data.get("email")
    password = data.get("pass")
    query = f"SELECT * FROM users WHERE email = {email} AND password = {password}"

    result = db.cursor_MS.execute(query).fetchone()
    db.close_MS()
    if result:
        return jsonify({"user": "True"})
    else:
        return jsonify({"user": "False"})

@app.route("/login-org",methods=["GET"])
def login_o():
    db.connect_MS()
    data = request.get_json()
    email = data.get("email")
    password = data.get("pass")
    query = f"SELECT * FROM org WHERE email = {email} AND password = {password}"

    result = db.cursor_MS.execute(query).fetchone()
    db.close_MS()
    if result:
        return jsonify({"user": "True"})
    else:
        return jsonify({"user": "False"})


if __name__ == "__main__":
    app.run(debug=True)
