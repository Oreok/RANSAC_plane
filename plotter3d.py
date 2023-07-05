import matplotlib.pyplot as plt
import numpy as np
import random


class DataPlotter:
    def __init__(self):
        self.pitch = []
        self.roll = []
        self.distance = []

    def add_data_point(self, pitch_deg, roll_deg, correct_distance):
        self.pitch.append(pitch_deg)
        self.roll.append(roll_deg)
        self.distance.append(correct_distance)

    def get_data_array(self):
        data_array = np.array([self.pitch, self.roll, self.distance]).T
        return data_array

    def fit_plane(self, points):
        # Normal tilted plane
        # p1, p2, p3 = points
        # v1 = p2 - p1
        # v2 = p3 - p1
        # normal = np.cross(v1, v2)
        # a, b, c = normal
        # d = np.dot(normal, p3)
        # return a, b, c, d

        # Assumption that the plane is parallel to the ground

        a, b, c = 0, 0, 1

        p = points[0]
        d = np.dot(np.array([a, b, c]), p)

        return a, b, c, d

    def find_inliers(self, data, model, threshold):
        a, b, c, d = model
        distances = np.abs(np.dot(data, np.array([a, b, c])) - d)
        inliers = np.where(distances < threshold)[0]
        return inliers

    def ransac(self, data, threshold, n_iterations=100):
        best_model = None
        best_inliers = []

        for _ in range(n_iterations):
            sample = random.sample(list(data), 3)
            model = self.fit_plane(sample)
            inliers = self.find_inliers(data, model, threshold)

            if len(inliers) > len(best_inliers):
                best_model = model
                best_inliers = inliers

        return best_model, best_inliers

    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(self.pitch, self.roll, self.distance, c='r', marker='o')
        data_array = self.get_data_array()
        eq, idx_inliers = self.ransac(data_array, threshold=0.01)

        print("Model: " + str(eq))
        print("Inliners: " + str(idx_inliers))

        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        xx, yy = np.meshgrid(np.linspace(xlim[0], xlim[1], 10), np.linspace(ylim[0], ylim[1], 10))
        zz = (eq[3] - eq[0] * xx - eq[1] * yy) / eq[2]
        ax.plot_surface(xx, yy, zz, alpha=0.5, color='lime')

        point_on_plane = np.array([0, 0, eq[3] / eq[2]])
        distance_to_ground = np.linalg.norm(point_on_plane)
        ax.text(0, 0, 0, f'Distance to ceiling: {distance_to_ground:.2f}', fontsize=10, color='red')

        ax.set_xlabel('Pitch (degrees)')
        ax.set_ylabel('Roll (degrees)')
        ax.set_zlabel('Distance (cm)')
        ax.set_title('Height')

        plt.show()
