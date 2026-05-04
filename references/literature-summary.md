# Literature And Source Summary

This file summarizes the main sources used to support the final project background, notebook, and report. The summaries are paraphrased and focused on how each source supports the implemented methods and evaluation outputs.

## 1. CS50 AI Search Notes

- **Link:** https://cs50.harvard.edu/ai/notes/0/
- **Relevant project part:** Flight connections between cities.

The CS50 AI search notes explain search problems in terms of states, actions, transition models, goal tests, path costs, nodes, frontiers, and explored sets. This directly supports the flight-route implementation because each city is treated as a state, each direct flight is treated as an action, and the target city is the goal state.

The notes also distinguish depth-first search from breadth-first search. BFS uses a queue-style frontier and explores shallower paths before deeper paths. This supports the project's implemented use of BFS in `shortest_path()` because the route graph is treated as unweighted, where each direct flight counts as one connection. The final report can therefore justify that the first target reached by BFS is a minimum-hop route.

## 2. CS50 AI Constraint Satisfaction Notes

- **Link:** https://cs50.harvard.edu/ai/2023/notes/3/
- **Relevant project part:** Hospital shift scheduler.

The CS50 AI CSP notes explain how constraint satisfaction problems are defined using variables, domains, and constraints. This matches the implemented hospital scheduler: the variables are weekly shift slots, the domain is the set of nurses, and the constraints include leave days, rest periods, and a maximum of 5 shifts per nurse.

The notes also cover node consistency, arc consistency, AC-3, backtracking search, and the Minimum Remaining Values heuristic. These concepts map directly to the `Shift_AI_Solver` pipeline. Node consistency handles leave-day pruning, AC-3 handles Night-to-next-Morning rest arcs, MRV chooses the next constrained shift, and backtracking with forward checking searches for a complete valid schedule.

## 3. German Traffic Sign Benchmarks Website

- **Link:** https://benchmark.ini.rub.de/
- **Relevant project part:** Traffic sign recognition.

The German Traffic Sign Benchmarks website provides context for the GTSRB dataset. It identifies GTSRB as a multi-category traffic sign recognition benchmark connected to the IJCNN 2011 competition. This supports the assignment framing for Part 3 and explains why a traffic-sign classifier is a realistic image classification task.

The final workspace does not track the official GTSRB dataset. The report therefore distinguishes between the intended GTSRB problem context and the generated synthetic `data/demo_gtsrb/` dataset used to validate the implemented pipeline.

## 4. Stallkamp et al. GTSRB Paper

- **Link:** https://www.ini.rub.de/upload/file/1470692848_f03494010c16c36bab9e/StallkampEtAl_GTSRB_IJCNN2011.pdf
- **Relevant project part:** Traffic sign recognition.

The GTSRB paper describes traffic sign recognition as a real-world benchmark with more than 50,000 images and 43 classes. It explains that images vary by distance, lighting, weather, partial occlusion, rotation, and scale.

This source supports the motivation for using machine learning and CNNs. A classifier must learn visual patterns that generalize across changing image conditions, not just memorize clean examples. In the final report, this source motivates the CNN approach while the demo results are reported separately as synthetic pipeline-validation results.

## 5. TensorFlow Image Classification Tutorial

- **Link:** https://www.tensorflow.org/tutorials/images/classification
- **Relevant project part:** Traffic sign recognition.

The TensorFlow image classification tutorial explains a practical image classification workflow: load images from folders, split data into training and validation sets, prepare batches, improve input pipeline performance, and standardize image values.

This supports the implemented Part 3 pipeline because `load_gtsrb()` loads images from class-numbered folders, resizes them to `30x30`, and normalizes pixel values by dividing by `255.0`. The final notebook connects this preprocessing step to the model's expected input shape and training stability.

## 6. TensorFlow CNN Tutorial

- **Link:** https://www.tensorflow.org/tutorials/images/cnn
- **Relevant project part:** Traffic sign recognition.

The TensorFlow CNN tutorial demonstrates how convolutional and pooling layers can be used for image classification. This supports the architecture discussion for the implemented baseline CNN because the model uses `Conv2D`, `MaxPooling2D`, dropout, dense layers, and a 43-unit softmax output layer.

The final report uses this source to justify why CNN layers are appropriate for traffic sign images: local visual features such as borders, symbols, shapes, and colors can be learned and combined into class-level predictions.

## 7. scikit-learn Confusion Matrix Documentation

- **Link:** https://scikit-learn.org/1.5/modules/generated/sklearn.metrics.confusion_matrix.html
- **Relevant project part:** Traffic sign recognition evaluation.

The scikit-learn documentation explains that a confusion matrix compares true labels with predicted labels. This supports the evaluation output generated for Part 3 because the final report includes both overall accuracy and a confusion matrix figure.

Accuracy gives a single performance score, while the confusion matrix shows where predictions are correct or confused across classes. This is useful for traffic sign recognition because some signs can be visually similar.

## How These Sources Support The Final Project

Together, these sources support the final project in three ways:

- They justify BFS for finding the minimum number of directed flight connections.
- They explain why the nurse scheduler is a CSP solved with node consistency, AC-3, MRV, forward checking, and backtracking.
- They support the CNN-based traffic sign pipeline and the evaluation using accuracy, a confusion matrix, training curves, and sample predictions.
