from src.network.layers.classifier import Classifier
import numpy as np


class FullyConnectedLayer:
    """Fully connected layer.
    The final layer(s) in the network.
    """

    def __init__(self, num_of_classes, learning_step_size, reg_strength) -> None:
        self.number_of_classes = num_of_classes
        self.step_size = learning_step_size
        self.reg_strength = reg_strength
        self.weight_matrix = None

        self.classifier_function = Classifier(
            learning_step_size=learning_step_size, reg_strength=reg_strength)
        
        self.initialize_weight_matrix()

    def _process(self, images):
        """This is a function to process the input image
        through the layer.

        Args:
            image (_type_): input image

        Returns:
            _type_: dot product of input image and weights
        """
        flattened_images = images.flatten()
        self.received_inputs = flattened_images
        activation = np.dot(flattened_images, self.weight_matrix) + self.bias
        
        result = self.classifier_function._compute_softmax_probabilities(
            activation)

        return result

    def initialize_weight_matrix(self):
        """Initialize weight matrix for the FC layer.
        Is called when image is received so it is
        created with the correct dimensions.

        Args:
            image_shape (_type_): input image shape
        """
        self.input_image_shape = (5, 12, 12)
        #size = images_shape[0]*images_shape[1]**2
        size = 5 * 12 * 12
        self.weight_matrix = 0.01 * \
                    np.random.randn(size, self.number_of_classes) \
                    * np.sqrt(2.0 / size)
        self.bias = np.zeros((self.number_of_classes))


    def initialize_gradients(self):
        self.gradient_weight = np.zeros_like(self.weight_matrix)
        self.bias_gradient = np.zeros_like(self.bias)


    def update_parameters(self, batch_size, learning_rate):
        self.gradient_weight /= batch_size
        self.bias_gradient /= batch_size

        self.weight_matrix -= learning_rate * self.gradient_weight
        self.bias -= learning_rate * self.bias_gradient

    def backpropagation(self, gradient_score):
        """Updates the weights in the weight matrix
        with the given gradients. 

        Args:
            gradient_score (_type_): Gradient score from the previous layer

        Returns:
            _type_: Gradients for the next layer
        """
        self.received_inputs = np.array(self.received_inputs)
        self.received_inputs = self.received_inputs.reshape(1, -1)
        gradient_score = gradient_score.reshape(1, -1)

        self.gradient_weight += np.dot(self.received_inputs.T, gradient_score)

        # L2 regularization
        self.gradient_weight += self.weight_matrix*self.reg_strength

        self.bias_gradient += np.sum(gradient_score)

        gradient_for_next_layer = np.dot(gradient_score, self.weight_matrix.T)
        
        return gradient_for_next_layer.reshape(self.input_image_shape)

    def _compute_loss(self, probabilities, label):
        """Calls the classifier function to compute
        loss, which is given (the function)
        as a parameter in the initialization.

        Args:
            images (_type_): _description_
            labels (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.classifier_function._compute_cross_entropy_loss(probabilities=probabilities, label=label)

    def _compute_gradient(self, probabilities, label):
        """Calls classifier function to compute average
        gradient of a given batch. Classifier function is 
        determined in the initialization function.

        Args:
            images (_type_): _description_
            labels (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.classifier_function._compute_gradients(probabilities=probabilities, label=label)
