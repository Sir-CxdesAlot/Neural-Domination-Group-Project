# Background And Theory

This section provides the theory used by the final notebook and report for the three implemented AI tasks: finding flight connections, generating a hospital shift schedule, and recognizing traffic signs from images. The explanations are aligned with the runnable code and the evaluation outputs in `reports/evaluation_metrics.json`.

## Part 1: Flight Connections Between Cities

The flight connection problem is represented as a graph search problem. A graph is made up of nodes and edges. In this project, each city is a node, and each direct flight route is a directed edge from a source city to a destination city. Because `flights.csv` stores `source_city_id` and `destination_city_id`, the direction of travel matters: a route from Windhoek to Johannesburg does not automatically mean that the reverse route exists unless it appears separately in the data.

The goal is to find the shortest sequence of direct flights connecting a source city to a target city. The path length is measured by the number of flight connections, not by distance, ticket price, or travel time. This makes the graph unweighted for this assignment: every direct flight counts as one step.

The implementation uses breadth-first search (BFS) because BFS explores paths level by level. It first checks all cities reachable in one flight, then all cities reachable in two flights, then three, and so on. Because every edge has the same cost, the first time BFS reaches the target city, the path found has the minimum number of flight connections.

Important terms for this part:

- **State:** the current city being considered.
- **Initial state:** the source city entered by the user.
- **Goal state:** the target city entered by the user.
- **Action:** taking a direct flight from the current city to another city.
- **Frontier:** the queue of cities that have been discovered but not fully explored yet.
- **Explored set:** the set of cities already processed, used to avoid repeated work and cycles.
- **Shortest path:** the sequence of `(flight_id, city_id)` pairs that leads from the source to the target using the fewest direct flights.

The implemented `neighbors_for_city(city_id, cities)` function returns every directly reachable destination from a given city. The implemented `shortest_path(source, target, cities)` function uses those neighbors to construct a BFS route. If a route exists, it returns the sequence of flight and city pairs. If no route exists, it returns `None`. If the source and target are the same city, it returns an empty list because zero connections are required.

The evaluation used `data/demo_flights/` because the official assignment flight dataset is not tracked in this repository. The demo evaluation passed all 4 test cases, including reachable routes, a zero-hop route, and a disconnected route.

## Part 2: Hospital Shift Scheduler

The hospital shift scheduler is a constraint satisfaction problem (CSP). A CSP assigns values to variables while obeying a set of rules. The objective is not just to fill the schedule, but to fill it in a way that satisfies all required constraints.

For this project, the CSP is defined as follows:

- **Variables:** the 21 weekly shift slots, made from 7 days and 3 shifts per day. Examples include `Monday_Morning`, `Monday_Afternoon`, and `Monday_Night`.
- **Domains:** the nurses who could potentially be assigned to each shift.
- **Constraints:** the rules that determine whether an assignment is valid.

The scheduler enforces three main constraint types:

- **Unary constraints:** a nurse cannot be assigned to a shift when that nurse is on approved leave for that day.
- **Binary constraints:** a nurse who works a Night shift cannot work the Morning shift on the next day, because this violates the rest requirement.
- **Higher-order constraints:** no nurse may work more than 5 total shifts during the 7-day schedule.

The `Shift_AI_Solver` class uses consistency checking and backtracking search to find a complete schedule. The first step is node consistency, implemented by `enforce_node_consistency()`, which removes nurses from a shift's domain when they are unavailable due to leave. This reduces invalid choices before the search begins.

The next step is arc consistency. The `revise(x, y)` function checks the Night-to-next-Morning rest relationship. If assigning a nurse to Night shift `x` would leave no valid assignment for the following Morning shift `y`, that nurse is removed from the domain of `x`.

The `ac3()` algorithm applies this revision process across the schedule before backtracking starts. AC-3 helps prune impossible assignments early. This makes the later search more efficient because the solver avoids exploring branches that are already inconsistent.

After consistency checking, the solver uses backtracking search. Backtracking assigns nurses to shifts one at a time. If a partial assignment violates a constraint or leads to a dead end, the solver undoes the last assignment and tries another value.

The `select_unassigned_variable(assignment)` function uses the Minimum Remaining Values (MRV) heuristic. MRV chooses the unassigned shift with the fewest remaining legal nurses. This is a fail-fast strategy: if a shift has very few possible nurses, it is better to handle it early because it is more likely to expose a problem in the partial schedule.

Forward checking strengthens the backtracking process. After assigning a nurse to a shift, the solver immediately checks how that assignment affects future shifts. For example, once a nurse reaches the 5-shift limit, that nurse is no longer considered for remaining shifts. This reduces unnecessary search and helps confirm that all 21 shifts can still be filled.

The final output is a dictionary where each shift name maps to the assigned nurse name. The demo evaluation used `data/demo_staff/staff_small.txt`, assigned all 21 shifts, produced no leave violations, produced no rest-rule violations, and kept the maximum shifts assigned to any nurse at 5.

## Part 3: Traffic Sign Recognition

The traffic sign recognition task is a supervised learning problem. In supervised learning, the model learns from examples where each input has a known label. Here, the inputs are traffic sign images, and the labels are the sign categories represented by folders numbered `0` through `42`.

The assignment context is the German Traffic Sign Recognition Benchmark (GTSRB), a 43-class traffic sign image classification benchmark. The final evaluation in this workspace used the extracted dataset at `gtsrb/Train`, which contains 39,209 labeled training images arranged in class folders `0` through `42`.

Before training, the images go through preprocessing in `load_gtsrb()`. Each image is loaded with OpenCV, resized to `30x30`, converted into an array, and normalized by dividing pixel values by `255.0`. Resizing is needed because the CNN expects consistent input dimensions. Normalization scales raw pixel values into a smaller numeric range that is easier for the model to process during training.

A convolutional neural network (CNN) is appropriate for this task because CNNs are designed for grid-like image data. The implemented baseline CNN uses:

- **Convolutional layers:** learn small visual patterns such as edges, curves, colors, and shapes.
- **ReLU activations:** introduce non-linear behavior so the model can learn more complex patterns.
- **Max-pooling layers:** reduce spatial size while keeping important visual features.
- **Dropout layers:** reduce overfitting by randomly disabling some activations during training.
- **Dense layers:** combine extracted features to make the final class prediction.
- **Softmax output layer:** converts the final outputs into class probabilities across the 43 traffic sign categories.

The training pipeline uses an 80/20 stratified train/test split, a 10% validation split inside the training set, categorical cross-entropy loss, the Adam optimizer, and accuracy as the main metric. The evaluation also produces a confusion matrix and sample prediction visualizations, because accuracy alone does not show which classes are being confused.

The final GTSRB evaluation trained for 6 epochs with batch size 32. It achieved held-out test accuracy `0.9872`, with `7,742 / 7,842` correct predictions. The generated figures are `reports/figures/confusion.png`, `reports/figures/sample_predictions.png`, and `reports/figures/training_curve.png`.
