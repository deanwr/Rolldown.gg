from flask import Flask, render_template, url_for, flash, redirect, jsonify
from forms import InputForm
from rolldownMath import calculate

application = app = Flask(__name__)
app.config['SECRET_KEY'] = 'NotTheRealKey'

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = InputForm()
    if form.validate_on_submit():
        oneUnitProbPerRoll, expectedUnitsPerRoll, oneUnitProbTotalGold, expectedUnitsTotalGold = calculate(form.level.data, form.unitCost.data, form.unitsSameCostGone.data,
            form.unitsGone.data, form.gold.data)
        flash(f'One Unit Probability Per Roll:  {"{:.2%}".format(oneUnitProbPerRoll)}')
        flash(f'Expected Units Per Roll: {"{:.03f}".format(expectedUnitsPerRoll)}')
        flash(f'One Unit Probability - Total Gold: {"{:.2%}".format(oneUnitProbTotalGold)}')
        flash(f'Expected Units - Total Gold: {"{:.03f}".format(expectedUnitsTotalGold)}')
        #return render_template('home.html', form=form)
    return render_template('home.html', form=form)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/help")
def help():
    return render_template('help.html', title='Help')

@app.route("/new")
def new():
    return render_template('new.html', title='New')

if __name__ == '__main__':
    app.run(debug=True)
