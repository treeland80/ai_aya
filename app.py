from flask import Flask, render_template, request
import os

app = Flask(__name__)

DOSSIER = "data"


def charger_docs():
    docs = []

    for f in os.listdir(DOSSIER):
        if f.endswith(".txt"):
            with open(os.path.join(DOSSIER, f), "r", encoding="utf-8") as file:
                docs.append((f, file.read().lower()))

    return docs


documents = charger_docs()


def chercher(question):
    question = question.lower().split()
    resultats = []

    for nom, texte in documents:
        score = 0
        for mot in question:
            if mot in texte:
                score += 1

        if score > 0:
            resultats.append((score, nom, texte))

    resultats.sort(reverse=True)
    return resultats


def reponse(question):
    res = chercher(question)

    if not res:
        return "Je n'ai trouvé aucune information dans mes documents."

    _, nom, texte = res[0]

    return f"Selon {nom} :\n\n{texte[:400]}..."


@app.route("/", methods=["GET", "POST"])
def home():
    answer = ""

    if request.method == "POST":
        question = request.form["question"]
        answer = reponse(question)

    return render_template("index.html", answer=answer)


if __name__ == "__main__":
    app.run(debug=True)