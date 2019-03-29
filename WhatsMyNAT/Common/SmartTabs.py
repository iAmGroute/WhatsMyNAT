
class SmartTabs:

    def __init__(self):
        self.columns = [0]

    def __call__(self, line):
        cells = line.split('\t')
        cols  = self.columns

        # Pad as needed or update existing columns
        for a in range(0, min(len(cells), len(cols))):
            padding = cols[a] - len(cells[a])
            if padding > 0:
                cols[a]  += padding
                cells[a] += ' ' * padding

        # Add new columns if needed
        for b in range(a + 1, len(cells)):
            cols.append(len(cells[b]))

        return ''.join(cells)

    def reset(self):
        self.columns = [0]

t = SmartTabs()
