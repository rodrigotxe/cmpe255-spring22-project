from flask import Flask, Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from pandas.core import indexing
from .models import Note
from . import db
import json
import os
import pickle 
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure 
import io

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    app = Flask(__name__) 

    #UPLOAD_FOLDER = os.path.dirname( app.instance_path )
    
    app.config['UPLOAD_FOLDER'] = os.path.dirname( app.instance_path )

    flowers = get_flowers( ) 

    if request.method == 'POST':
        
        model = pickle.load( open( os.path.join( app.config['UPLOAD_FOLDER'], 'model_cb.pkl' ), 'rb' ) )

        flowers = updateFlowers( flowers, request.form )

        weights = calculateWeights( flowers )

        #preds_prob = model.predict_proba(features)

        #plt.savefig(os.path.join( app.static_folder, 'output.png'), dpi='figure')

        isGraphCreated = os.path.exists( os.path.join( app.static_folder, 'output.png' ) )

        return render_template( "home.html", user = current_user, isGraphCreated = isGraphCreated , flowers = flowers )
    
    return render_template( "home.html", user = current_user, flowers = flowers )


def get_flowers( ):

    flowers = { }

    flowers['astilbe'] = [ 'Astilbe', 50]
    flowers['bellflower'] = [ 'Bellflower', 50]
    flowers['black_eyed_susan'] = [ 'Black-eyed Susan', 50]
    flowers['calendula'] = [ 'Calendula', 50]
    flowers['california_poppy'] = [ 'California Poppy', 50]
    flowers['carnation'] = [ 'Carnation', 50]
    flowers['commom_daisy'] = [ 'Commom Daisy', 50]
    flowers['coreopsis'] = [ 'Coreopsis', 50]
    flowers['daffodil'] = [ 'Daffodil', 50]
    flowers['dandelion'] = [ 'Dandelion', 50]
    flowers['iris'] = [ 'Iris', 50]
    flowers['magnolia'] = [ 'Magnolia', 50]
    flowers['rose'] = [ 'Rose', 50]
    flowers['sunflower'] = [ 'Sunflower', 50]
    flowers['tulip'] = [ 'Tulip', 50 ]
    flowers['water_lily'] = [ 'Water Lily', 50 ]
        
    return flowers

def updateFlowers( flowers, form ):

    for key in flowers:

        flowers[key][1] = int( request.form.get( key ) )

    return flowers

def calculateWeights( flowers ):

    weight = []

    total = 0

    for key in flowers:

        total += flowers[key][1]

    for key in flowers:

        weight.append( flowers[key][1] * 100 / total )
    
    return weight