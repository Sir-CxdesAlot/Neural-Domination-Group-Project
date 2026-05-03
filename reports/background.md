# Background And Theory

This section provides the theory needed to understand the three AI tasks in the project: finding flight connections, generating a hospital shift schedule, and recognizing traffic signs from images. The explanations are written for direct use in Markdown cells in the final notebook.

## Part 1: Flight Connections Between Cities

The flight connection problem can be represented as a graph search problem. A graph is made up of nodes and edges. In this project, each city is a node, and each direct flight route is a directed edge from a source city to a destination city. Because the data in `flights.csv` stores `source_city_id` and `destination_city_id`, the direction of travel matters: a route from Windhoek to Johannesburg does not automatically mean that the reverse route also exists unless it appears separately in the data.

The goal is to find the shortest sequence of direct flights connecting a source city to a target city. The path length is measured by the number of flight connections, not by distance, ticket price, or travel time. This makes the graph unweighted for the purpose of the assignment: every direct flight counts as one step.

Breadth-first search (BFS) is appropriate for this task because BFS explores paths level by level. It first checks all cities reachable in one flight, then all cities reachable in two flights, then three, and so on. Because every edge has the same cost, the first time BFS reaches the target city, the path found has the minimum number of flight connections.

Important terms for this part:

- **State:** the current city being considered.
- **Initial state:** the source city entered by the user.
- **Goal state:** the target city entered by the user.
- **Action:** taking a direct flight from the current city to another city.
- **Frontier:** the queue of cities that have been discovered but not fully explored yet.
- **Explored set:** the set of cities that have already been processed, used to avoid repeated work and cycles.
- **Shortest path:** the sequence of `(flight_id, city_id)` pairs that leads from the source to the target using the fewest direct flights.

The required `neighbors_for_city(city_id)` function supports the search by returning every directly reachable city from a given city. The required `shortest_path(source, target)` function should then use those neighbors to construct a route. If a route exists, it should return the sequence of flight and city pairs. If no route exists, it should return `None`.

In the final explanation, the search result should be described as the number of flight connections and then shown step by step, for example: source city to first connecting city, then to the next city, until the target city is reached.

## Part 2: Hospital Shift Scheduler

The hospital shift scheduler is a constraint satisfaction problem (CSP). A CSP is a problem where values must be assigned to variables while obeying a set of rules. The objective is not just to fill the schedule, but to fill it in a way that satisfies all required constraints.

For this project, the CSP can be described as follows:

- **Variables:** the 21 weekly shift slots, made from 7 days and 3 shifts per day. Examples include `Monday_Morning`, `Monday_Afternoon`, and `Monday_Night`.
- **Domains:** the nurses who could potentially be assigned to each shift.
- **Constraints:** the rules that determine whether an assignment is valid.

The assignment describes three main constraint types:

- **Unary constraints:** a nurse cannot be assigned to a shift when that nurse is on approved leave for that day.
- **Binary constraints:** a nurse who works a Night shift cannot work the Morning shift on the next day, because this violates the rest requirement.
- **Higher-order constraints:** no nurse may work more than 5 total shifts during the 7-day schedule.

The `Shift_AI_Solver` class should use consistency checking and backtracking search to find a complete schedule. The first step is node consistency, implemented by `enforce_node_consistency()`, which removes nurses from a shift's domain when they are unavailable due to leave. This reduces invalid choices before the search begins.

The next step is arc consistency. The `revise(x, y)` function checks whether values in the domain of shift `x` are still valid when compared with shift `y`. In this project, the most important binary relationship is between a Night shift and the following day's Morning shift. If assigning a nurse to `x` would leave no valid assignment for `y`, that nurse should be removed from the domain of `x`.

The `ac3()` algorithm applies this revision process across the schedule before backtracking starts. AC-3 helps prune impossible assignments early. This makes the later search more efficient because the solver avoids exploring branches that are already inconsistent.

After consistency checking, the solver uses backtracking search. Backtracking assigns nurses to shifts one at a time. If a partial assignment violates a constraint or leads to a dead end, the solver undoes the last assignment and tries another value. This is useful for CSPs because a valid solution may require trying several combinations before all rules are satisfied.

The `select_unassigned_variable(assignment)` function should use the Minimum Remaining Values (MRV) heuristic. MRV chooses the unassigned shift with the fewest remaining legal nurses. This is a fail-fast strategy: if a shift has very few possible nurses, it is better to handle it early, because it is more likely to expose a problem in the partial schedule.

Forward checking can strengthen the backtracking process. After assigning a nurse to a shift, the solver can immediately check how that assignment affects future shifts. For example, once a nurse reaches the 5-shift limit, that nurse should no longer be considered for remaining shifts. This reduces unnecessary search and helps confirm that all 21 shifts can still be filled.

The final output should be a dictionary where each shift name maps to the assigned nurse name. The schedule is successful only if all 21 shifts are assigned, no nurse is scheduled on leave, no Night-to-next-Morning rest rule is broken, and no nurse exceeds 5 total shifts.

## Part 3: Traffic Sign Recognition

The traffic sign recognition task is a supervised learning problem. In supervised learning, the model learns from examples where each input has a known label. Here, the inputs are traffic sign images, and the labels are the sign categories represented by folders numbered `0` through `42` in the GTSRB dataset.

This task is an image classification problem because the model must assign each image to one of several possible classes. The German Traffic Sign Recognition Benchmark (GTSRB) is suitable for this because it contains many real-world traffic sign images across 43 categories. The images vary in size, lighting, angle, and clarity, which makes the task more realistic than classifying perfectly clean images.

Before training, the images must go through a preprocessing step. The assignment recommends loading each image with OpenCV, resizing it to a fixed shape such as `30x30`, and normalizing pixel values by dividing by `255.0`. Resizing is needed because neural networks expect consistent input dimensions. Normalization is useful because raw RGB values range from 0 to 255, while smaller scaled values are easier for the model to process during training.

A convolutional neural network (CNN) is appropriate for this task because CNNs are designed for grid-like image data. A CNN usually includes:

- **Convolutional layers:** learn small visual patterns such as edges, curves, colors, and shapes.
- **Activation functions:** introduce non-linear behavior so the model can learn more complex patterns.
- **Pooling layers:** reduce spatial size while keeping important visual features.
- **Dropout layers:** reduce overfitting by randomly disabling some activations during training.
- **Dense layers:** combine extracted features to make the final class prediction.
- **Softmax output layer:** converts the final outputs into class probabilities across the 43 traffic sign categories.

The dataset should be split into training and testing sets. The training set is used to update the model's weights, while the testing set is used to estimate how well the model performs on unseen images. The model should be evaluated using accuracy, but accuracy alone is not enough. A confusion matrix should also be reported because it shows which classes are being confused with each other.

Visual inspection is also required by the assignment. This means selecting some test images, running the saved model on them, and comparing the predicted labels with the true labels. This helps reveal whether the model is making reasonable mistakes, such as confusing visually similar speed limit signs, or whether it is failing on obvious examples.

The final write-up for this section should explain the full machine learning pipeline: loading images, resizing and normalizing them, assigning labels from folder names, splitting the data, defining the CNN, training the model, evaluating accuracy, reporting the confusion matrix, and inspecting selected predictions.
