from keras.preprocessing import sequence
from keras.models import load_model
from data import encode_sentence
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# Parameters
version = 4
review_len = 128

# Model
model = load_model(("mdl_v%d.h5")%(version))

def encode_batch(arr):
    result = []
    for sentence in arr:
        result.append(encode_sentence(sentence))
    return sequence.pad_sequences(result, maxlen=review_len)

def predict_batch(arr):
    batch = encode_batch(arr)
    result = model.predict(batch, batch_size=len(batch), verbose=0)
    return result

# print(predict_batch([
# "He then joined the faculty of the University of California at Berkeley where he is a professor of computer science director of the Center for Intelligent Systems and holder of the Smith–Zadeh Chair in Engineering.",
# "He saved my pregnant daughter from drowning in a shipwreck then he delivered her baby while they rode on a piece of driftwood.",
# "He kisses her good night but things are kind of weird you know? Then he gets back in his car and starts to drive away but when he glances in his rearview mirror his blood turns cold.",
# "He proposed the Child Programme idea explaining “Instead of trying to produce a programme to simulate the adult mind why not rather try to produce one which simulated the child’s?",
# "He's adopted.",
# "He's this jolly old fat man who lives up at the North Pole and every year he flies all over the world leaving presents for all the good boys and girls.",
# "Hence reasoning and planning systems must be able to handle uncertainty.",
# "HIDDEN MARKOV MODELS  In terms of methodology AI has finally come firmly under the scientific method."
# ]))