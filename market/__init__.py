default_app_config = 'market.apps.MarketConfig'
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    if 'precio' in self.initial:
        self.initial['precio'] = int(self.initial['precio'])