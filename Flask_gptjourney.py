import openai
import os
# For the UI
from io import BytesIO
import base64
from PIL import Image
from flask import Flask, render_template, request, session
# Regular expressions:
import re
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai.api_key  = os.getenv('OPENAI_API_KEY')
base_path="C:/Users/djarv/Documents/GitHub/GalBot/"
# Create a new Flask app and set the secret key
app = Flask(__name__,static_folder='static')
app.secret_key = "mysecretkey" #Needed to use flask session
from utils.text2img import def_text2img,SD_APICALL
def gen_img(text,URL="http://127.0.0.1:7860",img_path="./story_app/static/images/"):
    #try:
        payload=def_text2img.copy()
        payload["prompt"]=payload["prompt"].replace("SNAKE",text)
        r=SD_APICALL(payload,URL)
        image = r['images'][0]
        image = Image.open(BytesIO(base64.decodebytes(image.encode("utf-8"))))
        os.makedirs(img_path,exist_ok=True)
        i=len(os.listdir(img_path))+1
        image.save(f"{img_path}{i}.png")
        
        return f"/static/images/{i}.png"
    #except Exception as e:
        # if it fails (e.g. if the API detects an unsafe image), use a default image
      #  img_url = "https://pythonprogramming.net/static/images/imgfailure.png"
     #   return img_url
    
def chat(inp,history, role="user"):
    history.append({"role":role,"content":inp})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = history
    )
    reply_content = completion.choices[0].message.content
    history.append({"role":"assistant","content":reply_content})
    #print(reply_content)
    #Len check
    if len(history)>25:
        init=[history[0]]
        for part in history[~0-10:]:
            init.append(part)
        history=init
    return reply_content,history

history=[ {
     "role":"user", "content": """
     You are an interactive story game bot that proposes some futuristic outerspace situation where the user needs to pick from 2-4 options that you provide.\
        The story base character is called kurumi she has Mikan colored hair and is a Wild and Pessimist adventure
        Kurumi backstory '''This planet is covered in green, yellow, and purple plants - and the tall hills are covered in blue moss! no one even bats an eyelid. It looks inhabited here, but every person is asleep in their homes, in suspended animation. Do you dare wake them? The Goddess would want you to unravel this mystery. "Im the best!" '''
        Once the user picks one of those options, \
        you will then state what happens next and present new options,\
        and this then repeats. \
        If you understand, say, OK, and begin when I say "begin." 
        When you present the story and options, 
        present just the story and start immediately with the story, 
        no further commentary, and then options like "Option 1:" "Option 2:" ...etc.
     """
}, {"role":"assistant","content":f"""OK, I Understand. Begin when your ready"""}]

@app.route("/",methods=["GET","POST"])
def home():
    title ="GPT-Journey"

    #Innital buttons 
    button_messages = {}
    button_states = {}

    if request.method == "GET":
        session["message_history"] = history
        message_history = session["message_history"]
        reply_content, message_history = chat("Begin",message_history)
        text = reply_content.split("Option 1")[0]
        # Using regex, grab the natural language options from the response
        options = re.findall(r"Option \d:.*", reply_content)
        #
        print("-----------Options-----------")
        #print(len(options))
        # Create a dictionary of button messages
        for i, option in enumerate(options):
            button_messages[f"button{i+1}"] = option
        # Initialize the button states
        for button_name in button_messages.keys():
            button_states[button_name] = False
        print("-----------buttons-----------")
        print(button_messages)
    #Post request 
    message = None 
    button_name = None
    if request.method == "POST":
        message_history = session["message_history"]
        button_messages = session["button_messages"]
        button_name = request.form.get("button_name")
        button_states[button_name] = True 
        message = button_messages.get(button_name)
        #Gen rresponse 
        reply_content, message_history = chat(message,message_history)
        text = reply_content.split("Option 1")[0]
        options = re.findall(r"Option \d:.*",reply_content)

        button_history = {} #Update buttons
        for i,option in enumerate(options):
            button_messages[f"button{i+1}"] = option
        for button_name in button_messages.keys():
            button_states[button_name] = False
    
    
    # Store the updated message history and button messages in the session
    session['message_history'] = message_history
    session['button_messages'] = button_messages
    #Img gen
    image_url = gen_img(text)
    #print("gened image ", image_url)
    #Render the template with the updated information
    return render_template('home.html', title=title, text=text, 
                            image_url=image_url, 
                            button_messages=button_messages, 
                            button_states=button_states, message=message)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5000)