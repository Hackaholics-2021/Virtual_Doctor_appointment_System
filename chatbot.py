import re
import long_responses as long


def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message:
        
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def check_all_messages(message):
    highest_prob_list = {}

    # Simplifies response creation / adds it to the dict
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Responses -------------------------------------------------------------------------------------------------------
    response('Hello, tell the symptoms you have!', ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
    response('See you!', ['bye', 'goodbye'], single_response=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    response('Thank you!', ['i', 'love', 'code', 'palace'], required_words=['code', 'palace'])

    # fever
    response('How long have you had it?', ['i', 'have', 'fever'], required_words=['fever'])
    response('So sorry to hear that. Tell me your age.', ['i', 'have', 'fever','for 3','days'], required_words=['days'])
    response('Good. Let me know your body temperature.(in Fahrenheit)', ['years','months'], required_words=['years'])
    response('Do you have any other of the following symptoms?<br>Cold, Sore throat, Headache, Running nose,None of these', ['c','f'], required_words=[degree])
    response(long.R_FEVER+long.R_END, ['yes','cold','sore throat','headache','running nose','none of these'],required_words=[])

    # cold
    response('So sorry to hear that. Do you often get cold and do you think it due to any allergies?', ['i', 'have', 'cold'], required_words=['cold'])
    response('If it is due to allergies then please take an allergy test and get to know what are you allergic for and try to stay away from it. For now. Please do the following'+long.R_COUGH+long.R_END, ['yes'], required_words=['yes'])
    response(long.R_COUGH+long.R_END, ['no'],required_words=['no'])

    # neck pain
    response('On a scale of 1 to 10, how would you rate your pain?', ['i', 'have', 'neck', 'pain'], required_words=['pain'])
    response(long.R_NECK_PAIN+long.R_END, ['1','2','3','4','5','6','7','8','9','10'], required_words=[degree])

    # dandruff
    response('Sorry to hear that.'+long.R_DANDRUFF+long.R_END, ['i', 'have', 'dandruff'], required_words=['dandruff'])

    # constipation
    response('Sorry to hear that? Tell me your diet plan. Are you a fast food eater? or Home food eater?', ['i', 'have', 'constipation'], required_words=['constipation'])
    response(long.R_CONSTIPATION+long.R_END, ['Home','food','fast','eater'], required_words=['home','fast'])

    # wounds and bruises
    response('Sorry to hear that? Do you have blood leak or only skin bruises?', ['i', 'have', 'wound','bruises'], required_words=['wound'])
    response(long.R_WOUNDS+long.R_END, ['blood', 'leak','bruises'], required_words=['leak'])
    response(long.R_BRUISES+long.R_END, ['blood', 'leak','bruises'], required_words=['bruises'])


    # Longer responses
    response(long.R_ADVICE, ['give', 'advice'], required_words=['advice'])
    response(long.R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    # print(highest_prob_list)
    # print(f'Best match = {best_match} | Score: {highest_prob_list[best_match]}')

    return long.unknown() if highest_prob_list[best_match] < 1 else best_match

degree = 0.0
# Used to get the response
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    numbers = re.search(r"\d+", user_input.lower())
    if numbers:
        print(numbers.group())
        numbers = numbers.group()
        global degree
        degree = numbers

    response = check_all_messages(split_message)
    return response


# Testing the response system
# while True:
#     print('Bot: ' + get_response(input('You: ')))