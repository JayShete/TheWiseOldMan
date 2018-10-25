import discord

TOKEN = 'NTA0MDgxNDE5OTA0MDkwMTIy.DrEjfA.6pgNHT7nhCAAs0sFQ5edHryNiag'
q = open("assets/Questions.txt","a+")
a = open("assets/Answers.txt","a+")
def ff():
    q.flush()
    q.seek(0)
    a.flush()
    a.seek(0)
ff()
questions = q.readlines()
answers = a.readlines()

client = discord.Client()

@client.event
async def on_message(message):
    global questions
    global answers
    ans = 'temp'
    
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('I have a question'):
        asker = message.author
        msg = 'What would your question be? {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
        message = await client.wait_for_message()
        ans = message.content
        if message.author == asker:
            print ('request:' + ans)
            if ans.endswith("?"):
                if ans+"\n" in questions:
                    msg = answers[questions.index(ans+"\n")] + '{0.author.mention}'.format(message)
                    await client.send_message(message.channel, msg)
                elif ans in questions:
                    msg = answers[questions.index(ans)]+'{0.author.mention}'.format(message)
                    await client.send_message(message.channel, msg)
                else:
                    msg = 'do you know the answer to that question so i can add it to my database? {0.author.mention}'.format(message)
                    await client.send_message(message.channel, msg)
                    anstwo = await client.wait_for_message()
                    if anstwo.author == asker:
                        if anstwo.content == 'yes':
                            msg = 'what is the answer to the question? {0.author.mention}'.format(message)
                            await client.send_message(message.channel, msg)
                            anstwo = await client.wait_for_message()
                            ff()
                            q.write("\n" + ans)
                            a.write("\n" + anstwo.content)
                            msg = 'i will now answer your question with your answer {0.author.mention}'.format(message)
                            await client.send_message(message.channel,msg)
                            ff()
                            questions = q.readlines()
                            answers = a.readlines
                        else:
                                msg = 'sorry... i am unable to help then {0.author.mention}'.format(message)
                                await client.send_message (message.channel,ans)
            else:
                msg = 'All questions must end in a question mark {0.author.mention}'.format(message)
                await client.send_message(message.channel, msg)
            return
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
