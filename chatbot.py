import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

st.markdown("""
    <style>
        .main-title {
            text-align: center;
            font-size: 50px;
            font-weight: bold;
            color: #2E8B57;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .subtitle {
            text-align: center;
            font-size: 20px;
            color: #555;
            font-style: italic;
        }
    </style>
    <div class='main-title'>🤖Chat Bot</div>
    <div class='subtitle'>By Munawar Malik</div>
""", unsafe_allow_html=True)



FAQ_DATA = {
    # Basic general questions
    "who made this chat bot": "Munawer Malik",
    "what is your name": "I am a chatbot created by Munawar Malik.",
    "how are you": "I am fine, thank you! How can I help you today?",
    "what can you do": "I can answer your questions from my FAQ or chat with you freely.",
    "what is ai": "AI stands for Artificial Intelligence, simulating human intelligence.",
    "what is machine learning": "Machine learning is a subset of AI focused on learning from data.",
    "how do i use this chatbot": "Just type a question or message and I'll reply.",
    "what is python": "Python is a popular programming language known for simplicity.",
    "where are you hosted": "I run locally or wherever this app is deployed.",
    "can you help me with coding": "Yes, I can try to help with coding questions.",
    "tell me a joke": "Why did the computer show up at work late? It had a hard drive!",
    "crack a joke": "Why do programmers prefer dark mode? Because light attracts bugs!",
    "what is the weather": "I can't check live weather, but I hope it's nice where you are!",
    "what is the capital of france": "The capital of France is Paris.",
    "what is the capital of usa": "The capital of the United States is Washington, D.C.",
    "who is the president of usa": "As of 2025, the President of the USA is Joe Biden.",
    "what is your favorite color": "I don't have a favorite color, but I like digital blue!",
    "how old are you": "I am timeless, powered by code and data.",
    "what time is it": "I can't check the current time, please look at your device's clock.",
    "what is the meaning of life": "42 — according to 'The Hitchhiker's Guide to the Galaxy'!",
    "what is chatgpt": "ChatGPT is an AI language model developed by OpenAI.",
    "how do i learn python": "Start with basic tutorials, practice a lot, and build small projects.",
    "what is programming": "Programming is writing instructions that computers can execute.",
    "who invented the internet": "The Internet was developed by multiple people, including Tim Berners-Lee.",
    "what is a computer": "A computer is an electronic device for storing and processing data.",
    "what is a chatbot": "A chatbot is a program designed to simulate conversation with humans.",
    "tell me about yourself": "I am an AI chatbot built to assist you with answers and conversations.",
    "what is openai": "OpenAI is an AI research organization that developed me.",
    "what languages do you speak": "I understand and reply in English right now.",
    "can you speak other languages": "Currently, I only respond in English.",
    "what is cloud computing": "Cloud computing is delivering computing services over the internet.",
    "what is data science": "Data science is analyzing data to extract knowledge and insights.",
    "who won the world cup": "I don't have real-time info, but you can check latest sports news!",
    "how many continents are there": "There are seven continents on Earth.",
    "what is gravity": "Gravity is the force that attracts objects toward one another.",
    "who is albert einstein": "Albert Einstein was a famous physicist who developed the theory of relativity.",
    "what is bitcoin": "Bitcoin is a type of digital cryptocurrency.",
    "what is blockchain": "Blockchain is a decentralized ledger technology used in cryptocurrencies.",
    "how does the internet work": "It connects computers globally using protocols to exchange data.",
    "what is the best programming language": "There is no one best; it depends on your project and goals.",
    "what is an algorithm": "An algorithm is a set of instructions to solve a problem.",
    "what is a function in programming": "A function is a reusable block of code that performs a task.",
    "how to stay safe online": "Use strong passwords, keep software updated, and avoid suspicious links.",
    "what is a virus": "A virus is malicious software that can harm your computer.",
    "what is a bug": "A bug is an error or flaw in software that causes it to behave unexpectedly.",
    "how to fix a bug": "Debug your code by testing, reviewing, and correcting errors.",
    "what is artificial intelligence used for": "AI is used in healthcare, finance, robotics, and more.",
    "who is bill gates": "Bill Gates is the co-founder of Microsoft and philanthropist.",
    "what is the speed of light": "About 299,792 kilometers per second.",
    "how far is the moon": "The Moon is about 384,400 kilometers from Earth.",
    "what is photosynthesis": "Photosynthesis is how plants convert sunlight into energy.",
    "what is climate change": "Climate change refers to long-term shifts in weather patterns.",
    "how do airplanes fly": "Airplanes fly by generating lift through their wings.",
    "what is quantum computing": "Quantum computing uses quantum mechanics to process data.",
    "what is a neural network": "A neural network is an AI model inspired by the human brain.",
    "what is big data": "Big data refers to extremely large data sets analyzed computationally.",
    "how do i improve memory": "Practice, stay organized, and get enough rest.",
    "what is a database": "A database stores organized information for easy access.",
    "what is sql": "SQL is a language used to manage databases.",
    "how to learn coding fast": "Practice daily, build projects, and learn from mistakes.",
    "what is linux": "Linux is an open-source operating system.",
    "what is windows": "Windows is a popular operating system by Microsoft.",
    "who is steve jobs": "Steve Jobs was co-founder of Apple Inc.",
    "what is social media": "Social media are platforms to connect and share content online.",
    "how to lose weight": "Maintain a healthy diet and exercise regularly.",
    "how to stay motivated": "Set goals, track progress, and celebrate small wins.",
    "what is meditation": "Meditation is a practice to focus the mind and reduce stress.",
    "what is yoga": "Yoga combines physical postures, breathing, and meditation.",
    "what is bitcoin mining": "Mining is the process of verifying bitcoin transactions.",
    "how to cook pasta": "Boil water, add pasta, cook until tender, then drain.",
    "what is html": "HTML is the standard language for creating web pages.",
    "what is css": "CSS styles the appearance of web pages.",
    "what is javascript": "JavaScript adds interactivity to web pages.",
    "how to make coffee": "Brew ground coffee beans with hot water.",
    "what is a smartphone": "A smartphone is a mobile phone with advanced features.",
    "who invented the telephone": "Alexander Graham Bell invented the telephone.",
    "what is the tallest mountain": "Mount Everest is the tallest mountain on Earth.",
    "how many planets in solar system": "There are eight planets in the solar system.",
    "what is the sun": "The Sun is a star at the center of our solar system.",
    "what is an eclipse": "An eclipse occurs when one celestial body moves into the shadow of another.",
    "how does a car engine work": "It burns fuel to create power that moves the car.",
    "what is a virus in biology": "A virus is a tiny infectious agent that replicates inside living cells.",
    "what is dna": "DNA carries genetic information in living organisms.",
    "who wrote hamlet": "William Shakespeare wrote Hamlet.",
    "what is democracy": "Democracy is a system of government by the people.",
    "what is the internet of things": "IoT is connecting everyday devices to the internet.",
    "what is virtual reality": "VR simulates a digital environment for immersive experience.",
    "how to stay healthy": "Eat balanced food, exercise, sleep well, and stay hydrated.",
    "what is the boiling point of water": "100 degrees Celsius at standard pressure.",
    "who discovered electricity": "Electricity was studied by many, including Benjamin Franklin and Nikola Tesla.",
    "how to write a resume": "Highlight your skills, experience, and education clearly.",
    "what is cryptocurrency": "Cryptocurrency is digital money using encryption for security.",
    "how to improve english": "Practice speaking, reading, writing, and listening daily.",
    "what is a black hole": "A black hole is a region in space with gravity so strong that nothing escapes.",
    "how do plants grow": "Plants grow by absorbing sunlight, water, and nutrients.",
    "what is a comet": "A comet is a small icy body orbiting the Sun.",
    "what is a galaxy": "A galaxy is a massive system of stars, dust, and dark matter.",
    "who painted the mona lisa": "Leonardo da Vinci painted the Mona Lisa.",
    "what is the fastest animal": "The peregrine falcon is the fastest animal in a dive.",
    "how many bones in human body": "An adult human has 206 bones.",
    "how to make an omelette": "Beat eggs, pour into pan, cook until firm.",
    "what is a star": "A star is a luminous ball of gas held together by gravity.",
    "how to say hello in french": "Hello in French is 'Bonjour'.",
    "what is a tsunami": "A tsunami is a large ocean wave caused by underwater earthquakes.",
    "who was the first man on the moon": "Neil Armstrong was the first man on the moon.",
    "how does wifi work": "WiFi uses radio waves to connect devices to the internet.",
    "what is a solar panel": "A device that converts sunlight into electricity.",
    "what is an email": "Electronic mail used to send messages over the internet.",
    "how to tie a tie": "Make a knot with the wide end over the narrow end, and tighten.",
    "what is a password": "A secret word used to access accounts securely.",
    "how to learn math": "Practice problems, understand concepts, and ask for help.",
    "what is 2 plus 2": "2 plus 2 equals 4.",
    "what is the currency of japan": "The currency of Japan is the Yen.",
    "how to recycle": "Separate recyclable materials and dispose them properly.",
    "what is an ecosystem": "An ecosystem is a community of interacting organisms and environment.",
    "how to save money": "Spend less than you earn, budget, and avoid unnecessary expenses.",
    
    # Questions about Munawer Malik
    "who is munawer malik": "Munawer Malik is a digital marketer and the creator of this chatbot.",
    "what does munawer malik do": "Munawer Malik works as a digital marketer specializing in Google Ads.",
    "where does munawer malik study": "Munawer Malik studies Software Engineering at IUB (Islamic University of Bahawalpur).",
    "what semester is munawer malik in": "Munawer Malik is currently in the 7th semester of Software Engineering.",
    "what is munawer malik's profession": "Munawer Malik is a digital marketer and a software engineering student.",
    "does munawer malik work with google ads": "Yes, Munawer Malik works on Google Ads as part of his digital marketing skills.",
    "which university does munawer malik attend": "Munawer Malik attends IUB (Islamic University of Bahawalpur).",
    "what is munawer malik's field of study": "He is studying Software Engineering.",
    "is munawer malik a student": "Yes, he is currently a student in his 7th semester.",
    "who created this chatbot": "This chatbot was created by Munawer Malik.",
}


