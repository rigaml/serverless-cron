class ticker_converter:

    @staticmethod
    def convert_yahoo_name(ticker: str) -> str:
        if not isinstance(ticker, str):
            raise ValueError(f"Ticker should be a string: {ticker}")

        if (len(ticker) > 4):
            if (ticker.endswith('JP')):
                return ticker[:-2] + ".T"
            if (ticker.endswith('HK')):
                return ticker[:-2] + ".HK"
            if (ticker.endswith('FP')):
                return ticker[:-2] + ".PA"
            if (ticker.endswith('CN')):
                return ticker[:-2] + ".TO"
            if (ticker.endswith('DSYSJ')):
                return 'DSY.JO'
            if (ticker.endswith('LI')):
                return None
            if ticker == 'ADYENNA':
                return 'ADYYF'
            if ticker == 'CMIIU':
                return 'SLGC'
                
        if ticker == 'CMLF':
            return None
        if ticker == 'HOFP' or ticker == 'HO':
            return 'HO.PA'
        if (ticker in (
            'ACIC', 
            'GLEO', 
            'AONE', 
            'EXPC', 
            'SRNG', 
            'SPFR', 
            'RTP',
            'SLGCW', # Completed its business combination with CM Life Sciences II, Inc. (Nasdaq: CMIIU), a special purpose acquisition company sponsored by affiliates of leading healthcare and life sciences fund advisors Casdin Capital and Corvex Management. Following the transaction, the combined company was renamed SomaLogic, Inc., and its Class A common stock and warrants will begin trading on the Nasdaq Global Market (“Nasdaq”) on September 2, 2021 under the symbols “SLGC” and “SLGCW,” respectively
            'DRNA', # Buyout offer from Novo Nordisk is giving Dicerna shareholders a big reason to cheer.
            'KVSB', # Khosla Ventures Acquisition Co.
            'RAVN', # CNH Industrial Completes the Acquisition of Raven Industries
            'XONE' # ExOne will continue to operate as a wholly owned subsidiary of Desktop Metal
            ,)):
            return None
        
        return ticker

