from flask import Flask, render_template, request, redirect, send_file
from extractors.ro import extract_ro_jobs
from extractors.wwr import extract_wwr_jobs
from file import save_to_file

app = Flask("JobScraper")

db = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search")
def search():
    print("searching", request.args)
    keyword = request.args.get("keyword")
    site = request.args.get("site")

    if keyword == None or keyword == "":
        return redirect("/")
    if keyword in db:
        ro = db[keyword]["ro"]
        wwr = db[keyword]["wwr"]
    else:
        ro = extract_ro_jobs(keyword)
        wwr = extract_wwr_jobs(keyword)
        db[keyword] = {"ro": ro, "wwr": wwr}

    if site == "all":
        jobs = ro + wwr
    elif site == "ro":
        jobs = ro
    elif site == "wwr":
        jobs = wwr
    else:
        jobs = []
    return render_template("search.html", site=site, keyword=keyword, jobs=jobs)


@app.route("/refresh")
def refresh():
    print("refreshing", request.args)
    keyword = request.args.get("keyword")
    site = request.args.get("site")
    print(site)
    db.pop(keyword, None)
    return redirect(f"/search?site={site}&keyword={keyword}")


@app.route("/export")
def export():
    print("exporting", request.args)
    keyword = request.args.get("keyword")
    site = request.args.get("site")

    if keyword == None or keyword == "":
        return redirect("/")
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")

    if site == "all":
        data = db[keyword]["ro"] + db[keyword]["wwr"]
    elif site == "ro":
        data = db[keyword]["ro"]
    elif site == "wwr":
        data = db[keyword]["wwr"]
    else:
        data = []
    save_to_file(keyword, data)
    return send_file(f"{keyword}.csv", as_attachment=True)


app.run("127.0.0.1", port=8000, debug=True)
