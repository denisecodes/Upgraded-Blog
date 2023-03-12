from flask import Flask, render_template, request
import requests
import smtplib
import os

blog_url = "https://api.npoint.io/3a99207ce70b558d517d"
response = requests.get(blog_url)
all_posts = response.json()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", posts=all_posts)

@app.route('/about')
def about():
    return render_template("about.html")

def send_email(name, email, phone, message):
    my_email = os.environ.get("MY_EMAIL")
    my_password = os.environ.get("MY_PASSWORD")
    with smtplib.SMTP("smtp.gmail.com") as connection:
        # Make connection secure and encrypts email
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=f"{my_email}",
            msg=f"Subject:New Message From Bootstrap Blog\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
        )

@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == 'POST':
        data = request.form
        name = data['name']
        email = data['email']
        phone = data['phone']
        message = data['message']
        send_email(name=name, email=email, phone=phone, message=message)
        return render_template("contact.html", msg_sent=True)
    else:
        return render_template("contact.html", msg_sent=False)

@app.route('/post/<blog_id>')
def post(blog_id):
    post_data = response.json()[int(blog_id)-1]
    return render_template("post.html", post=post_data)

if __name__ == "__main__":
    app.run(debug=True)