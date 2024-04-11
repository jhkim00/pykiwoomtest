import pykiwoom

_pkm = None


def pkm():
    global _pkm
    if _pkm is None:
        _pkm = pykiwoom.KiwoomManager()
    return _pkm