#!/usr/bin/env python
import os
import jinja2
import webapp2

#################
#Characteristics
#################
#HAIR COLOR DICTIONARY
hairColors = {
    "black" : "CCAGCAATCGC",
    "brown" : "GCCAGTGCCG",
    "blonde": "TTAGCTATCGC"
}

# FACIAL SHAPE DICTIONARY
facialShapes = {
    "Square": "GCCACGG",
    "Round": "ACCACAA",
    "Oval": "AGGCCTCA"
}

# EYE COLOR DICTIONARY
eyeColors = {
    "Blue": "TTGTGGTGGC",
    "Green": "GGGAGGTGGC",
    "Brown": "AAGTAGTGAC"
}

# GENDER DICTIONARY
genders = {
    "Female": "TGAAGGACCTTC",
    "Male": "TGCAGGAACTTC"
}

#RACE DICTIONARY
races = {
"White": "AAAACCTCA",
"Black": "CGACTACAG",
"Asian": "CGCGGGCCG"
}

##########################
#end of characteristics
##########################

# a function that will compare the human characteristics to the found DNA!
def compareDNA(characteristics,dna):
    char = ""

    for char in characteristics:  # let's loop through our list and match the DNA!

        analisys = dna.find(characteristics[char])

        if analisys != -1:
            return char


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")

class AnalysisHandler(BaseHandler):
    def post(self):
        dna = self.request.get("dna")

        hairResult= compareDNA(hairColors, dna)
        faceResult = compareDNA(facialShapes, dna)
        eyeResult = compareDNA(eyeColors, dna)
        genderResult = compareDNA(genders, dna)
        raceResult = compareDNA(races, dna)

        params = {"hair":hairResult, "face":faceResult, "eyes":eyeResult, "gender": genderResult, "race":raceResult}
        
        return self.render_template("results.html", params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/analysis',AnalysisHandler)
], debug=True)
