import api_helper as api
print('-------------------Discussion Start-------------------')
result = ''
wrappedConversationHistory = ''

def addToResult(text):
    print(text)
    global result
    result = result + '\n\n' + text

def summarizeAnswerAndSaveInHistory(text, politician):
    x = open('templates/prompts/summary-prompt.txt', "r")
    summary_prompt = x.read()
    summary_prompt = summary_prompt.replace("<Politiker>", politician)
    summary_prompt = summary_prompt.replace("<Text>", text)
    summary_response = api.getAnswerFromChatGPT(summary_prompt, '')
    global wrappedConversationHistory
    wrappedConversationHistory = wrappedConversationHistory + '\n' + summary_response


f = open('templates/politicians/olaf-scholz.txt', "r")
politician_1 = f.read()
politician_1_name = 'Olaf Scholz'

f = open('templates/politicians/alice-weidel.txt', "r")
politician_2 = f.read()
politician_2_name = 'Alice Weidel'

f = open('templates/politicians/gregor-gysi.txt', "r")
politician_3 = f.read()
politician_3_name = 'Gregor Gysi'

politicians = [politician_1, politician_2, politician_3]
politicians_str = str(politicians)

politicians_names = [politician_1_name, politician_2_name, politician_3_name]

f = open('templates/topics/ukraine.txt', "r")
topic = f.read()


#Beginn
f = open('templates/prompts/moderator/moderator-start-prompt.txt', "r")
moderator_start_prompt = f.read()
moderator_start_prompt = moderator_start_prompt.replace("<PolitikerListe>", politicians_str)
moderator_start_prompt = moderator_start_prompt.replace("<Thema>", topic)
moderator_start_response = api.getAnswerFromChatGPT(moderator_start_prompt, '')
addToResult('Anne Will: ' + moderator_start_response)

f = open('templates/prompts/moderator/moderator-first-question-prompt.txt', "r")
moderator_first_question_prompt = f.read()
moderator_first_question_prompt = moderator_first_question_prompt.replace("<PolitikerListe>", politicians_str)
moderator_first_question_prompt = moderator_first_question_prompt.replace("<Thema>", topic)
moderator_first_question_prompt = moderator_first_question_prompt.replace("<Politiker>", politicians[0])
moderator_first_question_response = api.getAnswerFromChatGPT(moderator_first_question_prompt, '')
addToResult('Anne Will: ' + moderator_first_question_response)

f = open('templates/prompts/politician/politician-answer-system-prompt.txt', "r")
politician_answer_system_prompt = f.read()
politician_answer_system_prompt = politician_answer_system_prompt.replace("<PolitikerListe>", politicians_str)
politician_answer_system_prompt = politician_answer_system_prompt.replace("<Thema>", topic)
politician_answer_system_prompt = politician_answer_system_prompt.replace("<Politiker>", politicians[0])
politician_answer_system_prompt = politician_answer_system_prompt.replace("<Historie>", 'Dies ist die erste Frage. Es wurden noch keine Argumente ausgetauscht')

f = open('templates/prompts/politician/politician-first-answer-user-prompt.txt', "r")
politician_answer_user_prompt = f.read()
politician_answer_user_prompt = politician_answer_user_prompt.replace("<Frage>", moderator_first_question_response)
politician_answer_response = api.getAnswerFromChatGPT(politician_answer_user_prompt, politician_answer_system_prompt)
addToResult(politicians_names[0] + ': ' + politician_answer_response)
summarizeAnswerAndSaveInHistory(politician_answer_response, politicians[0])


#Hauptteil
politician_index = 1
conversation_round_index = 1
while conversation_round_index < 7:
    f = open('templates/prompts/moderator/moderator-question-system-prompt.txt', "r")
    moderator_question_system_prompt = f.read()
    moderator_question_system_prompt = moderator_question_system_prompt.replace("<PolitikerListe>", politicians_str)
    moderator_question_system_prompt = moderator_question_system_prompt.replace("<Thema>", topic)
    moderator_question_system_prompt = moderator_question_system_prompt.replace("<Historie>", wrappedConversationHistory)

    f = open('templates/prompts/moderator/moderator-question-user-prompt.txt', "r")
    moderator_question_user_prompt = f.read()
    moderator_question_user_prompt = moderator_question_user_prompt.replace("<Politiker>", politicians[politician_index])
    moderator_question_user_response = api.getAnswerFromChatGPT(moderator_question_user_prompt, moderator_question_system_prompt)
    addToResult('Anne Will: ' + moderator_question_user_response)

    f = open('templates/prompts/politician/politician-answer-system-prompt.txt', "r")
    politician_answer_system_prompt = f.read()
    politician_answer_system_prompt = politician_answer_system_prompt.replace("<PolitikerListe>", politicians_str)
    politician_answer_system_prompt = politician_answer_system_prompt.replace("<Thema>", topic)
    politician_answer_system_prompt = politician_answer_system_prompt.replace("<Politiker>", politicians[politician_index])
    politician_answer_system_prompt = politician_answer_system_prompt.replace("<Historie>", wrappedConversationHistory)

    f = open('templates/prompts/politician/politician-answer-user-prompt.txt', "r")
    politician_answer_user_prompt = f.read()
    politician_answer_user_prompt = politician_answer_user_prompt.replace("<Frage>", moderator_question_user_response)
    politician_answer_response = api.getAnswerFromChatGPT(politician_answer_user_prompt, politician_answer_system_prompt)
    addToResult(politicians_names[politician_index] + ': ' + politician_answer_response)
    summarizeAnswerAndSaveInHistory(politician_answer_response, politicians[politician_index])

    if politician_index + 1 == len(politicians):
        politician_index = 0
    else:
        politician_index += 1
    conversation_round_index += 1

#Abschluss
f = open('templates/prompts/moderator/moderator-end-system-prompt.txt', "r")
moderator_end_system_prompt = f.read()
moderator_end_system_prompt = moderator_end_system_prompt.replace("<PolitikerListe>", politicians_str)
moderator_end_system_prompt = moderator_end_system_prompt.replace("<Thema>", topic)
moderator_end_system_prompt = moderator_end_system_prompt.replace("<Historie>", wrappedConversationHistory)
moderator_end_response = api.getAnswerFromChatGPT('Beende die Talkshow mit ein paar kurzen Sätzen.', moderator_end_system_prompt)
addToResult('Anne Will: ' + moderator_end_response)



print('wrappedConversationHistory:')
print(wrappedConversationHistory)
print('-------------------Discussion End-------------------')
print(result)
