# -*- coding: utf-8 -*-

class Score():        
    def readScores():
        file = open("highScores.txt", 'r')
        
        scores = []
        
        for score in file:
            scores.append(score.strip())
            
        return scores
    
    def saveScore(score):
        file = open("highScores.txt", 'r')
        
        scores = []
        
        for i in file:
            scores.append(i.strip())
        
        scores.append(score)
        scores.sort(key=int, reverse=True)
        
        file = open("highScores.txt", 'w')
        
        if len(scores) >= 10:        
            for i in range(10):
                file.write(scores[i])
                file.write('\n')
        else:
            for i in scores:
                file.write(i)
                file.write('\n')