import web
import git
import subprocess
import os
from lepl.apps.rfc3696 import Email

ARCHIVE_LOC = "archive"

#Set the template folder
render = web.template.render("templates/")

#Create upload form
isalnum = lambda str: str.isalnum()
upload_form = web.form.Form(
        web.form.Textbox("Simulation name",
            validator=web.form.Validator("Must be alphanumeric", isalnum)),
        web.form.Textbox("Author"),
        web.form.Textbox("Email",
            validator=web.form.Validator("Email address invalid", Email())),
        web.form.Textbox("Project number"),
        web.form.Textbox("Tags"),
        web.form.Textarea("Description"),
        )

#
#Helper functions
#
def store_file(fh, filename, upload_dir):
    filename = "%s/%s" % (upload_dir, filename)
    with open(filename, "wb+") as uploadfh:
        uploadfh.write(fh.read())
    return filename

#
#Define some view classes
#
class index(object):
    def __init__(self):
        self.title = "Simulation Archive"

    def GET(self):
        cur_form = upload_form()
        return render.index(self.title, cur_form)

    def POST(self):
        form = upload_form()

        #Handle file upload
        uploads = web.input(simarchive={})
        if "simarchive" in uploads:
            simfile = uploads.simarchive.file
            simfilename = uploads.simarchive.filename
            stored_file_name = store_file(simfile, simfilename, "/tmp")

        if form.validates():
            #Unpack uploaded archive
            repo_name = form["Simulation name"].value.replace(" ", "_")
            repo_path = "%s/%s.git/" % (ARCHIVE_LOC, repo_name)
            if os.path.exists(repo_path):
                return "Archive exists, aborting!"
            os.mkdir(repo_path)
            ret = subprocess.call(["tar", "xf", stored_file_name,
                    "-C", repo_path])

            #Init git archive
            os.environ.update({"GIT_AUTHOR_NAME" : form["Author"].value})
            os.environ.update({"GIT_AUTHOR_EMAIL" : form["Email"].value})
            repo = git.Repo.init(repo_path)
            repo.index.add("*")
            repo.index.commit("Initial archive import")
        else:
            return "FAIL\nSimulation name = %s" % form["Simulation name"].value

        #return render.index(form)

#Map urls -> classes to handle views
urls = (
        '/', "index"
        )

#Set up the webapp
app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
