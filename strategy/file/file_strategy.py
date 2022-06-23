from strategy.utils import Strategy


class FileStrategy(Strategy):
    async def do_algorithm(self, data):
        with open('dotem.txt', 'w') as f:
            for record in data:
                f.write(str(record) + '\n')
