#!/bin/bash
rm ./aligned-images/cache.t7
../openface/util/align-dlib.py ./training-images/ align outerEyesAndNose ./aligned-images/ --size 96
../openface/batch-represent/main.lua -outDir ./generated-embeddings/ -data ./aligned-images/
../openface/demos/classifier.py train ./generated-embeddings/