#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para ejecutar un client TagFS desde la línea de comandos.
"""

import os
import sys
import optparse

# Add to the Python path the directory containing the packages in the source distribution. 
PACKAGES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'packages'))
sys.path.insert(0, PACKAGES_DIR)

# Add the contrib directory to the Python path.
CONTRIB_DIR = os.path.join(PACKAGES_DIR, 'tagfs', 'contrib')
sys.path.insert(0, os.path.abspath(CONTRIB_DIR))

from tagfs import  __version__, __authors__
from tagfs.client.cli import CLITagFSClient


EXIT_SUCCESS, EXIT_FAILURE = 0, 1


def _parse_args(argv):
    """
    Reconoce las opciones especificadas como argumentos al ejecutar el script
    en la línea de comandos.
    
    @type argv: C{list}
    @param argv: Lista de argumentos del programa.
    
    @rtype: C{tuple}
    @return: Retorna una tupla donde el primer elemento es una estructura
        que almacena la información acerca de las opciones especificadas
        y el segundo elemento es una lista con el resto de los argumentos
        que no se reconocieron como opciones.
    """
    usage = '%prog [options]'
    version = '%%prog (TagFS) v%s\n' % __version__
    authors = '\n'.join(['Copyright (C) 2010 %s' % a for a in __authors__])
    desc = 'Command line client of the tag-based distributed filesystem.'
    parser = optparse.OptionParser(usage=usage, version=version + authors, 
                                   description=desc, prog=os.path.basename(argv[0]))
    parser.add_option('-i', '--ip', action='store', dest='address', type='string', metavar='IP',
                      help='the IP address of the interface that the TagFS client should use ' \
                           'to comunicate with the TagFS servers and for its own TagFS server')
    parser.add_option('-d', '--data-dir', action='store', dest='data_dir', type='string', metavar='DIRECTORY',
                      help='directory used to keep the files saved in the TagFS server executed by this client')
    parser.add_option('-c', '--capacity', action='store', dest='capacity', type='string', metavar='CAPACITY', 
                      help='sets the storage capacity of the TagFS server executed by this client in bytes ' \
                           'optionally followed by a K, M or G suffix (default: %default)')
    parser.add_option('-r', '--replication', action='store', dest='replication', type='int', metavar='PERCENTAGE',
                      help='the replication percentage to be used during this ' \
                           'session of the TagFS client (default: %default)')
    parser.add_option('-t', '--time-server', action='store', dest='ntp_server', type='string', metavar='SERVER', 
                      help='sets the NTP server to be used during synchronization (not required)')       
    parser.set_default('capacity', '1G')        
    parser.set_default('replication', 25)
    options, args = parser.parse_args(args=argv[1:])
    if not options.address:
        parser.error('missing required --ip option')
    if not options.data_dir:
        parser.error('missing required --data-dir option')
    options.data_dir = os.path.abspath(options.data_dir)
    try:
        if options.capacity.endswith('K'):
            options.capacity = int(options.capacity[:-1]) * 1024
        elif options.capacity.endswith('M'):
            options.capacity = int(options.capacity[:-1]) * (1024 ** 2)
        elif options.capacity.endswith('G'):
            options.capacity = int(options.capacity[:-1]) * (1024 ** 3)
        else:
            options.capacity = int(options.capacity[:-1])
    except:
        parser.error('invalid required --capacity option')        
    if not (0 <= options.replication <= 100):
        parser.error('invalid replication percentage specified')    
    return options, args


def main(argv):
    """
    Función principal del script.
    
    @type argv: C{list}
    @param argv: Lista de argumentos del programa.
    
    @rtype: C{int}
    @return: Retorna 0 si no ocurrió ningún error durante la ejecución 
        del programa y 1 en el caso contrario.
    """
    options, args = _parse_args(argv)   
    client = CLITagFSClient(options.address, options.data_dir, options.capacity, 
                            options.replication, options.ntp_server)
    client.start()
    return EXIT_SUCCESS


if __name__ == '__main__':
    sys.exit(main(sys.argv))
