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
            if (ticker.endswith('LI')):
                return None
            if (ticker == '6301JT'): #2022-08-24 6301JT -> KMTUY
                return 'KMTUY'
            if (ticker == '4689 JT' or ticker == '4689JT'):
                return '4689.T'
            if (ticker == 'DSYSJ'):
                return 'DSY.JO'

        #tickers with 4 or less letters not catch by previous "if"
        if (ticker == 'FB'):  #2022-08-24 FB -> META
            return 'META'
        if ticker == 'DSY':
            return 'DSY.JO'
        if ticker == 'HOFP' or ticker == 'HO':
            return 'HO.PA'
        if ticker == 'ADYYF' or ticker == 'ADYENNA' or ticker == 'ADYEN': #2022-08-24 ADYEN -> ADYEY
            return 'ADYEY'
        if ticker == 'CMIIU':
            return 'SLGC'
        # https://www.globenewswire.com/en/news-release/2022/07/25/2484749/11974/en/Pluristem-Therapeutics-Inc-Changes-its-Name-to-Pluri-Inc-Reflecting-the-Company-s-Strategy-to-Leverage-its-Innovative-3D-Cell-based-Technology-Platform-to-Additional-Industries.html
        if ticker == 'PSTI':
            return 'PLUR' # 2022-07-25 change from Pluristem Therapeutics (Nasdaq: PSTI) to Pluri Inc. (Nasdaq: PLUR)
        if (ticker in (
            'CMLF',
            'ACIC', 
            'GLEO', 
            'AONE', 
            'EXPC', 
            'SRNG', 
            'SPFR', 
            'RTP',
            'DYNS', #2022-08-24 DYNAMICS SPECIAL PURPOSE CORP
            'SLGCW', # Completed its business combination with CM Life Sciences II, Inc. (Nasdaq: CMIIU), a special purpose acquisition company sponsored by affiliates of leading healthcare and life sciences fund advisors Casdin Capital and Corvex Management. Following the transaction, the combined company was renamed SomaLogic, Inc., and its Class A common stock and warrants will begin trading on the Nasdaq Global Market (“Nasdaq”) on September 2, 2021 under the symbols “SLGC” and “SLGCW,” respectively
            'DRNA', # Buyout offer from Novo Nordisk is giving Dicerna shareholders a big reason to cheer.
            'KVSB', # Khosla Ventures Acquisition Co.
            'RAVN', # CNH Industrial Completes the Acquisition of Raven Industries
            'XONE', # ExOne will continue to operate as a wholly owned subsidiary of Desktop Metal
            'XLNX'  # XLNX acquired by AMD.
            'ZY'  # 2022-10-19 Ginkgo Bioworks Completes Acquisition of Zymergen
            )):
            return None
        
        return ticker

