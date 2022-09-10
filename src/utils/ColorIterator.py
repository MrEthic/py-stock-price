class ColorIterator:

    def __init__(self, colors=None):
        if colors is None:
            colors = ['#FECB52', '#FF97FF', '#B6E880', '#FF6692', '#19D3F3', '#FFA15A', '#AB63FA', '#00CC96', '#EF553B', '#636EFA']
        self.colors = colors
        self.current_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.current_index += 1
        if self.current_index == len(self.colors) - 1:
            self.current_index = 0

        return self.colors[self.current_index]

    @staticmethod
    def get_indicator_color(indicator: str):
        if 'ma' in indicator:
            return '#6928ED'
