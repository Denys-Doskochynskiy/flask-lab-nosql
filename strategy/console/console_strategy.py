from strategy.utils import Strategy


class ConsoleStrategy(Strategy):
    async def do_algorithm(self, data):
        print(f"Console response:\n{data}")
