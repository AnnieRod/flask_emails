from flask import request, redirect, render_template,session, request

from flask_app import app

from flask_app.models.email import Mail

@app.route('/')
def start_form():
    return render_template('index.html')

##Recupera info para mostrar correos registrados
@app.route('/success')
def all_emails():
    return render_template("list.html", emails = Mail.get_emails())

##BONUS NINJA: Elimina entrada de correo 
@app.route("/destroy/<int:id>")
def destroy_email(id):
    data = {
        "id": id
    }
    Mail.delete_mail(data)
    return redirect('/success')

##Procesa info de form y valida
@app.route('/process', methods = ['POST'])
def create_email():
    if not Mail.validate_email(request.form):
        return redirect("/")
    Mail.save_email(request.form)
    return redirect('/success')

if __name__ == "__main__":
    app.run(debug=True)
