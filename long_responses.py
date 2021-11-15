import random

R_EATING = "I don't like eating anything because I'm a bot obviously!"
R_ADVICE = "If I were you, I would go to the internet and type exactly what you wrote there!"
R_FEVER = "You can do the following:<br>1. Take Paracetamol for 3 days after meal in the morning and night.<br>2. Take Bismol for 1 day at night after meal."
R_COUGH = 'You can do the following:<br>1. Take crocin for 3 days after meal in the morning and night.<br>2. Steam inhalation 3 times a day.'
R_NECK_PAIN = 'You can do the following:<br>1. Apply Iodex or any other balm for pain releif.<br>2. Use ice pack on the area of pain.'
R_DANDRUFF = 'I would recommend to use a good shampoo like Scalpe plus.Use it once for three days in 4 weeks.'
R_CONSTIPATION = 'Don\'t worry I will help you. If you are a fast food eater then, please reduce the intake of fast foods and try converting into staple foods like oats, rice and wheat and drink plenty of water.Try to go out for a walk.<br> If you are a home food eater use Dulcoflex Stool Softener pills.'
R_WOUNDS = 'Here\'s what you can do. Try washing the wounded area and apply disinfectant like detol. Clean and Dress the wound. If blood leak stops then it is alright!<br> But if blood leakage is high please visit a doctor immediately'
R_BRUISES = 'Here\'s what you can do. Try washing the wounded area and apply disinfectant like detol. Small bruises will heal as it dries. If bleeding occurs please address a dcotor.'
R_END = '<br><br> <i>Please note:<br>This isn\'t a diagnosis. Always visit a doctor if you\'re unsure, or if symptoms get worse, or don\'t improve. If your situation is serious, call an emergency service.</i> <br><br><br><b>If you think you want consultation please visit consult tab for consulting with top doctors</b><br><br> Or if you want to book an appointment with our top doctors, feel free to go into <b>Book Appointments</b> tab for booking appointment'

def unknown():
    response = ["Could you please re-phrase that? ",
                "Sorry, I couldn't get you :(",
                "Let's try one more time. Can you please tell once again?",
                "What does that mean?",
                "I'm not quite sure what do you mean. Sorry:(",
                "I'm just a Bot. Try something new."][
        random.randrange(6)]
    return response