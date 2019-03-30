
import logging

log = logging.getLogger(__name__)

def parseReply(reply, token):
    try:
        rtoken       = reply[:16]
        assert rtoken == token, "Token mismatch"
        external     = reply[16:].decode('utf-8').split('\n')
        externalAddr = external[0]
        externalPort = int(external[1])
        return externalAddr, externalPort
    except Exception as e:
        log.warn(e)
        return None
