import matplotlib.pyplot as plt

class Visualizer:
    '''
    Visualize the result
    '''

    def __init__(self,debug_mode = 0):
        self.is_debug = debug_mode
        self.datax = []
        self.datay = []
        self.fig = plt.figure()
        self.p = self.fig.add_subplot(1, 1, 1)
        #plt.show()

    def insert_data(self,input:tuple):
        '''
        Insert the data
        :param input: tuple:(score,index)
        :return: No return
        '''
        score, index = input
        self.datax.append(index)
        self.datay.append(score)
        if self.is_debug:
            print("Data inserted: ",score,index)

    def plot_single(self):
        '''
        Plot the index-score figure
        :return:
        '''
        self.p.cla()
        self.p.scatter(self.datax,self.datay)
        plt.xlabel("index", fontdict={'size': 16})
        plt.ylabel("score", fontdict={'size': 16})
        plt.ion()
        plt.show()
        # plt.pause(0.5)


    def plot_average(self):
        '''
        Plot the average of 10 results/group
        :return:
        '''
        groups = int(len(self.datax) / 10)
        new_x = [i for i in range(0,groups)]
        new_y = []
        for i in range(0,groups):
            average = sum(self.datay[10 * i:10 * i + 10])
            new_y.append(average)
        assert len(new_x) == len(new_y)
        self.p.cla()
        self.p.scatter(new_x, new_y)
        plt.xlabel("index", fontdict={'size': 16})
        plt.ylabel("score", fontdict={'size': 16})
        plt.ion()
        plt.show()
        plt.pause(0.5)




if __name__ == "__main__":
    v = Visualizer()
    for i in range(0,10):
        v.insert_data((5 * i,i))
        v.plot_single()







