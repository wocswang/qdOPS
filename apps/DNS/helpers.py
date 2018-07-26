# Binder Helpers

# Standard Imports
import logging
import re
import socket

# 3rd Party
import dns.query
import dns.rcode
import dns.reversename
import dns.tsig
import dns.tsigkeyring
import dns.update

# App Imports
from DNS import models
from DNS.exceptions import KeyringException, RecordException

def add_Record(server,zone,record_name,record_type,ttl,record_data,key_name):

    logger = logging.getLogger('DNS.helpers')
    try:
        transfer_key = models.Key.objects.filter(name=key_name)[0]
    except models.Key.DoesNotExist as exc:
        logging.error(exc)
        raise KeyringException("The specified TSIG key %s does not exist in"
                               "binders configunation" % key_name)
    else:
        algorithm = str(transfer_key.data)

    #print server,zone,record_name,record_type,ttl,record_data,key_name,private_key
    keyring = dns.tsigkeyring.from_text({key_name:algorithm})
    update=dns.update.Update(str(zone),keyring=keyring)
    update.add(record_name,ttl,record_type,record_data)
    output =send_dns_update(update,str(server),key_name)
    #response=dns.query.tcp(update,str(server))
    return output

def edit_Record(server, zone, record_name, record_type, ttl, record_data, key_name):

    try:
        transfer_key = models.Key.objects.filter(name=key_name)[0]
    except models.Key.DoesNotExist as exc:
        logging.error(exc)
        raise KeyringException("The specified TSIG key %s does not exist in"
                               "binders configunation" % key_name)
    else:
        algorithm = str(transfer_key.data)

    keyring = dns.tsigkeyring.from_text({key_name: algorithm})
    update = dns.update.Update(zone, keyring=keyring)
    update.replace(record_name, ttl, record_type, record_data)
    output = send_dns_update(update, str(server), key_name)
    # response=dns.query.tcp(update,str(server))
    return output

def delete_Record(server, zone,record_name,record_type,record_data,key_name):
    try:
        transfer_key = models.Key.objects.filter(name=key_name)[0]
    except models.Key.DoesNotExist as exc:
        logging.error(exc)
        raise KeyringException("The specified TSIG key %s does not exist in"
                                "binders configunation" % key_name)
    else:
        algorithm = str(transfer_key.data)

    keyring = dns.tsigkeyring.from_text({str(key_name): algorithm})
    update = dns.update.Update(str(zone), keyring=keyring)
    update.delete(str(record_name),str(record_type),str(record_data))
    output = send_dns_update(update, str(server), str(key_name))
    # response=dns.query.tcp(update,str(server))
    return output


def send_dns_update(dns_message,server,key_name):

    logger=logging.getLogger('DNS.helpers')
    try:
        output=dns.query.tcp(dns_message,server)
    except dns.tsig.PeerBadKey as exc:
        logging.error(exc)
        raise KeyringException("DNS server %s is not configured for TSIG key: %s." %
                               (server, key_name))
    except dns.tsig.PeerBadSignature as exc:
        logging.error(exc)
        raise KeyringException("DNS server %s didn't like the TSIG signature "
                               "we sent. Check key %s for correctness." %
                               (server, key_name))
    logging.debug(output)
    return_code=output.rcode()
    if return_code != dns.rcode.NOERROR:
        raise RecordException('Error when requesting DNS server %s: %s' %
                                (server, dns.rcode.to_text(return_code)))
    return output



