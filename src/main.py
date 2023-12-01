from src.network.neural_network import NeuralNetwork
import matplotlib.pyplot as plt
import numpy as np


class App:
    """This is the main program
    the user interacts with.
    """

    def __init__(self):
        self.nn = NeuralNetwork()
        self.test_images = None
        self.test_labels = None

    def run(self):
        self._choose_network()
        # Run the rest of the program with trained network
        while True:
            do = input(
                "Test the network(1), visualize the network(2), choose a new network(3) or quit(4): ")
            if do == "1":
                self.test_network()
            elif do == "2":
                self.data_visualization()
            elif do == "3":
                self._choose_network()
            elif do == "4":
                break
        print()

    def _choose_network(self):
        setup = input("Load a pre-trained network(1) or train a network(2): ")
        if setup == "1":
            cust = input("Load latest(1) or specify network(2): ")
            if cust == "1":
                print("Loading network...")
                self.nn.load_saved_network(load_latest=True)
            elif cust == "2":
                name = input("Specify filename: ")
                print("Loading network...")
                try:
                    self.nn.load_saved_network(
                        load_latest=False, filename=name)
                except FileNotFoundError:
                    print("No such file...")
                    self._choose_network()
        elif setup == "2":
            self.nn.train_network()

    def test_network(self):
        self.test_images, self.test_labels = self.nn.get_test_data()
        test_size = input(
            "Do a quick test of 100 images(1), a medium test of 2 000 images(2) or a full test of 10 000 images(3): ")

        if test_size == "1":
            self._quick_test(100)
        elif test_size == "2":
            self._quick_test(2000)
        elif test_size == "3":
            self._full_test()

    def _full_test(self):
        """Perform in-depth test
        for network accuracy.
        """
        class_accuracy = {}
        for i in range(self.nn.num_of_classes):
            class_accuracy[str(i)] = [0, 0]  # left is correct pred

        result = 0
        for num in range(len(self.test_images)):
            prediction = self.nn.predict(self.test_images[num])
            if prediction == self.test_labels[num]:
                result += 1
                class_accuracy[str(prediction)][0] += 1
            class_accuracy[str(self.test_labels[num])][1] += 1

        print(f"Test accuracy: {(result / len(self.test_images))*100:.1f}%")

        self.test_visualization(class_accuracy)

    def _quick_test(self, size):
        """Perform fast test for
        network accuracy.
        """
        class_accuracy = {}
        for i in range(self.nn.num_of_classes):
            class_accuracy[str(i)] = [0, 0]  # left is correct pred

        result = 0
        nums = [np.random.randint(0, len(self.test_images))
                for i in range(size)]

        for num in nums:
            prediction = self.nn.predict(self.test_images[num])
            if prediction == self.test_labels[num]:
                result += 1
                class_accuracy[str(prediction)][0] += 1
            class_accuracy[str(self.test_labels[num])][1] += 1

        print(f"Test accuracy: {(result / len(nums))*100:.1f}%")

        self.test_visualization(class_accuracy)

    def data_visualization(self):
        """Visualize data going
        through the network.
        """
        print("Here we can see an input image of a number go through the network.")
        self.nn.get_layer_activations()

    def test_visualization(self, results):
        """This function visualizes
        test results based on each
        class accuracy.
        """
        labels = [i for i in range(self.nn.num_of_classes)]
        percentages = []
        for i in range(self.nn.num_of_classes):
            # get the percentage of correct pred for every class
            # this class didn't appear in the test set
            if results[str(i)][1] == 0:
                percentages.append(0.0)
                continue
            percentages.append((results[str(i)][0] / results[str(i)][1])*100)

        plt.bar(labels, percentages, tick_label=labels)
        plt.xlabel("Class Label")
        plt.ylabel("Correct predictions (%)")
        plt.title("Correct Predictions per Class")
        plt.show()


if __name__ == "__main__":
    a = App()
    a.run()
