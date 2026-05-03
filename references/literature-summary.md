# Literature And Source Summary

This file summarizes the main sources used to support the project background. The summaries are paraphrased and focused on how each source helps explain the assignment.

## 1. CS50 AI Search Notes

- **Link:** https://cs50.harvard.edu/ai/notes/0/
- **Relevant project part:** Flight connections between cities.

The CS50 AI search notes explain how search problems use states, actions, transition models, goal tests, path costs, nodes, frontiers, and explored sets. This is directly relevant to the flight route task because each city can be treated as a state, each direct flight can be treated as an action, and the target city is the goal state.

The notes also distinguish depth-first search from breadth-first search. BFS uses a queue-style frontier and explores shallower paths before deeper paths. This supports the choice of BFS for the assignment because the project asks for the fewest number of flight connections in an unweighted graph, where each direct flight counts as one step.

## 2. CS50 AI Constraint Satisfaction Notes

- **Link:** https://cs50.harvard.edu/ai/2023/notes/3/
- **Relevant project part:** Hospital shift scheduler.

The CS50 AI CSP notes explain how constraint satisfaction problems are defined using variables, domains, and constraints. This matches the hospital scheduler: the variables are shift slots, the domain is the set of available nurses, and the constraints include leave days, rest periods, and the maximum number of weekly shifts.

The notes also cover node consistency, arc consistency, AC-3, backtracking search, and the Minimum Remaining Values heuristic. These concepts map directly to the required `Shift_AI_Solver` methods. Node consistency handles unary constraints such as leave days. Arc consistency helps enforce binary constraints such as the Night-to-next-Morning rest rule. Backtracking then searches for a complete assignment while MRV helps choose the most constrained shift first.

## 3. German Traffic Sign Benchmarks Website

- **Link:** https://benchmark.ini.rub.de/
- **Relevant project part:** Traffic sign recognition.

The German Traffic Sign Benchmarks website provides context for the GTSRB dataset. It identifies GTSRB as a large multi-category traffic sign recognition benchmark connected to the IJCNN 2011 competition. This supports the assignment's use of GTSRB as a realistic benchmark for traffic sign image classification.

The site is also useful because it points to the recommended citation for work using the dataset. This is important for the final report because the dataset should be acknowledged properly rather than treated as an anonymous collection of images.

## 4. Stallkamp et al. GTSRB Paper

- **Link:** https://www.ini.rub.de/upload/file/1470692848_f03494010c16c36bab9e/StallkampEtAl_GTSRB_IJCNN2011.pdf
- **Relevant project part:** Traffic sign recognition.

The GTSRB paper describes the dataset as a real-world traffic sign recognition benchmark with more than 50,000 images and 43 classes. It explains that traffic sign recognition is difficult because images can vary by distance, lighting, weather, partial occlusion, rotation, and scale.

This source supports the motivation for using machine learning and CNNs. The model must learn visual patterns that are robust to real-world variation, not just memorize clean examples. The paper also helps explain why evaluation on unseen test images matters: the goal is to check whether the trained model generalizes to new traffic sign images.

## 5. TensorFlow Image Classification Tutorial

- **Link:** https://www.tensorflow.org/tutorials/images/classification
- **Relevant project part:** Traffic sign recognition.

The TensorFlow image classification tutorial explains a practical image classification workflow: load images from folders, split data into training and validation sets, prepare batches, improve input pipeline performance, and standardize image values. This supports the assignment's requirement to load traffic sign images from class folders and preprocess them before training.

The tutorial also emphasizes scaling RGB values into a smaller numeric range. This connects directly to the project hint to normalize image pixel values by dividing by `255.0`.

## 6. TensorFlow CNN Tutorial

- **Link:** https://www.tensorflow.org/tutorials/images/cnn
- **Relevant project part:** Traffic sign recognition.

The TensorFlow CNN tutorial demonstrates how a convolutional neural network can be built for image classification using convolutional and pooling layers. This supports the architecture discussion for the traffic sign task because CNNs are well suited to images, where local visual patterns such as edges and shapes are important.

For the final report, this source helps explain why layers such as `Conv2D`, `MaxPooling2D`, dense layers, and a final classification layer are appropriate for recognizing traffic signs.

## 7. scikit-learn Confusion Matrix Documentation

- **Link:** https://scikit-learn.org/1.5/modules/generated/sklearn.metrics.confusion_matrix.html
- **Relevant project part:** Traffic sign recognition evaluation.

The scikit-learn documentation explains that a confusion matrix compares true labels with predicted labels. This is relevant because the assignment requires both accuracy and a confusion matrix for the trained traffic sign model.

Accuracy gives a single overall performance score, while the confusion matrix gives more detail by showing which classes are predicted correctly and which classes are mixed up. This is especially useful for GTSRB because some traffic signs are visually similar and may be confused by the model.

## How These Sources Support The Project

Together, these sources support the project in three ways:

- They justify BFS for finding the minimum number of flight connections.
- They explain why the nurse scheduling task is a CSP and how AC-3, MRV, and backtracking help solve it.
- They support the CNN-based traffic sign pipeline and the required evaluation using accuracy, a confusion matrix, and visual inspection.
