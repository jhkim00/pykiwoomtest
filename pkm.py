import kiwoom

_pkm = None


def pkm():
    global _pkm
    if _pkm is None:
        _pkm = kiwoom.KiwoomManager()
    return _pkm