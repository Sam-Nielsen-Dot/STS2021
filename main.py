from depressionAnalysis.depressionAnalysis import classify, get_classifier

classifier = get_classifier(2)

print(classify("I hate my life"))
print(classify("I hate my life", mode="probabilities", classifier=classifier))
#[2, 3, 4, 5, 8, 9, 10, 11, 12, 13, 14, 26, 27, 28, 29, 30, 31, 76]