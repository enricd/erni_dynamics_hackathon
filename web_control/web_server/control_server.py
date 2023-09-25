from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        word = request.form.get('word', 'default')
        print("rec:", word)
        cmd1 = "cd /home/pi/picar-x/example/our_tests; python3 minecart_PRO.py"
        #cmd1 = "cd /home/pi/picar-x/example/; python3 tts_example.py"
        proc = os.system(cmd1)
        print("proc:", proc)


    return render_template_string('''
<html>
<head>
    <style>
        body {
            background-image: url("https://i.postimg.cc/SxvN27h1/Screenshot-2023-09-24-at-19-42-11.png");
            background-size: cover;
            background-position: center;
        }

        .container {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 80vh;

        }

        button {
            margin-top: 10px;
            width: 120px;
            height: 50px;
            font-size: 20px;
        }

        img {
            margin-top: -100px;
            width: 100%;
        }
    </style>
</head>

<body>
    <div class="container">
        <form action="/" method="post">
            <img src="https://2e136746ca9f.ngrok.app/video_feed" width="100%">
            <button type="submit" name="word" value="Go!">Go!</button>
        </form>
    </div>
</body>
</html>
''')

if __name__ == '__main__':
    app.run(debug=True)