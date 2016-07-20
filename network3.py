#!/usr/bin/python

from time import sleep
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import Controller
from mininet.node import OVSController
from mininet.cli import CLI

class Example( Topo ):
    def __init__( self,**opts):
        topoopts=dict(link=TCLink)
        Topo.__init__( self,**opts )

        # Add hosts 
        lma = self.addHost('lma')
        mag1 = self.addHost('mag1')
        mag2 = self.addHost('mag2')
        mag3 = self.addHost('mag3')
        mag4 = self.addHost('mag4')

        host1 = self.addHost('host1')
        host2 = self.addHost('host2')
        host3 = self.addHost('host3')
        host4 = self.addHost('host4')
        host5 = self.addHost('host5')
        host6 = self.addHost('host6')


        ##lma to mags
        self.addLink(lma, mag1)
        self.addLink(lma, mag2)
        self.addLink(lma, mag3)
        self.addLink(lma, mag4)

        ##host to mags
        self.addLink(host1, mag1) 
        self.addLink(host2, mag1)


        self.addLink(host3, mag2) 

        self.addLink(host4, mag3) 

        self.addLink(host5, mag4) 
        self.addLink(host6, mag4)

def x(subnet):
    return '192.168.' + subnet 

def reset_rp_filter(host, if_list):
    for interf in if_list:
        print host.cmd('echo 0 >/proc/sys/net/ipv4/conf/' + interf +'/rp_filter')

def ping(host, subnet):
    print host
    print host.cmd('ping -qnc 2 ' + x(subnet))

def start_mcproxy(host, config_file):
    mcproxy='/home/s/mininet-wifi/examples'
    host.cmd('xterm -e "' + mcproxy + ' -sdvv -f ' + config_file + '; sleep 2"&')

def set_interface_delay(action, host, interface, delay): #action: add/change/delete
    print host.cmd('tc qdisc ' + action + ' dev ' + interface + ' root handle 1: netem delay ' + delay)

def killall(host):
    host.cmd('killall mcproxy')    
    host.cmd('killall tester')

def set_interface_delays(lma, mag1, mag2, mag3, mag4, host1, host2, host3, host4, host5, host6):
    #action = 'add' or 'change'

    lma_mag_delay =  '20ms 5ms' #delay, jitter
    mag_host_delay =  '30ms 10ms' #delay, jitter

    set_interface_delay('add', lma, 'lma-eth0', lma_mag_delay)
    set_interface_delay('add', lma, 'lma-eth1', lma_mag_delay)
    set_interface_delay('add', lma, 'lma-eth2', lma_mag_delay)
    set_interface_delay('add', lma, 'lma-eth3', lma_mag_delay)

    set_interface_delay('add', mag1, 'mag1-eth0', lma_mag_delay)
    set_interface_delay('add', mag1, 'mag1-eth1', mag_host_delay)
    set_interface_delay('add', mag1, 'mag1-eth2', mag_host_delay)

    set_interface_delay('add', mag2, 'mag2-eth0', lma_mag_delay)
    set_interface_delay('add', mag2, 'mag2-eth1', mag_host_delay)

    set_interface_delay('add', mag3, 'mag3-eth0', lma_mag_delay)
    set_interface_delay('add', mag3, 'mag3-eth1', mag_host_delay)

    set_interface_delay('add', mag4, 'mag4-eth0', lma_mag_delay)
    set_interface_delay('add', mag4, 'mag4-eth1', mag_host_delay)
    set_interface_delay('add', mag4, 'mag4-eth2', mag_host_delay)

    set_interface_delay('add', host1, 'host1-eth0', mag_host_delay)
    set_interface_delay('add', host2, 'host2-eth0', mag_host_delay)
    set_interface_delay('add', host3, 'host3-eth0', mag_host_delay)
    set_interface_delay('add', host4, 'host4-eth0', mag_host_delay)
    set_interface_delay('add', host5, 'host5-eth0', mag_host_delay)
    set_interface_delay('add', host6, 'host6-eth0', mag_host_delay)



