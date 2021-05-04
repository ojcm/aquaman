#!/usr/bin/python3

from werkzeug.datastructures import MultiDict
from absl import app, flags, logging
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import json

FLAGS = flags.FLAGS
flags.DEFINE_string("config_file_path", None, "Path of config file to read/write")
flags.mark_flag_as_required("config_file_path")

flask_app = Flask(__name__, template_folder=".")
Bootstrap(flask_app)  # Flask-Bootstrap requires this line


class IdentifiersForm(FlaskForm):
    id1 = StringField("Sensor 1 ID")
    id2 = StringField("Sensor 2 ID")
    id3 = StringField("Sensor 3 ID")
    id4 = StringField("Sensor 4 ID")
    id5 = StringField("Sensor 5 ID")
    id6 = StringField("Sensor 6 ID")
    id7 = StringField("Sensor 7 ID")
    id8 = StringField("Sensor 8 ID")
    submit = SubmitField("Submit")


class ConfigFile:
    def __init__(self, path):
        self.path = path
        self.config = {}
        self.read()

    def read(self):
        logging.debug("reading file " + self.path)
        with open(self.path) as f:
            self.config = json.load(f)

    def write(self):
        logging.debug("writing to " + self.path)
        with open(self.path, "w") as f:
            json.dump(self.config, f)

    def set_config(self, config):
        logging.debug("setting config: " + str(config))
        self.config = config

    def string(self):
        return json.dumps(self.config)


@flask_app.route("/", methods=["GET", "POST"])
def index():
    config = flask_app.config["aquaman_config"]
    form = IdentifiersForm(
        meta={"csrf": False},  # Disable CSRF (not required at this time)
        id1=config.config["id1"],
        id2=config.config["id2"],
        id3=config.config["id3"],
        id4=config.config["id4"],
        id5=config.config["id5"],
        id6=config.config["id6"],
        id7=config.config["id7"],
        id8=config.config["id8"],
    )

    if form.validate_on_submit():
        identifiers = {
            "id1": form.id1.data,
            "id2": form.id2.data,
            "id3": form.id3.data,
            "id4": form.id4.data,
            "id5": form.id5.data,
            "id6": form.id6.data,
            "id7": form.id7.data,
            "id8": form.id8.data,
        }
        config.set_config(identifiers)
        config.write()
        flask_app.config["aquaman_config"] = config

    return render_template("index.html", form=form, config=config.string())


def main(argv):
    del argv
    conf = ConfigFile(FLAGS.config_file_path)
    flask_app.config["aquaman_config"] = conf
    flask_app.run()


if __name__ == "__main__":
    app.run(main)
