from flask import Flask, Blueprint, render_template, request, flash
from flask_login import login_required, current_user

import os

import tensorflow as tf

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

import numpy as np

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure 

views = Blueprint('views', __name__)

@login_required
@views.route('/', methods=['GET', 'POST'])
def home():

    app = Flask(__name__) 

    app.config['UPLOAD_FOLDER'] = os.path.dirname( app.instance_path )

    flowers = get_flowers( ) 

    model_id = 1

    if request.method == 'POST':

        model_id = int( request.form.get( 'models' ) )

        multiplier = 127
        
        if model_id == 1:

            model_name = 'gan_not_trained.h5'

            multiplier = 2000

        elif model_id == 2: 

            model_name = 'gan.h5'

            multiplier = 500

        elif model_id == 3:

            model_name = 'cycle_gan.h5'

        elif model_id == 4:

            model_name = 'cycle_gan_v2.h5'    

        model = tf.keras.models.load_model( model_name )

        flowers = updateFlowers( flowers, request.form )

        seed = np.random.normal( 1,16 ) * 0.2

        weight = np.array( calculateWeights( flowers ) ).astype(np.float32) * 0.8

        weight = seed + weight

        #seed = tf.random.normal([1, 16])

        predictions = model( tf.constant( [ weight ] ) )

        #predictions = model( tf.constant( [ calculateWeights( flowers ) ] ) )

        plt.clf()

        plt.imshow( predictions[0] * multiplier )

        plt.savefig( os.path.join( app.static_folder, 'output.png'), dpi = 'figure' )
        
        isGraphCreated = os.path.exists( os.path.join( app.static_folder, 'output.png' ) )

        return render_template( "home.html", user = current_user, isGraphCreated = isGraphCreated , flowers = flowers, model = model_id )
    
    return render_template( "home.html", user = current_user, flowers = flowers, model = model_id )

def get_flowers( ):

    flowers = { }

    flowers['astilbe'] = [ 'Astilbe', 100]
    flowers['bellflower'] = [ 'Bellflower', 100]
    flowers['black_eyed_susan'] = [ 'Black-eyed Susan', 100]
    flowers['calendula'] = [ 'Calendula', 100]
    flowers['california_poppy'] = [ 'California Poppy', 100]
    flowers['carnation'] = [ 'Carnation', 100]
    flowers['commom_daisy'] = [ 'Commom Daisy', 100]
    flowers['coreopsis'] = [ 'Coreopsis', 100]
    flowers['daffodil'] = [ 'Daffodil', 100]
    flowers['dandelion'] = [ 'Dandelion', 100]
    flowers['iris'] = [ 'Iris', 100]
    flowers['magnolia'] = [ 'Magnolia', 100]
    flowers['rose'] = [ 'Rose', 100]
    flowers['sunflower'] = [ 'Sunflower', 100]
    flowers['tulip'] = [ 'Tulip', 100 ]
    flowers['water_lily'] = [ 'Water Lily', 100 ]
        
    return flowers

def updateFlowers( flowers, form ):

    for key in flowers:

        flowers[key][1] = int( request.form.get( key ) )

    return flowers

def calculateWeights( flowers ):

    maxWeight = 0

    minWeight = 100

    weight = []

    total = 0

    for key in flowers: 
        
        total += flowers[key][1]

    for key in flowers:

        aux = flowers[key][1] * 100 / total 

        weight.append( ( aux / 50.0 - 1 ) )
    
    return weight