def TopoTest():
    topo=Example()	
    net = Mininet(topo=topo, controller = OVSController, link=TCLink)
    net.start()
    
    mag1 = net.get('mag1') 
    mag2 = net.get('mag2') 
    mag3 = net.get('mag3') 
    mag4 = net.get('mag4') 

    lma = net.get('lma')
    host1 = net.get('host1')
    host2 = net.get('host2')
    host3 = net.get('host3')
    host4 = net.get('host4')
    host5 = net.get('host5')
    host6 = net.get('host6')

    #config lma
    lma.setIP(x('1.1'), 24, 'lma-eth0')
    lma.setIP(x('2.1'), 24, 'lma-eth1')
    lma.setIP(x('3.1'), 24, 'lma-eth2')
    lma.setIP(x('4.1'), 24, 'lma-eth3')

    reset_rp_filter(lma, ['all', 'lma-eth0', 'lma-eth1','lma-eth2', 'lma-eth3'])
    start_mcproxy(lma, 'lma.conf')

    #config mag1
    mag1.setIP(x('1.2'), 24, 'mag1-eth0')
    mag1.setIP(x('10.1'), 24, 'mag1-eth1')
    mag1.setIP(x('10.2'), 24, 'mag1-eth2')

    reset_rp_filter(mag1, ['all', 'mag1-eth0', 'mag1-eth1', 'mag1-eth2'])
    start_mcproxy(mag1, 'mag1.conf')

    #config mag2
    mag2.setIP(x('2.2'), 24, 'mag2-eth0')
    mag2.setIP(x('11.1'), 24, 'mag2-eth1')

    reset_rp_filter(mag2, ['all', 'mag2-eth0', 'mag2-eth1'])
    start_mcproxy(mag2, 'mag2.conf')

    #config mag3
    mag3.setIP(x('3.2'), 24, 'mag3-eth0')
    mag3.setIP(x('12.1'), 24, 'mag3-eth1')

    reset_rp_filter(mag3, ['all', 'mag3-eth0', 'mag3-eth1'])
    start_mcproxy(mag3, 'mag3.conf')

    #config mag4
    mag4.setIP(x('4.2'), 24, 'mag4-eth0')
    mag4.setIP(x('13.1'), 24, 'mag4-eth1')
    mag4.setIP(x('13.2'), 24, 'mag4-eth2')

    reset_rp_filter(mag4, ['all', 'mag4-eth0', 'mag4-eth1', 'mag4-eth2'])
    start_mcproxy(mag4, 'mag4.conf')

    #config host1 
    host1.setIP(x('10.3'), 24, 'host1-eth0')
    reset_rp_filter(host1, ['all', 'host1-eth0'])

    #config host2 
    host2.setIP(x('10.4'), 24, 'host2-eth0')
    reset_rp_filter(host2, ['all', 'host2-eth0'])

    #config host3 
    host3.setIP(x('11.2'), 24, 'host3-eth0')
    reset_rp_filter(host3, ['all', 'host3-eth0'])

    #config host4 
    host4.setIP(x('12.2'), 24, 'host4-eth0')
    reset_rp_filter(host4, ['all', 'host4-eth0'])

    #config host5 
    host5.setIP(x('13.3'), 24, 'host5-eth0')
    reset_rp_filter(host5, ['all', 'host5-eth0'])


    #config host6 
    host6.setIP(x('13.4'), 24, 'host6-eth0')
    reset_rp_filter(host6, ['all', 'host6-eth0'])

    
    #delays
    set_interface_delays(lma, mag1, mag2, mag3, mag4, host1, host2, host3, host4, host5, host6)

    #run programms
    ##################################################
    print "*** Running CLI"
    CLI( net )

    tester='/home/swapna/mininet-wifi/examples'

    host2.cmd('xterm -e "' + tester + ' h2_recv; sleep 2"&')
    host1.cmd('xterm -e "' + tester + ' h1_send; sleep 2"&')
    
    sleep(300)

   
    print 'all killed'

if __name__=='__main__':
    TopoTest()

