import environment as env
import random
import time


env.reset()
observation, loss, done, heart_is_use = env.step(0)

"""
env.step принимает action: 1 - биться сердцу, 0 - не биться сердцу.
         возвращает:
            - observation: list, частота биения сердца и объём крови;
            - done: bool, True, если мы сердце бьётся, False - если нет;
            - heart_is_use: bool. Тут поподробнее...
                если предсердия уже начали сокращаться, то мы никак на это не повлияем,
                да и смысла в этом нет. Поэтому мы должны подавать информацию нейросети,
                если heart_is_use имеет значение False.
"""

while True:
    
    time.sleep(0.01)
    if not heart_is_use:
        action = 1 if random.randint(0, 10) % 5 == 1 else 0 # action должен генерироваться нейросетью
        observation, loss, done, heart_is_use = env.step(action)
    else:
        _, _, _, heart_is_use = env.step(0)
    
    env.render()
    #print(loss)
    #print(observation)
    
    if done:
        env.reset()