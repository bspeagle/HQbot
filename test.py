import searchHelper
import time

start = time.time()

testAnswers = ['Big Bird and Friends', "Jim Henson's Muppets", '123 Avenue B']

searchHelper.answerQuestion('"Sesame Stree" was almost called what?', testAnswers)

end = time.time()

print('\nTime: ' + str(end - start))
