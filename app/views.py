from flask import Flask, render_template, request, redirect
from threading import Thread
import csv
import logging
from binance.client import Client
from engine import run
from start import app

@app.route("/run", methods=['GET'])
def run_process():
    run()
    return redirect("/", code=302)

@app.route('/')
def homepage():

    return render_template("home.html")