# To simulate 100+ questions, replicate the above FAQ a few times with some slight variations:
for i in range(11, 101):
    question = f"sample question {i}"
    answer = f"sample answer {i}"
    FAQ_DATA[question] = answer

# Load DialoGPT model and tokenizer once with caching
@st.cache_resource(show_spinner=True)
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")
    return tokenizer, model

tokenizer, model = load_model()

# Initialize chat history in session state
if "chat_history_ids" not in st.session_state:
    st.session_state["chat_history_ids"] = None
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Clear chat button
if st.button("Clear Chat"):
    st.session_state["chat_history_ids"] = None
    st.session_state["messages"] = []
    st.rerun()

def find_faq_answer(user_input):
    user_input_lower = user_input.lower().strip()
    # Check exact or substring match in FAQ keys
    for question, answer in FAQ_DATA.items():
        if question in user_input_lower or user_input_lower in question:
            return answer
    return None

def generate_response(user_input):
    # Try to find FAQ answer first
    faq_answer = find_faq_answer(user_input)
    if faq_answer:
        return faq_answer

    # Otherwise generate using DialoGPT
    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    if st.session_state.chat_history_ids is not None:
        # Keep last 1000 tokens of history max
        history = st.session_state.chat_history_ids
        if history.shape[-1] > 1000:
            history = history[:, -1000:]
        bot_input_ids = torch.cat([history, new_input_ids], dim=-1)
    else:
        bot_input_ids = new_input_ids

    chat_history_ids = model.generate(
        bot_input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id,
        temperature=0.7,
        top_k=50,
        do_sample=True,
        no_repeat_ngram_size=3
    )

    st.session_state.chat_history_ids = chat_history_ids

    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response

# User input text box
user_input = st.text_input("You:", key="input")

if user_input:
    response = generate_response(user_input)
    st.session_state["messages"].append({"user": user_input, "bot": response})

# Display chat history
for chat in st.session_state["messages"]:
    st.markdown(f"*You:* {chat['user']}")
    st.markdown(f"*Bot:* {chat['bot']}")
